# -*- coding: utf-8 -*-
#################################################################################
# Author      : Webkul Software Pvt. Ltd. (<https://webkul.com/>)
# Copyright(c): 2015-Present Webkul Software Pvt. Ltd.
# All Rights Reserved.
#
#
#
# This program is copyright property of the author mentioned above.
# You can`t redistribute it and/or modify it.
#
#
# License URL <https://store.webkul.com/license.html/>
#################################################################################
import logging
import pprint
import werkzeug
import requests
from odoo import http, _, fields, exceptions
from odoo.http import request
from odoo.addons.website_sale.controllers.main import WebsiteSale
from odoo.addons.payment.controllers.portal import PaymentProcessing
from odoo.addons.portal.controllers.portal import CustomerPortal, pager as portal_pager, get_records_pager

_logger=logging.getLogger(__name__)

_transactions_per_page = 20

class WalletWebsiteSale(WebsiteSale):

    def _error(self, **kwargs):
        _logger.info('Wallet: Something went wrong with this transaction')
    
    def _calc_wallet_debit_amount(self):
        # This will calcualte the wallet debit amount based on sale order amount
        order = request.website.sale_get_order()
        cur_pricelist_currency_id = order.pricelist_id.currency_id
        date = fields.Date.today()
        company = request.env['res.company'].browse(request._context.get('company_id')) or request.env.company
        amount_total = order.amount_total
        wallet_id = request.env['website.e.wallet'].search([('company_id','=',request.env.user.company_id.id)])
        from_currency = wallet_id.company_id.currency_id
        cur_pricelist_partner_amount = from_currency._convert(order.partner_id.wallet_credit, cur_pricelist_currency_id,
            round = False,date= date,company= company
        )
        wallet_credit = cur_pricelist_partner_amount
        wallet_debit = wallet_credit if amount_total >= wallet_credit else amount_total
        return wallet_debit

    @http.route(["/payment/add/wallet"], type='json', auth="public", methods=['POST'], website=True)
    def payment_add_wallet(self, add_wallet, **kw):
        wallet_debit, values = 0, {}
        order = request.website.sale_get_order()

        if add_wallet:
            wallet_debit = self._calc_wallet_debit_amount()
        order.write(dict(wallet_debit = wallet_debit))

        cur_pricelist_currency_id = order.pricelist_id.currency_id
        amount_total = order.amount_total

        values.update({
            'wallet_debit': wallet_debit,
            'symbol': cur_pricelist_currency_id.symbol,
            'position': cur_pricelist_currency_id.position,
            'total': amount_total - wallet_debit,
            'amount_total': amount_total,
            'total_amount_template': request.env['ir.ui.view'].render_template('odoo_e_wallet.wk_wallet_amount_total', {
                'amount': amount_total - wallet_debit,
                'currency_id': cur_pricelist_currency_id
            }),
            'wallet_total_template': request.env['ir.ui.view'].render_template('odoo_e_wallet.wk_wallet_amount', {
                'wallet_amount': wallet_debit,
                'currency_id': cur_pricelist_currency_id
            }),
            'used_wallet_amount_template': request.env['ir.ui.view'].render_template('odoo_e_wallet.wk_wallet_used_amount', {
                'wallet_bal': wallet_debit,
                'currency_id': cur_pricelist_currency_id
            })
        })

        return values

    @http.route(['/shop/payment'], type='http', auth="public", website=True)
    def payment(self, **post):
        res = super(WalletWebsiteSale, self).payment(**post)
        wallet_id = request.env['website.e.wallet'].search([('company_id','=',request.env.user.company_id.id)])
        is_wallet_active = True if wallet_id else False
        show_wallet = False
        website_sale_order = request.website.sale_get_order()
        if website_sale_order and is_wallet_active:
            if website_sale_order.partner_id.wallet_credit > 0:
                show_wallet = True
            if website_sale_order.wallet_debit > 0:#initally we set wallet debit amount on cart to 0
                website_sale_order.wallet_debit = 0
        res.qcontext.update({
            'show_wallet' : show_wallet,
            'is_wallet_active' : is_wallet_active,
        })
        return res

    def _create_wallet_transaction(self, order):
        wallet_id = request.env['website.e.wallet'].search([('company_id','=',request.env.user.company_id.id)])
        txn_tag = wallet_id.order_debit_tag_id
        vals = {
            'txn_type': 'debit',
            'partner_id': order.partner_id.id,
            'reference': 'sale_order',
            'amount': order.wallet_debit,
            'tag_ids': [(4,txn_tag.id)],
            'currency_id': order.currency_id.id,
            'sale_order_id': order.id,
            'sale_order_line_ids': [(6,0,order.order_line.ids)],
            'wallet_id': wallet_id.id
        }
        website_transaction_id = request.env['website.transactions'].sudo().create(vals)
        order.wallet_txn_id = website_transaction_id
        return True

    @http.route(['/shop/payment/transaction/',
        '/shop/payment/transaction/<int:so_id>',
        '/shop/payment/transaction/<int:so_id>/<string:access_token>'], type='json', auth="public", website=True)
    def payment_transaction(self, acquirer_id, save_token=False, so_id=None, access_token=None, token=None, **kwargs):
        order = request.website.sale_get_order()
        #If in-consistency occur during payment
        if request.website.sudo().is_wallet_active():
            if order:
                if order.wallet_debit > 0 and (order.amount_total - order.wallet_debit < 0):
                    self._error()
                    return False
                wallet_debit = self._calc_wallet_debit_amount()
                if order.wallet_debit > 0 and (round(order.wallet_debit, 2) != round(wallet_debit, 2)):
                    self._error()
                    return False
                
        if order.wallet_debit > 0 and (order.amount_total - order.wallet_debit) == 0:
            acquirer_id = request.env.ref('odoo_e_wallet.payment_acquirer_wallet').id
            res = super(WalletWebsiteSale,self).payment_transaction(
                acquirer_id=acquirer_id,
                save_token=save_token,
                so_id=so_id,
                access_token=access_token,
                token=token,
                **kwargs
            )
            ###
            self._create_wallet_transaction(order)
        else:
            if order.wallet_debit > 0:
                transaction = order._create_custom_wallet_transation()
                self._create_wallet_transaction(order)
                #
                # last_tx_id = request.session.get('__website_sale_last_tx_id')
                # last_tx = request.env['payment.transaction'].browse(last_tx_id).sudo().exists()
                # if last_tx:
                #     PaymentProcessing.remove_payment_transaction(last_tx)
                # PaymentProcessing.add_payment_transaction(transaction)
                # request.session['__website_sale_last_tx_id'] = transaction.id
                render = transaction.render_sale_button(order)
            
            # Security Check
            if not order.wallet_debit > 0:
                wallet_acquirer_id = request.env.ref('odoo_e_wallet.payment_acquirer_wallet').id
                if wallet_acquirer_id == acquirer_id:
                    return False
                

            res = super(WalletWebsiteSale,self).payment_transaction(
                acquirer_id=acquirer_id, save_token=save_token, so_id=so_id, access_token=access_token, token=token, **kwargs
            )
        return res

    @http.route()
    def payment_token(self, pm_id=None, **kwargs):
        """ Method that handles payment using saved tokens
        :param int pm_id: id of the payment.token that we want to use to pay.
        """
        order = request.website.sale_get_order()
        if not order:
            return request.redirect('/shop/?error=no_order')

        if order and order.wallet_debit > 0:
            transaction = order._create_custom_wallet_transation()
            ###
            self._create_wallet_transaction(order)
            
        return super(WalletWebsiteSale, self).payment_token(pm_id, **kwargs)


    @http.route(['/shop/confirmation'], type='http', auth="public", website=True)
    def payment_confirmation(self, **post):
        # sale_order_session = request.session.get('sale_last_order_id')#fix for multi browser
        # sale_order_id = request.env['sale.order'].browse([sale_order_id])
        res = super(WalletWebsiteSale, self).payment_confirmation(**post)
        if res:
            sale_order = res.qcontext.get('order')
            if not sale_order:
                return request.redirect('/shop')
            if sale_order and request.website.sudo().is_wallet_active() and sale_order.wallet_debit > 0:
                #Done the last transaction by wallet acq.
                transaction_ids = sale_order.transaction_ids.filtered(lambda t: t.acquirer_id.provider == 'e_wallet')
                if transaction_ids:
                    transaction_id = max(transaction_ids)#get the last wallet transaction
                    if transaction_id.state == 'draft':
                        transaction_id._set_transaction_done()
                        transaction_id._reconcile_after_transaction_done()
                        transaction_id._log_payment_transaction_received()
                        transaction_id.write({'is_processed': True})

                # response= request.env['website.transactions'].create_transaction(sale_order,'debit','sale_order')
                sale_order.wallet_txn_id.debit()
                request.session.update({'sale_order_status':sale_order.state})
        return res

    def _prepare_wallet_transactions(self,only_count=False):
        partner = request.env.user.partner_id
        if not only_count:
            partner_transactions = request.env['website.transactions'].search([('partner_id','=',partner.id)])
            return partner_transactions
        else:
            partner_transactions_count = request.env['website.transactions'].search_count([('partner_id','=',partner.id)])
            return partner_transactions_count

    @http.route(['/main/wallet','/main/wallet/page/<int:page>'], type="http", auth="public", website=True)
    def render_wallet_transactions(self, page=1, date_begin=None, date_end=None, sortby=None, selection=None, search=None, **kw):
        if request.env.user._is_public():
            return request.redirect('/web/login')
        values = {}
        partner = request.env.user.partner_id
        wallet_transaction_count = self._prepare_wallet_transactions(True)
        wallet_id = request.env['website.e.wallet'].search([('company_id','=',request.env.user.company_id.id)])
        domain = [('partner_id','=',partner.id),('wallet_id','=',wallet_id.id),('state','!=','draft')]
        wallet_searchbar_sorting = {
            'date': {'label': _('Date'), 'order': 'transaction_datetime desc'},
            'type': {'label': _('Credit/Debit'), 'order': 'txn_type'},
            'currency': {'label': _('Currency'), 'order': 'currency_id'},
            'state': {'label': _('State'), 'order': 'state'},
            'wallet': {'label': _('Wallet'), 'order': 'wallet_id'},
        }
        if not sortby:
            sortby = 'date'
        sort_order = wallet_searchbar_sorting[sortby]['order']
        if date_begin and date_end:
            domain += [('create_date', '>', date_begin), ('create_date', '<=', date_end)]

        if selection == 'all':
            domain = [('partner_id','=',partner.id),('state','!=','draft')]
        elif search == None:
            pass
        elif selection and search:
            if selection == 'transaction_id':
                domain += [('transaction_id','=',search)]
            if selection == 'sale_order':
                domain += [('sale_order_id','=',search)]

        pager = portal_pager(
            url="/main/wallet",
            url_args={'date_begin': date_begin, 'date_end': date_end, 'sortby': sortby},
            total=wallet_transaction_count,
            page=page,
            step=_transactions_per_page
        )
        wallet_transaction_values = request.env['website.transactions'].search(domain, limit=_transactions_per_page, offset=pager['offset'], order=sort_order)
        amount_total = request.env.user.partner_id.wallet_credit
        values.update({
                'pager':pager,
                'wallet_transaction_ids': wallet_transaction_values,
                'sortby': sortby,
                'searchbar_sortings': wallet_searchbar_sorting,
                'date': date_begin,
                'default_url': '/main/wallet',
                'selection': selection,
                'search':search,
                'show_transactions': request.website.sudo().is_transactions_active(),
                'amount_total' : amount_total,
                'wallet': wallet_id
        })
        return request.render("odoo_e_wallet.main_wallet", values)

    @http.route('/wallet/check/status', type="json", auth="public", methods=['POST'], website=True)
    def checkstatus(self, is_checked):
        # Check for duplicate payment tabs.
        # We need to reset the old payment tab if a new payment tab i open with updated values
        vals = {
            'is_safe': True
        }
        if is_checked:
            order = request.website.sale_get_order()
            if order.wallet_debit == 0:
                vals['is_safe'] = False

        return vals


class WalletController(http.Controller):
    _accept_url = '/payment/wallet/feedback'

    @http.route([
        '/payment/wallet/feedback',
    ], type='http', auth='public', csrf=False)
    def wallet_form_feedback(self, **post):
        _logger.info('Beginning form_feedback with post data %s', pprint.pformat(post))
        request.env['payment.transaction'].sudo().form_feedback(post, 'e_wallet')
        return werkzeug.utils.redirect(post.get('return_url'))
