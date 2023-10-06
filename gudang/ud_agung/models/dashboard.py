from odoo import fields, models

class Dashboard(models.Model):
    _name = 'u.dashboard'
    _description = 'Dashboard'

    name = fields.Char(string='Nama', required=True)
    stok_bahan = fields.Integer(string='Stok Bahan')
    stok_barang = fields.Integer(string='Stok Barang')
