from odoo import fields, models, api

class anggota(models.Model):
    _name = 'p.anggota'
    _description = 'Description'

    name = fields.Char(string='No Anggota')
    nama = fields.Char(
        string='Nama',
        required=False)
    alamat = fields.Char(
        string='Alamat',
        required=False)
    prodi = fields.Char(
        string='Prodi',
        required=False)
    jk = fields.Selection(
        string='Jenis kelamin',
        selection=[('perempuan', 'Perempuan'),
                   ('laki-laki', 'Laki-Laki'), ],
        required=False, )
    anggota = fields.Boolean(
        string='Anggota',
        required=False)
    img = fields.Binary(string="Profil")

