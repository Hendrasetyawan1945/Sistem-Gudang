# -*- coding: utf-8 -*-
{
    'name': "perpus",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "My Company",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Services',
    'version': '0.1',
    'application': True,

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'data/pengembalian_data.xml',
        'data/peminjaman_data.xml',


        'views/views.xml',
        'views/templates.xml',
        'views/menu.xml',
        'views/buku_view.xml',
        'views/rak_view.xml',
        'views/petugas_view.xml',
        'views/anggota_view.xml',
        'views/peminjaman_view.xml',
        'views/pengembalian_view.xml',

        'report/report.xml',
        'report/peminjaman_pdf.xml',
        'report/pengembalian_pdf.xml',

        'wizz/peminjamanreport.xml',

    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
