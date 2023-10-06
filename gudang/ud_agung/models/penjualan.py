from odoo import fields, models, api
from odoo.exceptions import ValidationError
import random
import string

class Penjualan(models.Model):
    _name = 'u.penjualan'
    _description = 'Penjualan'

    name = fields.Char(string='Nomor Penjualan', required=True, readonly=True, copy=False,
                    default=lambda self: self._generate_nomor_penjualan())
    tanggal = fields.Date(string='Tanggal', required=True, default=fields.Date.today())
    total = fields.Float(string='Total', compute='_compute_total_harga', store=True)
    detail_ids = fields.One2many(comodel_name='u.penjualandetail', inverse_name='penjualan', string='Detail Penjualan')
    state = fields.Selection(string='Status',
                            selection=[('draft', 'Draft'),
                                        ('confirm', 'Confirm'),
                                        ('cancel', 'Cancel')],
                            required=True,
                            readonly=True,
                            default='draft')

    barang_ids = fields.Many2many(
        comodel_name='u.stok',
        relation='u_penjualan_barang_rel',
        column1='penjualan_id',
        column2='barang_id',
        string='Barang yang Dijual',
        compute='_compute_barang_ids',
        store=True,
    )


    @api.depends('detail_ids.subtotal')
    def _compute_total_harga(self):
        for penjualan in self:
            penjualan.total = sum(detail.subtotal for detail in penjualan.detail_ids)

    @api.depends('detail_ids.barang')
    def _compute_barang_ids(self):
        for penjualan in self:
            penjualan.barang_ids = penjualan.detail_ids.mapped('barang')

    @api.depends('detail_ids')
    def _compute_total(self):
        for penjualan in self:
            penjualan.total = sum(detail.subtotal for detail in penjualan.detail_ids)

    @staticmethod
    def _generate_nomor_penjualan():
        digits = ''.join(random.choice(string.digits) for _ in range(4))
        nomor_penjualan = 'PJ' + digits
        return nomor_penjualan

    def action_confirm(self):
        self.write({'state': 'confirm'})
        for penjualan in self:
            for penjualandetail in penjualan.detail_ids:
                if penjualandetail.jumlah:
                    penjualandetail.barang.barangberkurang -= penjualandetail.jumlah
                    penjualandetail.barang.stokbarang -= penjualandetail.jumlah
                    # stokbarang

    def action_cancel(self):
        self.write({'state': 'cancel'})
        for penjualan in self:
            for penjualandetail in penjualan.detail_ids:
                if penjualandetail.jumlah:
                    penjualandetail.barang.stokbarang += penjualandetail.jumlah


    def action_draft(self):
        self.write({'state': 'draft'})

    def unlink(self):
        if self.filtered(lambda line: line.state != 'draft'):
            raise ValidationError('Tidak dapat menghapus selain yang masih DRAFT')
        else:
            for penjualan in self:
                for penjualan_detail in penjualan.detail_ids:
                    if penjualan_detail.jumlah:
                        penjualan_detail.barang.stokbarang += penjualan_detail.jumlah
            return super(Penjualan, self).unlink()


class PenjualanDetail(models.Model):
    _name = 'u.penjualandetail'
    _description = 'Detail Penjualan'

    penjualan = fields.Many2one(comodel_name='u.penjualan', string='Penjualan', required=True)
    barang = fields.Many2one(comodel_name='u.stok', string='Barang', required=True)
    barang_kode = fields.Char(string='ID barang', compute="_compute_barang_kode", readonly=True)
    jumlah = fields.Integer(string='Jumlah Pembelian', required=True)
    harga_jual = fields.Float(string='Harga Jual',compute="_compute_hj", readonly=True)
    satuan = fields.Char(string='Satuan', compute="_compute_satuan", readonly=True)
    subtotal = fields.Integer(string='Subtotal', compute="_compute_subtotal", required=False)
    penjualan_state = fields.Selection(related='penjualan.state', string='State', store=True, readonly=True)

    stoktersedia= fields.Char(string='Stok Yang Tersedia', compute="_compute_st", readonly=True)

    @api.depends('barang')
    def _compute_barang_kode(self):
        for barang in self:
            barang.barang_kode = barang.barang.kode

    @api.depends('barang')
    def _compute_st(self):
        for barang in self:
            barang.stoktersedia = barang.barang.stokbarang

    @api.onchange('barang')
    def _onchange_satuan(self):
        if self.barang:
            self.satuan = self.barang.satuan
    
    @api.depends('barang')
    def _compute_satuan(self):
        for barang in self:
            barang.satuan = barang.barang.satuan

    @api.onchange('barang')
    def _onchange_barang(self):
        if self.barang:
            self.barang_kode = self.barang.kode
            
    @api.depends('barang')
    def _compute_hj(self):
        for barang in self:
            barang.harga_jual = barang.barang.hargajual

    @api.onchange('barang')
    def _onchange_hargajual(self):
        if self.barang:
            self.barang_kode = self.barang.hargajual

    @api.depends('subtotal')
    def _compute_subtotal(self):
        for record in self:
            record.subtotal = record.jumlah * record.harga_jual

    @api.constrains('jumlah')
    def _check_penjualan(self):
        for detail in self:
            if detail.jumlah < 1:
                raise ValidationError('Penjualan {} harus diisi dengan jumlah yang lebih dari 0!'.format(detail.barang.name))
            elif detail.jumlah > detail.barang.stokbarang:
                raise ValidationError('Stok barang {} tidak mencukupi! Stok saat ini: {}'.format(detail.barang.name, detail.barang.stokbarang))

