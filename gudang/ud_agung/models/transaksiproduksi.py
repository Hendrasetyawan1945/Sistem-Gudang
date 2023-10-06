from odoo import fields, models, api
from odoo.exceptions import ValidationError


class TransaksiProduksi(models.Model):
    _name = 'u.produksi'
    _description = 'Transaksi Produksi'
    _rec_name = 'tanggal_produksi'

    tanggal_produksi = fields.Date(string='Tanggal Produksi', required=True, default=fields.Date.today())
    detail_produksi_ids = fields.One2many(
        comodel_name='u.detailproduksi',
        inverse_name='transaksi_produksi_id',
        string='Detail Produksi'
    )

    def update_stok_barang(self):
        for detail_produksi in self.detail_produksi_ids:
            if detail_produksi.barang_id:
                if detail_produksi.jumlah_ambil > detail_produksi.barang_id.stokbahan:
                    raise ValidationError('Stok Bahan {} tidak mencukupi! Stok saat ini: {}'.format(detail_produksi.barang_id.name, detail_produksi.barang_id.stokbahan))
                detail_produksi.barang_id.barangbertambah += detail_produksi.hasil
                detail_produksi.barang_id.stokbarang += detail_produksi.hasil
                detail_produksi.barang_id.stokbahan += detail_produksi.sisa
                detail_produksi.barang_id.bahanberkurang -= detail_produksi.hasil
                detail_produksi.barang_id.stokbahan -= detail_produksi.jumlah_ambil

    @api.model
    def create(self, vals):
        transaksi_produksi = super(TransaksiProduksi, self).create(vals)
        transaksi_produksi.update_stok_barang()
        return transaksi_produksi

class DetailProduksi(models.Model):
    _name = 'u.detailproduksi'
    _description = 'Detail Produksi'

    transaksi_produksi_id = fields.Many2one(
        comodel_name='u.produksi',
        string='Transaksi Produksi',
        required=True
    )
    barang_id = fields.Many2one(comodel_name='u.stok', string='Barang', required=True)
    jumlah_ambil = fields.Integer(string='Jumlah Ambil', required=True)
    hasil = fields.Integer(string='Hasil')
    sisa = fields.Integer(string='Sisa', compute='_compute_sisa', store=True)

    @api.depends('jumlah_ambil', 'hasil')
    def _compute_sisa(self):
        for record in self:
            record.sisa = record.jumlah_ambil - record.hasil