# -*- coding: utf-8 -*-

{
    "name": "Telegram Integration",
    "category": '',
    'summary': 'Telegram Integration .',
    "description": """ 
        Send Message from odoo to Telegram
     """,
    "author": u"Arga Dwi Ardinata",
    "website": u"",
    "version": '14.1.1',
    "depends": ['base', 'contacts', 'sale'],
    "data": [
        "security/ir.model.access.csv",

        "wizard/send_message_view.xml",
        "wizard/send_message_sale_view.xml",

        "views/partnert_view.xml",
        "views/res_company_view.xml",
        "views/sale_views.xml",
    ],
    'qweb': [],
    "installable": True,
    "application": True,
    "auto_install": False,
}
