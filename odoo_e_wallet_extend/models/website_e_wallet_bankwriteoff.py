# -*- coding: utf-8 -*-
import logging

from odoo import api, exceptions, fields, models
from odoo.http import request
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT
from datetime import datetime, timedelta, date

_logger = logging.getLogger(__name__)

class WebsiteEWalletBankwriteoff(models.Model):

    _name = 'website.e.wallet.bankwriteoff'
    _description = '台銀銷帳資料'

    state = fields.Selection([
        ('draft', '尚未比對'),
        ('assigned', '找不到客戶'),
        ('done', '己完成'),
        ('cancel', '己取消')], default='draft',string='銷帳狀態')

    transaction_id = fields.Many2one(comodel_name='website.transactions',string="錢包交易記錄")
    partner_id = fields.Many2one(comodel_name='res.partner', string="客戶")
    user_id = fields.Many2one('res.users', '建檔者', default=lambda self: self.env.user, index=True)
    company_id = fields.Many2one('res.company', string='銷帳api公司', default=lambda self: self.env.company)
    wallet_id = fields.Many2one(comodel_name="website.e.wallet", related="transaction_id.wallet_id",
                                         string='所屬錢包')

    name = fields.Char(string='Name')
    system = fields.Char(string='System')
    trndt = fields.Char(string='TrnDt')
    trntime = fields.Char(string='TrnTime')
    rcptid = fields.Char(string='RCPTId')
    curamt = fields.Char(string='CurAmt')
    code = fields.Char(string='Code')
    userdata = fields.Char(string='UserData')
    cname = fields.Char(string='CName')
    pname = fields.Char(string='PName')
    trntype = fields.Char(string='TrnType')
    sitdate = fields.Char(string='SITDate')
    cllbr = fields.Char(string='CLLBR')
    xml = fields.Text(string='XML')

    # 增加電子錢包交易記錄
    def action_add_website_transactions(self):
        #依虛擬帳號尋找客戶
        partner = self.env['res.partner'].sudo().search([
            ('wallet_virtualaccount', '=', self.rcptid)
        ])
        if not partner:
            self.write({'state': 'assigned'})
            return False
        #取得虛擬帳號所屬公司
        company_id = self.env['ir.property'].search([
            ('name', '=', 'wallet_virtualaccount'),
            ('value_text', '=', self.rcptid),
            ('res_id', '=', 'res.partner,' + str(partner.id))
        ]).company_id

        if company_id.id != self.company_id.id:
            raise exceptions.UserError('銷帳API公司與虛擬帳號所屬公司不同')


        # 依銷帳API傳入公司，找電子錢包
        wallet_id =  self.env['website.e.wallet'].search([('company_id','=',self.company_id.id)])
        txn_tag = wallet_id.order_debit_tag_id

        vals = {
            'txn_type' : 'credit',
            'partner_id': partner.id,
            'amount': int(self.curamt),
            'tag_ids': [(4, txn_tag.id)],
            'currency_id':  wallet_id.company_id.currency_id.id,
            'wallet_id': wallet_id.id,
            'bankwriteoff_id' : self.id
        }

        website_transaction_id = self.env['website.transactions'].sudo().create(vals)
        website_transaction_id.credit()

        self.write({
            'transaction_id': website_transaction_id,
            'partner_id': partner.id,
            'state': 'done'
        })


        return True


        # self._cr.execute('INSERT INTO website_transactions \
        #                 (state, txn_type, partner_id, amount, transaction_datetime, \
        #                     wallet_id,currency_id,bankwriteoff_id) \
        #                 VALUES (%s, %s,  %s, %s, %s, %s, %s, %s) RETURNING id', (
        #     'done',
        #     'credit',
        #     partner.id,
        #     int(self.curamt),
        #     (datetime.now()+timedelta(hours=-4)).strftime(DEFAULT_SERVER_DATETIME_FORMAT),
        #     wallet_id.id,
        #     wallet_id.company_id.currency_id.id,
        #     self.id
        # ))
        # transaction_id = self._cr.fetchone()[0]

        # transaction = request.env['website.transactions'].search([('id', '=', transaction_id)])
        # transaction.credit()

        # self.write({
        #     'transaction_id': transaction_id,
        #     'partner_id': partner.id,
        #     'state': 'done'
        # })
        #
        #
        # return True








class WebsiteTransaction(models.Model):

    _inherit = "website.transactions"

    bankwriteoff_id = fields.Many2one(comodel_name='website.e.wallet.bankwriteoff', string="Transaction Id")




