# -*- coding: utf-8 -*-
##########################################################################
#
#    Copyright (c) 2015-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>)
#
##########################################################################
import logging

from odoo import api, exceptions, fields, models
from odoo.http import request

_logger = logging.getLogger(__name__)

class WebsiteEWallet(models.Model):

    _name = 'website.e.wallet'
    _description = 'website e wallet model'

    active = fields.Boolean(
        string='Active',
        default=True
    )
    show_transactions = fields.Boolean(
        string="Show Transactions",
        default=False
    )
    name = fields.Char(
        string='Name',
        required=True
    )
    company_id = fields.Many2one(
        'res.company'
    )
    order_debit_tag_id  = fields.Many2one(comodel_name="website.transaction.tags",
        string=  'Website Debit Tag',
        help=  'Default Sale Order Transaction Tag',
        default = lambda self: self.env['website.transaction.tags'].search([],limit=1),
        required = True,
        ondelete='cascade',
    )
    wallet_transaction_ids = fields.One2many(comodel_name="website.transactions",inverse_name="wallet_id",string="E-Wallet Transactions")

    order_cancelled_tag = fields.Many2one(comodel_name="website.transaction.tags",
        string=  'Cancelled Sale Order Tag',
        help=  'Default Cancelled Sale Order Wallet Money Tag',
        default = lambda self: self.env['website.transaction.tags'].search([],limit=1),
        required = True,
        ondelete='cascade',
    )
    image = fields.Binary(string="Wallet Image")

    @api.model
    def create(self,vals):
        company_ids = self.env['website.e.wallet'].search([])
        if vals.get('company_id') in company_ids.ids:
            raise exceptions.UserError('Selected company already have a wallet, Only one wallet is allowed to a company')
        res = super(WebsiteEWallet, self).create(vals)
        return res

    def write(self,vals):
        company_ids = self.env['website.e.wallet'].search([])
        if vals.get('company_id') in company_ids.ids:
            raise exceptions.UserError('Selected company already have a wallet, Only one wallet is allowed to a company')
        res = super(WebsiteEWallet, self).write(vals)
        return res

    def unlink(self):
        raise exceptions.UserError('You can only deactivate the wallet!')

class WebsiteWalletTags(models.Model):

    _name = "website.transaction.tags"
    _description = 'website transaction tags model'

    name = fields.Char(required=1)
    txn_type = fields.Selection([('credit','Credit'),('debit','Debit')],string="Type",required=True)
    active = fields.Boolean(default=True)


