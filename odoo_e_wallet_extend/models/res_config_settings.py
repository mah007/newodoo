
from odoo import models, fields, api


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    e_wallet_virtualaccount_type= fields.Char(string='代收類別', related='company_id.e_wallet_virtualaccount_type', readonly=False)
    e_wallet_writeoff_auto = fields.Boolean(string='是否自動銷帳',
                config_parameter='odoo_e_wallet_extend.e_wallet_writeoff_auto')
    e_wallet_writeoff_user = fields.Many2one(string='接受台銀銷帳使用者', comodel_name='res.users',
                config_parameter='odoo_e_wallet_extend.e_wallet_writeoff_user')

    #批次變更所有客戶的所有分公司虛擬帳號
    def update_partner_virtualaccount(self):
        partners = self.env['res.partner'].search([])
        for partner in partners:
            partner.update_virtualaccount(partner.id)

class ResCompany(models.Model):
    _inherit = "res.company"

    e_wallet_virtualaccount_type = fields.Char(string='代收類別')