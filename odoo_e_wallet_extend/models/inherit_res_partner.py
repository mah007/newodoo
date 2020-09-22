# -*- coding: utf-8 -*-

from odoo import api, exceptions, fields, models,SUPERUSER_ID, _, tools
from odoo.exceptions import ValidationError, UserError

import logging
_logger =  logging.getLogger(__name__)

class ResPartner(models.Model):
    _inherit = "res.partner"

    wallet_virtualaccount = fields.Char(string='台銀虛擬帳號', company_dependent=True, check_company=True)

    @api.model
    def create(self, vals):
        res = super(ResPartner, self).create(vals)
        self.update_virtualaccount(res.id)
        return res


    #判斷該客戶在各公司是否有虛擬帳號，若無則新增，若有則更新
    def update_virtualaccount(self,partner_id):
        #取得最高權限，不然無法在ir.property新增
        env = api.Environment(self.env.cr, SUPERUSER_ID, {})

        company_ids = env['res.company'].search([])
        for company_id in company_ids:
            #判斷公司有無設定 代收類別
            if company_id.e_wallet_virtualaccount_type:
                #判斷在不同公司下,該客戶是否有虛擬帳號
                properties = env['ir.property'].search([
                    ('name', '=', 'wallet_virtualaccount'),
                    ('res_id', '=', 'res.partner,' + str(partner_id)),
                    ('company_id', '=', company_id.id)])

                vals = {
                    'name': 'wallet_virtualaccount',
                    'fields_id': env['ir.model.fields'].search([
                        ('name', '=', 'wallet_virtualaccount'),
                        ('model', '=', 'res.partner')], limit=1).id,
                    'company_id': company_id.id,
                    'res_id': 'res.partner,' + str(partner_id),
                    'value_text': self._gen_virtualaccount(company_id.e_wallet_virtualaccount_type, partner_id),
                    'type': 'char'
                }
                # 若無則create，若有則write
                if properties:
                    properties.write(vals)
                else:
                    env['ir.property'].create(vals)



    #虛擬帳號產生
    def _gen_virtualaccount(self,bank_type,custom_id):
        s = "%07d" % custom_id
        return bank_type + s + '1'

    #原生錢包，多公司有問題，計算錢包餘額
    def _calculate_wallet_balance(self):
        # if self.env.context.get('website_id'):
        #     companyid = self.env['website'].browse(self.env.context['website_id']).company_id.id
        # else:

        #取得呼叫者的當前公司，後台及前端網站可共用
        allowed_company_ids = self.env.context.get('allowed_company_ids', [])
        companyid=allowed_company_ids[0]

        wallet_id =  self.env['website.e.wallet'].search([('company_id','=',companyid)])
        for rec in self:
            credit_balance = self.env['website.transactions'].search([('partner_id','=',rec.id),
                                                            ('txn_type','=','credit'),
                                                            ('state','=','done'),
                                                            ('wallet_id','=',wallet_id.id)])
            debit_balance = self.env['website.transactions'].search([('partner_id','=',rec.id),
                                                            ('txn_type','=','debit'),
                                                            ('state','=','done'),
                                                            ('wallet_id','=',wallet_id.id)])

            rec.wallet_credit = sum(credit_balance.mapped('total_amount'))-sum(debit_balance.mapped('total_amount'))


    # @api.depends('name')
    # def gen_wallet_virtualaccount(self):
    #     virtualaccount = self.env['ir.property'].get('property_account_receivable_id', 'res.partner')
    #     raise UserError(_('%s invalid recipients') % virtualaccount)
        # for rec in self:
        #     if rec.id:
        #         s = "%07d" % rec.id
        #         if self.env.user.company_id.e_wallet_virtualaccount_type:
        #             rec.wallet_virtualaccount = self.env.user.company_id.e_wallet_virtualaccount_type + s + '1'

                # companies = self.env['res.company'].search([])
                # for company in companies:
                #     partner=self.env['res.partner'].search([('company_id', '=', company.id), ('id', '=', rec.id)], limit=1)
                #
                #     if company.e_wallet_virtualaccount_type:
                #         partner.wallet_virtualaccount = company.e_wallet_virtualaccount_type + s + '1'
                #     else:
                #         rec.wallet_virtualaccount = '000000' + s + '1'