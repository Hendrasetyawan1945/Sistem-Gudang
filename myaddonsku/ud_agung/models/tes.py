from odoo import fields, models, api,_
import random
import string

class tes(models.Model):
    _name = 'u.tes'
    _description = 'tes'

    name = fields.Char(string='Nama tes', required=True)
    kode = fields.Char(string='Kode tes', required=True, readonly=True, copy=False, default=lambda self: self._generate_kode())
    harga = fields.Float(string='Harga', required=True)
    stok = fields.Integer(string='Stok', required=True)

    @api.depends('harga', 'stok')
    def _compute_total_value(self):
        for tes in self:
            tes.total_value = tes.harga * tes.stok

    total_value = fields.Float(string='Total Nilai', compute='_compute_total_value')

    @api.model
    def _generate_kode(self):
        digits = ''.join(random.choice(string.digits) for _ in range(8))
        return digits
