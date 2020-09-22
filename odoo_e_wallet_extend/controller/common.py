# -*- coding: utf-8 -*-
import logging
import xml.etree.ElementTree as ET
import base64
import datetime
import json
import os
import logging
import pytz
import requests
import werkzeug.utils
import werkzeug.wrappers


from odoo import _, http, release
from odoo.http import content_disposition, dispatch_rpc, request, Response
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT
from datetime import datetime, timedelta, date
_logger = logging.getLogger(__name__)

class WalletController(http.Controller):
    # 接收台銀銷帳檔
    @http.route(['/Wallet/GetBankWriteoff','/Wallet/GetBankWriteoff/company/<int:company>'], type='http', auth="none", methods=['POST','GET'], csrf=False)
    def getbankwriteoff(self, company=1):
        body = request.httprequest.data
        restr=body.decode("big5")
        #檢查接收字串是否有錯
        totalStartTags = restr.find('<RsXMLData>')
        totalEndTags = restr.find('</RsXMLData>')

        if (not restr) or (totalEndTags == -1) or (totalStartTags != -1) :
            return '"HTTP/1.1 406 Not Acceptable"'

        tree = ET.fromstring(restr)
        bankwriteoff={}
        bankwriteoff['xml'] = restr
        bankwriteoff['state'] = 'draft'
        for elem in tree.iter():
            if elem.tag.find('System') != -1:
                bankwriteoff['system'] = elem.text
                bankwriteoff['name'] = elem.text
            if elem.tag.find('TrnDt') != -1:
                bankwriteoff['trndt'] = elem.text
            if elem.tag.find('TrnTime') != -1:
                bankwriteoff['trntime'] = elem.text
            if elem.tag.find('RCPTId') != -1:
                bankwriteoff['rcptid'] = elem.text
            if elem.tag.find('CurAmt') != -1:
                bankwriteoff['curamt'] = elem.text
            if elem.tag.find('Code') != -1:
                bankwriteoff['code'] = elem.text
            if elem.tag.find('UserData') != -1:
                bankwriteoff['userdata'] = elem.text
            if elem.tag.find('CName') != -1:
                bankwriteoff['cname'] = elem.text
            if elem.tag.find('PName') != -1:
                bankwriteoff['pname'] = elem.text
            if elem.tag.find('TrnType') != -1:
                bankwriteoff['trntype'] = elem.text
            if elem.tag.find('SITDate') != -1:
                bankwriteoff['sitdate'] = elem.text
            if elem.tag.find('CLLBR') != -1:
                bankwriteoff['cllbr'] = elem.text
        #print(bankwriteoff)
        #接受台銀銷帳使用者
        writeoff_user = request.env['ir.config_parameter'].sudo().get_param(
            'odoo_e_wallet_extend.e_wallet_writeoff_user')
        bankwriteoff['user_id'] = writeoff_user

        # 接受台銀銷帳使用者
        user_id = request.env['res.users'].search([('id', '=', writeoff_user)])
        #從傳入參數取得company_id，預設為1
        bankwriteoff['company_id'] = company

        #request.env['res.partner'].search_read([['id', 'in', partner_ids]], ['id', 'im_status'])
        bankwriteoff_id = request.env['website.e.wallet.bankwriteoff'].sudo().create(bankwriteoff)

        #若需自動銷帳
        writeoff_auto = request.env['ir.config_parameter'].sudo().get_param(
            'odoo_e_wallet_extend.e_wallet_writeoff_auto')
        if writeoff_auto:
            # 重點，force_company，指定當前公司，依虛擬帳號尋找客戶
            partner = request.env['res.partner'].sudo().with_context(force_company=company).search([
                ('wallet_virtualaccount', '=', bankwriteoff_id.rcptid)
            ])

            if not partner:
                bankwriteoff_id.write({'state': 'assigned'})
                return '成功，但找不到客戶'

            wallet_id = request.env['website.e.wallet'].search([('company_id', '=', company)])

            request.cr.execute('INSERT INTO website_transactions \
                            (transaction_id,state, txn_type, partner_id, amount, transaction_datetime, \
                                wallet_id,currency_id,bankwriteoff_id) \
                            VALUES (%s,%s, %s,  %s, %s, %s, %s, %s, %s) RETURNING id', (
                request.env['ir.sequence'].sudo().with_context(force_company=company).next_by_code('website.transactions.sequence'),
                'done',
                'credit',
                partner.id,
                int(bankwriteoff_id.curamt),
                (datetime.now()+timedelta(hours=-4)).strftime(DEFAULT_SERVER_DATETIME_FORMAT),
                wallet_id.id,
                wallet_id.company_id.currency_id.id,
                bankwriteoff_id.id
            ))
            website_transaction_id = request.cr.fetchone()[0]

            bankwriteoff_id.write({
                'transaction_id': website_transaction_id,
                'partner_id': partner.id,
                'state': 'done'
            })
            return '成功'

        #     # 依API公司，找電子錢包
        #     wallet_id =  request.env['website.e.wallet'].search([('company_id','=',company)])
        #     txn_tag = wallet_id.order_debit_tag_id
        #     vals = {
        #         'txn_type': 'credit',
        #         'partner_id': partner.id,
        #         'amount': int(bankwriteoff_id.curamt),
        #         'tag_ids': [(4, txn_tag.id)],
        #         'currency_id': wallet_id.company_id.currency_id.id,
        #         'wallet_id': wallet_id.id,
        #         'bankwriteoff_id': bankwriteoff_id.id
        #     }
        #
        #     website_transaction_id = request.env['website.transactions'].sudo().create(vals)
        #     website_transaction_id.credit()
        #
        #     bankwriteoff_id.write({
        #         'transaction_id': website_transaction_id,
        #         'partner_id': partner.id,
        #         'state': 'done'
        #     })
        #
        # return '成功'
