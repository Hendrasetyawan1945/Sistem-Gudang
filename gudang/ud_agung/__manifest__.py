# -*- coding: utf-8 -*-
{
    'name': "GUDANG",

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
    'depends': ['base','web'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        # 'security/karyawan.xml',
        # 'security/bos.xml',
        'security/pegawai.xml',

        'views/views.xml',
        'views/templates.xml',
        'views/menu.xml',
        'views/barang.xml',
        'views/stok.xml',
        # 'views/bom.xml',
        # 'views/bomi.xml',
        # 'views/billofmaterial.xml',
        'views/produksi.xml',
        'views/type.xml',
        'views/supplier.xml',
        'views/pembelian.xml',
        'views/purchase.xml',
        'views/penjualan.xml',
        # 'views/dashboard.xml',
        'report/stock_report.xml',
        # 'report/stokbahan_pembelian.xml',

        # 'views/reportpembelian.xml',





    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
