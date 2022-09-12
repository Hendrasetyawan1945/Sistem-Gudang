from odoo import fields, models, api


class ModelName(models.Model):
    _name = 'p.buku'
    _description = 'Description'

    name = fields.Char(string='kode_buku')
    judul = fields.Char(
        string='Judul',
        required=False)
    penulis = fields.Char(
        string='Penulis', 
        required=False)
    penerbit = fields.Char(
        string='Penerbit',
        required=False)
    id_rak = fields.Many2one(
        comodel_name='p.rak',
        string='Id_rak',
        required=False)
    stok = fields.Integer(
        string='Stok', 
        required=False)
