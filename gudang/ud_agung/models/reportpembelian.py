# from odoo import models, fields,api


# class PembelianReport(models.AbstractModel):
#     _name = 'u.pembelian.report'
#     _description = 'Laporan Pembelian'
#     name = fields.Char(string='Nomor Pembelian')
#     tanggal = fields.Date(string='Tanggal')
#     supplier = fields.Many2one(comodel_name='u.supplier', string='Supplier')
#     total = fields.Float(string='Total')
#     state = fields.Selection(string='Status', selection=[('draft', 'Draft'), ('confirm', 'Confirm'), ('done', 'Done'), ('cancel', 'Cancel')])
    
#     def _get_report_data(self):
#         Pembelian = self.env['u.pembelian']
#         return Pembelian.search([]).read(['name', 'tanggal', 'supplier', 'total', 'state'])
    
#     @api.model
#     def init(self):
#         # Panggil method _get_report_data() untuk mengambil data transaksi pembelian
#         data = self._get_report_data()

#         # Buat entri laporan dengan menggunakan fungsi create() pada model laporan
#         self.create(data)
#     @api.model
#     def uninstall_hook(self):
#         # Panggil method init() untuk menginisialisasi ulang model laporan saat uninstall
#         self.init()
