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
# You should have received a copy of the License along with this program.
# If not, see <https://store.webkul.com/license.html/>
#################################################################################
{
    "name"                 :  "Website e Wallet",
    "summary"              :  "ODOO Website Wallet : Allow user to store credit in you website using  wallet and pay using store credit in wallet.",
    "category"             :  "Website",
    "author"               :  "Webkul Software Pvt. Ltd.",
    "version"              :  "2.0.1",
    "sequence"             :  1,
    "depends"              :  [
                                'website_sale_management',
                                'website_sale_delivery',
                            ],
    "website"              :  "https://store.webkul.com/Odoo-Website-Wallet.html",
    "description"          :  """ODOO Website Wallet : Allow user to store credit in you website using  wallet and pay using store credit in wallet.""",
    "live_test_url"        :  "http://odoodemo.webkul.com/?module=odoo_e_wallet&version=12.0",
    "data"                 :  [
                               'views/odoo_e_wallet.xml',
                               'views/odoo_e_wallet_sequence.xml',
                               'views/inherit_res_partner.xml',
                               'views/inherit_sale_view_order_form.xml',
                               'views/odoo_e_wallet_email_template.xml',
                               'security/access_control_security.xml',
                               'security/ir.model.access.csv',
                               'views/template.xml',
                               'demo/data.xml',
                              ],
    'demo'                 :  ['demo/demo.xml'],
    "images"               :  ['static/description/Banner.png'],
    "application"          :  True,
    "installable"          :  True,
    "price"                :  199,
    "currency"             :  "EUR",
}