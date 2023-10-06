from odoo import fields, models, api
import random
import string


class stok(models.Model):
    _name = 'u.stok'
    _description = 'stok'

    name = fields.Char(string='Nama Barang', required=True)
    kode = fields.Char(string='Kode Barang ', required=True, copy=False, default=lambda self: self._generate_kode())
    stokbahan = fields.Integer(string='Stok Bahan Mentah', required=True)
    hargabeli = fields.Integer(string='Harga Beli',required=True)
    stokbarang = fields.Integer(string='Stok Barang Jadi', required=True)
    hargajual = fields.Integer(string='Harga Jual', required=True)

    satuan = fields.Selection(
        string='Satuan',
        selection=[
            ('m3', 'M3'),
            ('pcs', 'Pcs'),
            ('kg', 'Kg'),
            ('gram', 'Gram'),
            ('ton', 'Ton'),
            ('kw', 'KW'),
            ('box', 'Box'),
            ('lembar', 'Lembar'),
            ('lusin', 'Lusin'),
            ('kotak', 'Kotak'),
            ('lainya', 'Lainya'),
            # Tambahkan pilihan lainnya di sini
        ],
        required=False,
    )
    bahanbertambah = fields.Integer(string='Bahan Bertambah',readonly=True)
    bahanberkurang = fields.Integer(string='Bahan Berkurang',readonly=True)
    barangbertambah = fields.Integer(string='Barang Bertambah',readonly=True)
    barangberkurang = fields.Integer(string='Barang Berkurang',readonly=True)
    
    # Tambahkan field 'penjualan_ids' untuk menyimpan riwayat pembelian
    pembelian_ids = fields.Many2many('u.purchase', compute='_compute_pe_ids', string='ID Pembelian Barang')

    # Method untuk menghitung nilai computed field 'penjualan_ids'
    def _compute_pe_ids(self):
        for stok in self:
            stok.pembelian_ids = self.env['u.purchase'].search([('barang_ids', 'in', stok.id)])
    # Tambahkan field untuk menyimpan total pembelian
    total_pembelian = fields.Float(string='Total Pembelian', compute='_compute_total_pembelian')

    # Method untuk menghitung total pembelian (jumlah terbeli)
    @api.depends('pembelian_ids')
    def _compute_total_pembelian(self):
        for stok in self:
            total_pembelian = 0.0
            for pembelian in stok.pembelian_ids:
                total_pembelian += pembelian.total
            stok.total_pembelian = total_pembelian
    # Tambahkan field untuk menyimpan jumlah terbeli (total pembelian)
    jumlah_terbeli = fields.Integer(string='Jumlah Terbeli', compute='_compute_jumlah_terbeli')

    # Method untuk menghitung total pembelian (jumlah terbeli)
    @api.depends('pembelian_ids')
    def _compute_jumlah_terbeli(self):
        for stok in self:
            jumlah_terbeli = 0
            for pembelian in stok.pembelian_ids:
                for detail in pembelian.detail_ids:
                    jumlah_terbeli += detail.jumlah
            stok.jumlah_terbeli = jumlah_terbeli
    ################################################################################
    ###############################################################################
    penjualan_ids = fields.Many2many('u.penjualan', compute='_compute_penjualan_ids', string='ID Penjualan Barang')

    # Method untuk menghitung nilai computed field penjualan_ids
    def _compute_penjualan_ids(self):
        for stok in self:
            stok.penjualan_ids = self.env['u.penjualan'].search([('barang_ids', 'in', stok.id)])

    # Tambahkan field computed untuk menyimpan jumlah total penjualan
    total_penjualan = fields.Float(string='Total Penjualan', compute='_compute_total_penjualan')

    # Method untuk menghitung nilai computed field total_penjualan
    def _compute_total_penjualan(self):
        for stok in self:
            total_penjualan = 0.0
            for penjualan in stok.penjualan_ids:
                total_penjualan += penjualan.total  # Gantilah 'total' dengan field yang sesuai pada model u.penjualan
            stok.total_penjualan = total_penjualan

    jumlah_terjual = fields.Integer(compute='_compute_jumlah_terjual', string='Jumlah Terjual')

    # Method untuk menghitung nilai computed field penjualan_ids
    def _compute_penjualan_ids(self):
        for stok in self:
            stok.penjualan_ids = self.env['u.penjualan'].search([('barang_ids', 'in', stok.id)])

    # Method untuk menghitung jumlah barang yang terjual
    def _compute_jumlah_terjual(self):
        for stok in self:
            stok.jumlah_terjual = sum(stok.penjualan_ids.mapped('detail_ids.jumlah'))


    @staticmethod
    def _generate_kode():
        digits = ''.join(random.choice(string.digits) for _ in range(4))
        kode = 'KB' + digits
        return kode