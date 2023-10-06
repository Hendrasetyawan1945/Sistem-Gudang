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

    selected_barang_ids = fields.Many2many(
        comodel_name='u.stok',
        relation='u_produksi_barang_rel',
        column1='produksi_id',
        column2='barang_id',
        string='Barang Yang Di Produksi',
        compute='_compute_selected_barang_ids'
    )

    @api.depends('detail_produksi_ids.barang_id')
    def _compute_selected_barang_ids(self):
        for produksi in self:
            produksi.selected_barang_ids = produksi.detail_produksi_ids.mapped('barang_id')


    def update_stok_barang(self):
        for detail_produksi in self.detail_produksi_ids:
            if detail_produksi.barang_id:
                if detail_produksi.jumlah_ambil > detail_produksi.barang_id.stokbahan:
                    raise ValidationError('Stok barang {} tidak mencukupi untuk produksi! Stok saat ini: {}'.format(detail_produksi.barang_id.name, detail_produksi.barang_id.stokbahan))
                detail_produksi.barang_id.barangbertambah += detail_produksi.hasil
                detail_produksi.barang_id.stokbarang += detail_produksi.hasil
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
    barang_kode = fields.Char(string='ID barang', compute="_compute_barang_kode", readonly=True)
    satuan = fields.Char(string='Satuan', compute="_compute_satuan", readonly=True)
    jumlah_ambil = fields.Integer(string='Jumlah Ambil', required=True)
    hasil = fields.Integer(string='Hasil')

    stoktersedia= fields.Char(string='Stok Yang Tersedia', compute="_compute_st", readonly=True)



    @api.depends('barang_id')
    def _compute_st(self):
        for barang_id in self:
            barang_id.stoktersedia = barang_id.barang_id.stokbahan
    

    @api.onchange('barang_id')
    def _onchange_satuan(self):
        if self.barang_id:
            self.satuan = self.barang_id.satuan
    
    @api.depends('barang_id')
    def _compute_satuan(self):
        for barang_id in self:
            barang_id.satuan = barang_id.barang_id.satuan

    @api.depends('barang_id')
    def _compute_barang_kode(self):
        for barang_id in self:
            barang_id.barang_kode = barang_id.barang_id.kode

    @api.onchange('barang_id')
    def _onchange_barang(self):
        if self.barang_id:
            self.barang_kode = self.barang_id.kode