class WebsiteTransaction(models.Model):

    _name = "website.transactions"
    _description = 'website transactions model'
    _rec_name = "transaction_id"
    _inherit = ['mail.thread']
    _order = "transaction_id desc"

    state = fields.Selection([('draft','Draft'),('done','Done'),('error','Error'),('cancelled','Cancelled'),('refunded','Refunded')],default="draft",track_visibility="onchange")

    transaction_id = fields.Char(string="Transaction Id",readonly=1)

    txn_type = fields.Selection([('credit','Credit'),('debit','Debit')],default="credit",string = "Type",required=True,track_visibility="onchange")
    partner_id = fields.Many2one(comodel_name='res.partner',string="Customer",track_visibility="always",required=True)
    reference = fields.Selection([('manual','Manual'),('sale_order','Sale Order')],default="manual")
    amount = fields.Float(track_visibility="always",required=True,string="E-Wallet Amount")
    total_amount = fields.Float("Total Converted Amount",compute="_get_amount_total",help="Display the converted amount from the currency used for transaction to the current wallet company currency",track_visibility="always")
    tag_ids = fields.Many2many(comodel_name="website.transaction.tags", required=True,ondelete='cascade')
    currency_id = fields.Many2one(comodel_name="res.currency",track_visibility="always")
    sale_order_line_ids = fields.One2many(comodel_name="sale.order.line", inverse_name="wallet_transaction_id")
    sale_order_id = fields.Many2one(comodel_name="sale.order")
    transaction_datetime = fields.Datetime(string='Transaction Date', required=True, readonly=True, index=True, states={'draft': [('readonly', False)], 'sent': [('readonly', False)]}, copy=False, default=fields.Datetime.now)
    wallet_id = fields.Many2one(comodel_name="website.e.wallet",string="E-Wallet",required=True,track_visibility="always")
    wallet_currency_id = fields.Many2one(comodel_name="res.currency",related="wallet_id.company_id.currency_id",string='wallet currency id')

    @api.model
    def create(self,vals):
        vals['transaction_id'] = self.env['ir.sequence'].sudo().next_by_code('website.transactions.sequence')
        if vals.get('txn_type') == 'debit' and vals.get('reference') == 'manual' and vals.get('amount') > self.env['res.partner'].browse([vals.get('partner_id')]).wallet_credit:
            raise exceptions.UserError('User "{}" have only {:.2f} amount in current wallet'.format(self.env['res.partner'].browse([vals.get('partner_id')]).name,self.env['res.partner'].browse([vals.get('partner_id')]).wallet_credit))
        if vals.get('amount') <= 0:
            raise exceptions.UserError('Please insert a valid amount')
        partner_obj = self.env['res.partner']
        wallet_obj = self.env['website.e.wallet']
        partner_id = partner_obj.browse([vals.get('partner_id')])
        user = self.env['res.users'].search([('partner_id','=',partner_id.id)])
        wallet_id = wallet_obj.search([('company_id','=',user.company_id.id)])
        if wallet_id:
            vals['wallet_id'] = wallet_id.id
        else:
            vals['wallet_id'] = wallet_obj.search([]).id
        if vals.get('txn_type') == 'credit' and vals.get('reference') != 'sale_order':
            vals['currency_id'] = wallet_id.company_id.currency_id.id
        if vals.get('txn_type') == 'debit' and vals.get('reference') == 'manual':
            vals['currency_id'] = wallet_id.company_id.currency_id.id
        rec_id = super(WebsiteTransaction,self).create(vals)
        return rec_id

    def credit(self):
        self.ensure_one()
        if self.state not in ['done']:#security, loop hole through inspecting in the backend
            self.state = 'done'
            self.send_credit_mail()

    def debit(self):
        self.ensure_one()
        if self.state not in ['done']:#security, loop hole through inspecting in the backend
            self.state = 'done'
            self.send_manual_debit_mail()

    def unlink(self):
        for rec in self:
            if rec.txn_type == 'credit':
                if rec.state != 'done':
                    return super(WebsiteTransaction, self).unlink()
                else:
                    raise exceptions.UserError('The log for successful transaction can not be deleted.')
            else:
                raise exceptions.UserError('The log for successful transaction can not be deleted.')

    def cancel(self):
        if self.state not in ['cancelled']:#security, loop hole through inspecting in the backend
            self.ensure_one()
            self.state = 'cancelled'

    def refund(self):
        if self.state not in ['cancelled']:#security, loop hole through inspecting in the backend
            self.ensure_one()
            self.state = 'refunded'

    def draft(self):
        self.ensure_one()
        self.state = 'draft'

    @api.onchange('txn_type')
    def change_tag(self):
        if self.txn_type == 'credit':
            # self.reference = 'manual'
            self.tag_ids = None
        else:
            self.tag_ids = None
            # self.reference = 'sale_order'
        return {
            'domain' : {'tag_ids' : [('txn_type','=',self.txn_type)] }
        }

    @api.onchange('partner_id')
    def set_wallet(self):
        if self.partner_id:
            user = self.env['res.users'].search([('partner_id','=',self.partner_id.id)])
            wallet= self.env['website.e.wallet'].search([('company_id','=',user.company_id.id)])
            if not user.company_id:
                raise exceptions.UserError('This customer currently is not a website user')
            if not wallet:
                raise exceptions.UserError('There is no wallet related to this user\'s company')
            self.wallet_id = wallet.id
            self.currency_id = self.wallet_id.company_id.currency_id.id

    def send_credit_mail(self):
        self.ensure_one()
        template_id=self.env.ref('odoo_e_wallet.website_wallet_mail_credit_template')
        template_id.send_mail(self.id, force_send=True)
        return True

    def send_debit_mail(self):
        self.ensure_one()
        template_id=self.env.ref('odoo_e_wallet.website_wallet_mail_debit_template')
        template_id.send_mail(self.id, force_send=True)
        return True

    def send_manual_debit_mail(self):
        self.ensure_one()
        template_id=self.env.ref('odoo_e_wallet.website_wallet_mail_manual_debit_template')
        template_id.send_mail(self.id, force_send=True)
        return True

    def _get_amount_total(self):
        for rec in self:
            date = rec._context.get('date') or fields.Date.today()
            company = rec.env['res.company'].browse(rec._context.get('company_id')) or rec.env.company
            # currency_id = rec.env.user.company_id.currency_id
            currency_id = rec.wallet_id.company_id.currency_id
            rec.total_amount = rec.currency_id._convert(
                rec.amount,currency_id,round = False, date= date, company= company
            )

    def create_transaction(self,sale_order,txn_type,reference):
        wallet_id =  self.env['website.e.wallet'].search([('company_id','=',self.env.user.company_id.id)])
        txn_tag = wallet_id.order_debit_tag_id
        # if not txn_tag:
        #     txn_tag = self.env['website.transaction.tags'].search([('txn_type','=','debit')],limit=1)
        if not sale_order.wallet_txn_id:
            vals = {
                'txn_type': txn_type,
                'partner_id': sale_order.partner_id.id,
                'reference': reference,
                'amount': sale_order.wallet_debit,
                'tag_ids': [(4,txn_tag.id)],
                'currency_id': sale_order.currency_id.id,
                'sale_order_id': sale_order.id,
                'sale_order_line_ids': [(6,0,sale_order.order_line.ids)],
                'wallet_id': wallet_id.id
            }

            website_transaction_id = self.sudo().create(vals)
            sale_order.write({
                'wallet_txn_id': website_transaction_id.id,
            })
            website_transaction_id.debit()
        return True

    def sale_order_view(self):
        res_id = self.env['sale.order'].search([('id','=',self.sale_order_id.id)])
        res = {
            'name': 'Sale Order',
            'view_id': self.env.ref('sale.view_order_form').id,
            'res_model': 'sale.order',
            'res_id': res_id.id,
            'view_mode': 'form',
            'type': 'ir.actions.act_window',
            'domain': [('partner_id','=',self.partner_id.id)]
        }
        return res


