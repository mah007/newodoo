# -*- coding: utf-8 -*-
{
    'name': "construction",

    'summary': """
        construction management system  """,

    'description': """
        construction management system  
    """,

    'author': "Expert",
    'website': "http://www.expert-mep.org",


    'category': 'construction',
    'version': '1.0',

    # any module necessary for this one to work correctly
    'depends': ['base','project','purchase','sale'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
