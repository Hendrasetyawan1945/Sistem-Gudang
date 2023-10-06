from odoo import fields, models, api, _
from odoo.exceptions import ValidationError

class Benda(models.Model):
    _name = 'u.benda'
    _description = 'Description'
    _rec_name = 'id_benda'

    id_benda = fields.Char(
        string='Id benda',
        required=True, default=lambda self: _('New ID benda tes aja'),
        copy=False, )

    name = fields.Char(
        string="Nama benda",
        required=False,
        size=50)

    tipe = fields.Many2one(
        comodel_name='u.type',
        string='ID Type',
        required=False,)

    hargabeli = fields.Integer(
        string='Harga Beli',
        digits=(12, 2),
        required=True,
    )

    hargajual = fields.Integer(
        string='Harga Jual',
        digits=(12, 2),
        required=True,
    )

    satuan = fields.Selection(
        string='Satuan',
        selection=[('m3', 'M3')],
        required=False,
    )

    qty = fields.Integer(string='Stok')

    @api.constrains('hargabeli')
    def _check_hargabeli(self):
        for record in self:
            if not str(record.hargabeli).isdigit():
                raise ValidationError("Harga beli harus berupa angka atau numerik!")

    @api.constrains('hargajual')
    def _check_hargajual(self):
        for record in self:
            if not str(record.hargajual).isdigit():
                raise ValidationError("Harga jual harus berupa angka atau numerik!")

