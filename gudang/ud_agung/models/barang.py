from odoo import fields, models, api
import random
import string


class Barang(models.Model):
    _name = 'u.barang'
    _description = 'Barang'

    name = fields.Char(string='Nama Barang', required=True)
    kode = fields.Char(string='Kode Barang', required=True, copy=False, default=lambda self: self._generate_kode())
    harga_beli = fields.Float(string='Harga Beli', required=True)
    harga_jual = fields.Float(string='Harga Jual', required=True)
    stok = fields.Integer(string='Stok', required=True)
    tipe = fields.Many2one(comodel_name='u.type', string='Tipe', required=True)
    tipe_name = fields.Char(string='Nama Tipe', related='tipe.name', readonly=True)
    tipe_kode = fields.Char(string='ID Tipe', compute="_compute_tipe_kode", readonly=True)

    satuan = fields.Selection(
        string='Satuan',
        selection=[
            ('m3', 'M3'),
            ('meter', 'Meter'),
            ('pcs', 'Pcs'),
            ('kg', 'Kg'),
            ('gram', 'Gram'),
            ('liter', 'Liter'),
            ('ton', 'Ton'),
            ('kw', 'KW'),
            ('kva', 'KVA'),
            ('batang', 'Batang'),
            ('box', 'Box'),
            ('ons', 'Ons'),
            ('buah', 'Buah'),
            ('lembar', 'Lembar'),
            ('roll', 'Roll'),
            ('set', 'Set'),
            ('pasang', 'Pasang'),
            ('lusin', 'Lusin'),
            ('rim', 'Rim'),
            ('pak', 'Pak'),
            ('kardus', 'Kardus'),
            ('kotak', 'Kotak'),
            ('batu', 'Batu'),
            ('gelas', 'Gelas'),
            ('kain', 'Kain'),
            ('tas', 'Tas'),
            ('dus', 'Dus'),
            ('batang', 'Batang'),
            ('tabung', 'Tabung'),
            ('botol', 'Botol'),
            ('kotak', 'Kotak'),
            ('pasang', 'Pasang'),
            ('lainya', 'Lainya'),
            # Tambahkan pilihan lainnya di sini
        ],
        required=False,
    )
        
    @api.depends('tipe')
    def _compute_tipe_kode(self):
        for barang in self:
            barang.tipe_kode = barang.tipe.kode

    @api.onchange('tipe')
    def _onchange_tipe(self):
        if self.tipe:
            self.tipe_kode = self.tipe.kode

    @api.onchange('tipe_name')
    def _onchange_tipe_name(self):
        if self.tipe_name:
            self.tipe_kode = self.tipe.kode

    @api.depends('harga_jual', 'stok')
    def _compute_total_value(self):
        for barang in self:
            barang.total_value = barang.harga_jual * barang.stok

    total_value = fields.Float(string='Total Nilai', compute='_compute_total_value')

    @staticmethod
    def _generate_kode():
        kode = 'B' + ''.join(random.choice(string.digits) for _ in range(8))
        return kode
