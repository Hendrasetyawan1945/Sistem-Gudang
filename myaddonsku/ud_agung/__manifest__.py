# -*- coding: utf-8 -*-
{
    'name': "ud_agung",

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
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'data/type_data.xml',
        'data/barang_data.xml',
        'data/barangkeluar_data.xml',
        'data/supplier_data.xml',
        'data/penjualan_data.xml',
        'data/stok_data.xml',
        'data/pembelian_data.xml',

        'views/views.xml',
        'views/templates.xml',
        'views/menu.xml',        
        'views/barang.xml',
        # 'views/benda.xml',        
        'views/beli.xml',
        'views/bom.xml',
        'views/barangkeluar.xml',    
        'views/type.xml',
        'views/produk.xml',
        'views/supplier.xml',
        'views/penjualan.xml',
        # 'views/tes.xml',
        'views/pembelian.xml',


        'report/report.xml',
        'report/report_pembelian.xml',
        'report/report_penjualan.xml',





    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
