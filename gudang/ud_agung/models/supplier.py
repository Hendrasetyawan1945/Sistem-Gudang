from odoo import fields, models
import random
import string


class Supplier(models.Model):
    _name = 'u.supplier'
    _description = 'Supplier'

    name = fields.Char(string='Nama Supplier', required=True)
    kode = fields.Char(string='Kode Supplier', required=True, copy=False, default=lambda self: self._generate_kode())
    alamat = fields.Text(string='Alamat')
    telepon = fields.Char(string='Telepon')
    email = fields.Char(string='Email')
    kota = fields.Char(string='Kota')

    @staticmethod
    def _generate_kode():
        digits = ''.join(random.choice(string.digits) for _ in range(1, 9))
        kode = 'S' + digits
        return kode
