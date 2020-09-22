# -*- coding: utf-8 -*-
#################################################################################
# Author      : kuilus
#################################################################################
{
    "name"                 :  "Website e Wallet Extend",
    "summary"              :  "擴展ODOO Website Wallet",
    "category"             :  "Website",
    "author"               :  "kulius",
    "version"              :  "1.0.0",
    "sequence"             :  1,
    "depends"              :  [ 'base', 'mail',
                                'odoo_e_wallet',
                                'website_sale_management',
                                'website_sale_delivery',
                            ],
    "description"          :  """
                            擴充ODOO Website Wallet
                            1.增加客戶虛擬帳號(台銀規則)
                            2.於網站呈現個人虛擬帳號
                            """,
    "data"                 :  [
                                'data/demo.xml',
                                'views/res_config_setting_view.xml',
                                'views/inherit_res_partner.xml',
                                'views/inherit_portal_my_home.xml',
                                'views/website_e_wallet_bankwriteoff.xml',
                                'views/inherit_odoo_e_wallet.xml',
                               # 'views/odoo_e_wallet_sequence.xml',
                               # 'views/inherit_res_partner.xml',
                               # 'views/inherit_sale_view_order_form.xml',
                               # 'views/odoo_e_wallet_email_template.xml',
                               # 'security/access_control_security.xml',
                                'security/ir.model.access.csv',
                               # 'views/template.xml',
                               # 'demo/data.xml',
                              ],
    "images"               :  ['static/description/Banner.png'],
    "application"          :  True,
    "installable"          :  True,
}