class ResPartner(models.Model):
    _inherit = "res.partner"

    wallet_credit = fields.Float("Wallet balance",compute='_calculate_wallet_balance')

    def _calculate_wallet_balance(self):
        wallet_id =  self.env['website.e.wallet'].search([('company_id','=',self.env.user.company_id.id)])
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


    # def open_related_view(self,context=None):
    #     return {
    #          'name' : 'Customer Transactions',
    #          'type': 'ir.actions.act_window',
    #          'res_model': 'website.transactions',
    #          'view_mode': 'tree',
    #          'view_type': 'tree,form',
    #          'view_id': self.env.ref('odoo_e_wallet.transaction_histroy_view_tree').id,
    #          'domain':[('partner_id','=',self.id)]
    #     }

class website(models.Model):

    _inherit = 'website'

    @api.model
    def get_login_partner(self):
        return self.env['res.partner'].sudo().search([('user_ids', '=', request.uid)])

    def get_wallet_details(self,partner=None,amount=False):
        if partner:
            count = 0
            wallet_id = request.env['website.e.wallet'].search([('company_id','=',request.env.user.company_id.id)])
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
        active = self.env['website.e.wallet'].search([('company_id','=',self.env.user.company_id.id)]).active
        if active:#if wallet is active
            return True
        return False

    @api.model
    def _get_current_wallet(self):
        wallet_id = self.env['website.e.wallet'].search([('company_id','=',self.env.user.company_id.id)])
        return wallet_id or False

    @api.model
    def is_transactions_active(self):
        show_transactions = self.env['website.e.wallet'].search([('company_id','=',self.env.user.company_id.id)]).show_transactions
        if show_transactions:
            return True
        return False

    def get_users_currency(self, partner_id):
        wallet_id =  self.env['website.e.wallet'].search([('company_id','=',request.env.user.company_id.id)])
        return wallet_id.company_id.currency_id
