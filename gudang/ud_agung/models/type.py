from odoo import fields, models
import random
import string

class Type(models.Model):
    _name = 'u.type'
    _description = 'Type'

    name = fields.Char(string='Type Name', required=True)
    kode = fields.Char(string='Type Code', required=True, copy=False, default=lambda self: self._generate_kode())
    barang_ids = fields.One2many(
        comodel_name='u.barang',
        inverse_name='tipe',
        string='Barang'
    )

    @staticmethod
    def _generate_kode():
        digits = ''.join(random.choice(string.digits) for _ in range(1, 9))
        kode = 'T' + digits
        return kode
