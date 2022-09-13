from odoo import fields, models, api


class rak(models.Model):
    _name = 'p.rak'
    _description = 'Description'

    name = fields.Char(string='Nama Rak')
    lokasi_rak = fields.Char(
        string='Lokasi Rak',
        required=False)
    ids_rak = fields.One2many(
        comodel_name='p.buku',
        inverse_name='id_rak',
        string='Ids_rak',
        required=False)
