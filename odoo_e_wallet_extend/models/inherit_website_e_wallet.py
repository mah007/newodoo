# -*- coding: utf-8 -*-
import logging

from odoo import api, exceptions, fields, models
from odoo.http import request


_logger = logging.getLogger(__name__)


class WebsiteTransaction(models.Model):

    _inherit = "website.transactions"

    @api.model
    def create(self, vals):
        vals['transaction_id'] = self.env['ir.sequence'].sudo().next_by_code('website.transactions.sequence')
        if vals.get('txn_type') == 'debit' and vals.get('reference') == 'manual' and vals.get('amount') > self.env['res.partner'].browse([vals.get('partner_id')]).wallet_credit:
            raise exceptions.UserError('User "{}" have only {:.2f} amount in current wallet'.format(self.env['res.partner'].browse([vals.get('partner_id')]).name,self.env['res.partner'].browse([vals.get('partner_id')]).wallet_credit))
        if vals.get('amount') <= 0:
            raise exceptions.UserError('Please insert a valid amount')
        if not vals.get('wallet_id'):
            raise exceptions.UserError('請設定好電子錢包')
        else:
            wallet_id = self.env['website.e.wallet'].sudo().search([('id', '=', vals.get('wallet_id'))])
            if vals.get('txn_type') == 'credit' and vals.get('reference') != 'sale_order':
                vals['currency_id'] = wallet_id.company_id.currency_id.id
            if vals.get('txn_type') == 'debit' and vals.get('reference') == 'manual':
                vals['currency_id'] = wallet_id.company_id.currency_id.id

        if not vals.get('currency_id'):
            raise exceptions.UserError('請設定交易所屬貨幣')

        res = super(models.Model,self).create(vals)
        return res

    @api.onchange('partner_id')
    def set_wallet(self):
        if self.partner_id:
            user = self.env['res.users'].search([('partner_id','=',self.partner_id.id)])
            #改為直接讀取環境的公司別
            wallet= self.env['website.e.wallet'].search([('company_id','=',self.env.company.id)])
            if not user.company_id:
                raise exceptions.UserError('該客戶並不是網站使用者')
            if not wallet:
                raise exceptions.UserError('There is no wallet related to this user\'s company')
            self.wallet_id = wallet.id
            self.currency_id = self.wallet_id.company_id.currency_id.id

    #多公司下email會出錯，有時間再找
    def send_credit_mail(self):
        # self.ensure_one()
        # template_id=self.env.ref('odoo_e_wallet.website_wallet_mail_credit_template')
        # template_id.send_mail(self.id, force_send=True)
        return True

    # 多公司下email會出錯，有時間再找
    def send_debit_mail(self):
        # self.ensure_one()
        # template_id=self.env.ref('odoo_e_wallet.website_wallet_mail_debit_template')
        # template_id.send_mail(self.id, force_send=True)
        return True

    # 多公司下email會出錯，有時間再找
    def send_manual_debit_mail(self):
        # self.ensure_one()
        # template_id=self.env.ref('odoo_e_wallet.website_wallet_mail_manual_debit_template')
        # template_id.send_mail(self.id, force_send=True)
        return True

class Website(models.Model):

    _inherit = 'website'

    def get_wallet_virtualaccount(self,partner=None):
        if partner:
            rec = self.env['res.partner'].sudo().search([('id','=',partner.id)])
            for r in rec:
                return r.wallet_virtualaccount
        else:
            return '尚未建立虛擬帳號'

        return True

    def get_wallet_details(self,partner=None,amount=False):
        if partner:
            # 取得呼叫者的當前公司，後台及前端網站可共用
            allowed_company_ids = self.env.context.get('allowed_company_ids', [])
            companyid = allowed_company_ids[0]
            count = 0
            wallet_id = request.env['website.e.wallet'].search([('company_id','=',companyid)])
            if wallet_id:
                rec = self.env['website.transactions'].search([('partner_id','=',partner.id),('wallet_id','=',wallet_id.id),('state','!=','draft')])
                for r in rec:
                    if not(r.txn_type == 'credit' and r.state == 'cancelled'):
                        count = count + 1;
                return count
            else:
                return 0
        if amount:
            return self.env.user.partner_id.wallet_credit
        return True if self.env.user.partner_id.wallet_credit > 0 or not request.session['sale_order_id'] else False

    @api.model
    def is_wallet_active(self):
        # 取得呼叫者的當前公司，後台及前端網站可共用
        allowed_company_ids = self.env.context.get('allowed_company_ids', [])
        companyid = allowed_company_ids[0]
        active = self.env['website.e.wallet'].search([('company_id','=',companyid)]).active
        if active:#if wallet is active
            return True
        return False

    @api.model
    def _get_current_wallet(self):
        # 取得呼叫者的當前公司，後台及前端網站可共用
        allowed_company_ids = self.env.context.get('allowed_company_ids', [])
        companyid = allowed_company_ids[0]
        wallet_id = self.env['website.e.wallet'].search([('company_id','=',companyid)])
        return wallet_id or False

    @api.model
    def is_transactions_active(self):
        # 取得呼叫者的當前公司，後台及前端網站可共用
        allowed_company_ids = self.env.context.get('allowed_company_ids', [])
        companyid = allowed_company_ids[0]
        show_transactions = self.env['website.e.wallet'].search([('company_id','=',companyid)]).show_transactions
        if show_transactions:
            return True
        return False

    def get_users_currency(self, partner_id):
        # 取得呼叫者的當前公司，後台及前端網站可共用
        allowed_company_ids = self.env.context.get('allowed_company_ids', [])
        companyid = allowed_company_ids[0]
        wallet_id =  self.env['website.e.wallet'].search([('company_id','=',companyid)])
        return wallet_id.company_id.currency_id

