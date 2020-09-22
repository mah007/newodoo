# -*- coding: utf-8 -*-
##########################################################################
#
#    Copyright (c) 2015-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>)
#
##########################################################################
from odoo import api, exceptions, fields, models, _
from odoo.exceptions import ValidationError, UserError
import logging
_logger =  logging.getLogger(__name__)

class SaleOrder(models.Model):

    _inherit = 'sale.order'

    wallet_debit = fields.Float('Wallet Debit')
    wallet_txn_id = fields.Many2one(comodel_name="website.transactions",string="Wallet Transaction Id")

    def action_cancel(self):
        res= super(SaleOrder, self).action_cancel()
        for order in self:
            domain = [
                ('state','=','draft'),
                ('sale_order_id','=',order.id),
                ('reference','=','sale_order'),
            ]
            txn = self.env['website.transactions'].search(domain)
            if txn:
                # order.write({'wallet_debit': 0})
                txn.cancel()
            domain = [
                ('state','=','done'),
                ('sale_order_id','=',order.id),
                ('reference','=','sale_order'),
            ]
            txn = self.env['website.transactions'].search(domain)
            if txn:
                rec = self.env['website.transactions'].create({
                    'state': 'done',
                    'txn_type': 'credit',
                    'partner_id': order.partner_id.id,
                    'reference': 'sale_order',
                    'amount': order.wallet_debit,
                    'tag_ids': [(4,txn.wallet_id.order_cancelled_tag.id)],
                    'currency_id': order.pricelist_id.currency_id.id,
                    'wallet_id': txn.wallet_id.id,
                    'sale_order_id': order.id,
                })
                order.write({'wallet_debit': 0})
                txn.cancel()
                rec.refund()
        return res

    def _check_for_wallet_transactions(self):
        # rec = self.env['website.transactions'].create_transaction(self,'debit','sale_order')
        # transaction_ids = self.transaction_ids.filtered(lambda t: t.acquirer_id.provider != 'e_wallet')
        # done_transactions = transaction_ids.filtered(lambda t: t.state not in ['error', 'cancel', 'draft', 'pending', ''])
        # if not done_transactions:
        #     _logger.info('Inconsistency appear in wallet transaction: Cancelling Transaction: {}'.format(self.wallet_txn_id.transaction_id))
        #     self.wallet_txn_id.cancel()
        #     return

        #Done the last transaction by wallet acq.
        transaction_ids = self.transaction_ids.filtered(lambda t: t.acquirer_id.provider == 'e_wallet')
        if transaction_ids:
            transaction_id = max(transaction_ids)#get the last wallet transaction
            if transaction_id.state == 'draft':
                transaction_id._set_transaction_done()
                transaction_id._reconcile_after_transaction_done()
                transaction_id._log_payment_transaction_received()
                transaction_id.write({'is_processed': True})

        if self.wallet_txn_id.state == 'draft':
            self.wallet_txn_id.debit()

        return True

    def action_confirm(self):
        result = super(SaleOrder, self).action_confirm()
        for order in self:

            if self.wallet_debit > 0 and not self.wallet_txn_id:
                self.wallet_debit = 0
            
            # Cross check
            # Some cases are there when payment is done but confirmation page didn't hit.
            if self.wallet_debit > 0:
                res = order._check_for_wallet_transactions()

            domain = [
                ('state','=','draft'),
                ('sale_order_id','=',order.id),
                ('reference','=','sale_order'),
            ]
            txn = self.env['website.transactions'].search(domain)
            txn.write(dict(state='cancelled'))
        return result

    def _create_payment_transaction(self, vals):
        '''Similar to self.env['payment.transaction'].create(vals) but the values are filled with the
        current sales orders fields (e.g. the partner or the currency).
        :param vals: The values to create a new payment.transaction.
        :return: The newly created payment.transaction record.
        '''
        if self.wallet_debit == 0:
            return super(SaleOrder, self)._create_payment_transaction(vals)

        # Ensure the currencies are the same.
        currency = self[0].pricelist_id.currency_id
        if any([so.pricelist_id.currency_id != currency for so in self]):
            raise ValidationError(_('A transaction can\'t be linked to sales orders having different currencies.'))

        # Ensure the partner are the same.
        partner = self[0].partner_id
        if any([so.partner_id != partner for so in self]):
            raise ValidationError(_('A transaction can\'t be linked to sales orders having different partners.'))

        # Try to retrieve the acquirer. However, fallback to the token's acquirer.
        acquirer_id = vals.get('acquirer_id')
        acquirer = False
        payment_token_id = vals.get('payment_token_id')

        if payment_token_id:
            payment_token = self.env['payment.token'].sudo().browse(payment_token_id)

            # Check payment_token/acquirer matching or take the acquirer from token
            if acquirer_id:
                acquirer = self.env['payment.acquirer'].browse(acquirer_id)
                if payment_token and payment_token.acquirer_id != acquirer:
                    raise ValidationError(_('Invalid token found! Token acquirer %s != %s') % (
                    payment_token.acquirer_id.name, acquirer.name))
                if payment_token and payment_token.partner_id != partner:
                    raise ValidationError(_('Invalid token found! Token partner %s != %s') % (
                    payment_token.partner.name, partner.name))
            else:
                acquirer = payment_token.acquirer_id

        # Check an acquirer is there.
        if not acquirer_id and not acquirer:
            raise ValidationError(_('A payment acquirer is required to create a transaction.'))

        if not acquirer:
            acquirer = self.env['payment.acquirer'].browse(acquirer_id)

        # Check a journal is set on acquirer.
        if not acquirer.journal_id:
            raise ValidationError(_('A journal must be specified of the acquirer %s.' % acquirer.name))

        if not acquirer_id and acquirer:
            vals['acquirer_id'] = acquirer.id

        if self.wallet_debit:
            if acquirer.provider == 'e_wallet':
                amount = self.wallet_debit
            else:
                amount = sum(self.mapped('amount_total')) - self.wallet_debit
        else:
            amount = sum(self.mapped('amount_total'))

        vals.update({
            'amount': amount,
            'currency_id': currency.id,
            'partner_id': partner.id,
            'sale_order_ids': [(6, 0, self.ids)],
        })

        transaction = self.env['payment.transaction'].create(vals)

        # Process directly if payment_token
        if transaction.payment_token_id:
            transaction.s2s_do_transaction()

        return transaction

    def _create_custom_wallet_transation(self):
        self.ensure_one()
        acquirer_id = self.env.ref('odoo_e_wallet.payment_acquirer_wallet').id
        vals = {
            'acquirer_id': acquirer_id,
            'return_url': '/shop/payment/validate'
        }
        transaction = self._create_payment_transaction(vals)
        return transaction

class WalletSaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    wallet_transaction_id = fields.Many2one(comodel_name="website.transactions")

class Invoice(models.Model):
    _inherit = "account.move"

    def get_wallet_order(self):
        order =  self.env['sale.order'].search([('name','=',self.invoice_origin)])
        return order
