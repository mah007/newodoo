# coding: utf-8
import logging
import requests

from odoo.tools import float_compare
from odoo.exceptions import UserError
from odoo import api, fields, models, _
from odoo.addons.payment.models.payment_acquirer import ValidationError

_logger = logging.getLogger(__name__)

class PaymentAcquirerWallet(models.Model):
    _inherit = 'payment.acquirer'

    provider = fields.Selection(selection_add=[('e_wallet', 'E-Wallet')])

    def e_wallet_form_generate_values(self, values):
        return values

    def e_wallet_get_form_action_url(self):
        return '/payment/wallet/feedback'
        # return '/shop/payment/validate'

    def e_wallet_compute_fees(self, amount, currency_id, country_id):
        return 0.0

    def _get_feature_support(self):
        vals = super(PaymentAcquirerWallet, self)._get_feature_support()
        # vals.get('authorize').append('e_wallet')
        return vals

    # def toggle_website_published(self):
    #     ''' When clicking on the website publish toggle button, the website_published is reversed and
    #     the acquirer journal is set or not in favorite on the dashboard.
    #     '''
    #     self.ensure_one()
    #     if self.provider == 'e_wallet' and self.website_published == False:
    #         raise UserError(_('This acquirer is not meant to be published!'))
    #         return False
    #     return super(PaymentAcquirerWallet, self).toggle_website_published()

    # def write(self, vals):
    #     self.ensure_one()
    #     if self.provider == 'e_wallet':
    #         raise UserError(_('This acquirer is not meant to be Enabled`!'))
    #         return False
    #     return super(PaymentAcquirerWallet, self).write(vals)

class TxWallet(models.Model):
    _inherit = "payment.transaction"

    @api.model
    def _e_wallet_form_get_tx_from_data(self, data):
        reference = data.get('reference')
        tx = self.env['payment.transaction'].sudo().search([('reference', '=', str(reference))])

        if not tx or len(tx) > 1:
            error_msg = _('Wallet: received data with missing reference (%s)') % (reference)
            if not tx:
                error_msg += '; no order found'
            else:
                error_msg += '; multiple order found'
            raise ValidationError(error_msg)
        return tx

    def _e_wallet_form_validate(self, data):
        self.ensure_one()
        # for order in self.sale_order_ids:
        #     if order.wallet_txn_id.state == 'done':
        #         return False
        self._set_transaction_done()
        # self._generate_and_pay_invoice()
        return True

    def render_sale_button(self, order, submit_txt=None, render_values=None):
        if order and order.wallet_debit == 0:
            return super(TxWallet, self).render_sale_button(order, submit_txt, render_values)

        values = {
            'partner_id': order.partner_shipping_id.id or order.partner_invoice_id.id,
            'billing_partner_id': order.partner_invoice_id.id,
        }
        if render_values:
            values.update(render_values)
        # Not very elegant to do that here but no choice regarding the design.
        self._log_payment_transaction_sent()
        if self.provider == 'e_wallet':
            amount_total = order.wallet_debit
        else:
            amount_total = sum(order.mapped('amount_total')) - order.wallet_debit
        return self.acquirer_id.with_context(submit_class='btn btn-primary', submit_txt=submit_txt or _('Pay Now')).sudo().render(
            self.reference,
            amount_total,
            order.pricelist_id.currency_id.id,
            values=values,
        )

    def _check_amount_and_confirm_order(self):
        self.ensure_one()
        for order in self.sale_order_ids.filtered(lambda so: so.state in ('draft', 'sent')):
            wallet_debit = order.wallet_debit
            amount_total = order.amount_total
            if wallet_debit > 0:
                if self.provider == 'e_wallet':
                    if wallet_debit == amount_total:
                        order.with_context(send_email=True).action_confirm()
                else:
                    if float_compare(self.amount, amount_total - wallet_debit, 2) == 0:
                        order.with_context(send_email=True).action_confirm()
                    else:
                        _logger.warning(
                            '<%s> transaction AMOUNT MISMATCH for order %s (ID %s): expected %r, got %r',
                            self.acquirer_id.provider,order.name, order.id,
                            amount_total, self.amount,
                        )
                        order.message_post(
                            subject=_("Amount Mismatch (%s)") % self.acquirer_id.provider,
                            body=_("The order was not confirmed despite response from the acquirer (%s): order total is %r but acquirer replied with %r.") % (
                                self.acquirer_id.provider,
                                amount_total,
                                self.amount,
                            )
                        )
            else:
                return super(TxWallet, self)._check_amount_and_confirm_order()
