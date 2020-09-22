# -*- coding: utf-8 -*-
import logging
import pprint
import werkzeug
import requests
from odoo import http, _, fields, exceptions
from odoo.http import request
from odoo.addons.odoo_e_wallet.controller.main import WalletWebsiteSale
from odoo.addons.payment.controllers.portal import PaymentProcessing
from odoo.addons.portal.controllers.portal import CustomerPortal, pager as portal_pager, get_records_pager


_logger=logging.getLogger(__name__)

_transactions_per_page = 20

class Extension(WalletWebsiteSale):

    #依訂單建立電子錢包交易記錄時，公司別取得鏌誤
    def _create_wallet_transaction(self, order):
        #改為 request.website.company_id.id
        wallet_id = request.env['website.e.wallet'].sudo().search([('company_id','=',request.website.company_id.id)])
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

    #依電子錢包貸幣，將訂單金額轉換
    def _calc_wallet_debit_amount(self):
        # This will calcualte the wallet debit amount based on sale order amount
        order = request.website.sale_get_order()
        cur_pricelist_currency_id = order.pricelist_id.currency_id
        date = fields.Date.today()
        company = request.env['res.company'].browse(request._context.get('company_id')) or request.env.company
        amount_total = order.amount_total
        #加上sudo不然取得會出錯
        wallet_id = request.env['website.e.wallet'].sudo().search([('company_id','=',request.env.user.company_id.id)])
        from_currency = wallet_id.company_id.currency_id
        cur_pricelist_partner_amount = from_currency._convert(order.partner_id.wallet_credit, cur_pricelist_currency_id,
            round = False,date= date,company= company
        )
        wallet_credit = cur_pricelist_partner_amount
        #wallet_credit = order.partner_id.wallet_credit
        wallet_debit = wallet_credit if amount_total >= wallet_credit else amount_total
        return wallet_debit

    #呈現電子錢包資訊時，取得正確公司別
    @http.route()
    def render_wallet_transactions(self, page=1, date_begin=None, date_end=None, sortby=None, selection=None, search=None, **kw):
        if request.env.user._is_public():
            return request.redirect('/web/login')
        values = {}
        partner = request.env.user.partner_id
        wallet_transaction_count = self._prepare_wallet_transactions(True)
        #改為 request.website.company_id.id
        wallet_id = request.env['website.e.wallet'].sudo().search([('company_id','=', request.website.company_id.id)])
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
        wallet_transaction_values = request.env['website.transactions'].sudo().search(domain, limit=_transactions_per_page, offset=pager['offset'], order=sort_order)
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

