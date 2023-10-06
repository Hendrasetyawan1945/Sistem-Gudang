from odoo import fields, models, api
from odoo.exceptions import ValidationError
import random
import string


class Pembelian(models.Model):
    _name = 'u.pembelian'
    _description = 'Pembelian'

    name = fields.Char(string='Nomor Pembelian', required=True, readonly=True, copy=False,
                    default=lambda self: self._generate_nomor_pembelian())
    tanggal = fields.Date(string='Tanggal', required=True, default=fields.Date.today())
    supplier = fields.Many2one(comodel_name='u.supplier', string='Supplier', required=True)
    total = fields.Float(string='Total', compute='_compute_total_harga', store=True)
    detail_ids = fields.One2many(comodel_name='u.pembeliandetail', inverse_name='pembelian', string='Detail Pembelian')
    state = fields.Selection(string='Status',
                            selection=[('draft', 'Draft'),
                                        ('confirm', 'Confirm'),
                                        ('done', 'Done'),
                                        ('cancel', 'Cancel')],
                            required=True,
                            readonly=True,
                            default='draft')
    barang_ids = fields.Many2many(
        comodel_name='u.barang',
        relation='u_pembelian_barang_rel',
        column1='pembelian_id',
        column2='barang_id',
        string='Barang yang Dibeli',
        compute='_compute_barang_ids',
        store=True,
    )

    @api.depends('detail_ids.subtotal')
    def _compute_total_harga(self):
        for Pembelian in self:
            Pembelian.total = sum(Pembelian.detail_ids.mapped('subtotal'))

    @api.depends('detail_ids.barang')
    def _compute_barang_ids(self):
        for pembelian in self:
            pembelian.barang_ids = pembelian.detail_ids.mapped('barang')

    @api.depends('detail_ids')
    def _compute_total(self):
        for pembelian in self:
            pembelian.total = sum(detail.subtotal for detail in pembelian.detail_ids)

    @staticmethod
    def _generate_nomor_pembelian():
        digits = ''.join(random.choice(string.digits) for _ in range(4))
        nomor_pembelian = 'PB' + digits
        return nomor_pembelian

    def action_confirm(self):
        self.write({'state': 'confirm'})
        for pembelian in self:
            for pembeliandetail in pembelian.detail_ids:
                if pembeliandetail.jumlah:
                    pembeliandetail.barang.stok += pembeliandetail.jumlah

    def action_cancel(self):
        self.write({'state': 'cancel'})
        for pembelian in self:
            for pembeliandetail in pembelian.detail_ids:
                if pembeliandetail.jumlah:
                    pembeliandetail.barang.stok -= pembeliandetail.jumlah

    def action_done(self):
        self.write({'state': 'done'})

    def action_draft(self):
        self.write({'state': 'draft'})

    def unlink(self):
        if self.filtered(lambda line: line.state != 'draft'):
            raise ValidationError('Tidak dapat menghapus selain yang masih DRAFT')
        else:
            for pembelian in self:
                for pembelian_detail in pembelian.detail_ids:
                    if pembelian_detail.jumlah:
                        pembelian_detail.barang.stok -= pembelian_detail.jumlah
            return super(Pembelian, self).unlink()


class PembelianDetail(models.Model):
    _name = 'u.pembeliandetail'
    _description = 'Detail Pembelian'

    pembelian = fields.Many2one(comodel_name='u.pembelian', string='Pembelian', required=True)
    barang = fields.Many2one(comodel_name='u.barang', string='Barang', required=True)
    barang_kode = fields.Char(string='ID barang', compute="_compute_barang_kode", readonly=True)
    jumlah = fields.Integer(string='Jumlah', required=True)
    harga_beli = fields.Float(string='Harga Beli', store=True)
    subtotal = fields.Integer(string='Subtotal',compute="_compute_subtotal",required=False)
        
    @api.depends('barang')
    def _compute_barang_kode(self):
        for barang in self:
            barang.barang_kode = barang.barang.kode

    @api.onchange('barang')
    def _onchange_barang(self):
        if self.barang:
            self.barang_kode = self.barang.kode

    @api.depends('barang')
    def _compute_harga_jual(self):
        for detail in self:
            detail.harga_jual = detail.barang.harga_jual

    @api.depends('barang')
    def _compute_harga_beli(self):
        for detail in self:
            detail.harga_beli = detail.barang.harga_beli

    @api.depends('subtotal')
    def _compute_subtotal(self):
        for record in self:
            record.subtotal = record.jumlah * record.harga_beli


    @api.constrains('jumlah')
    def _check_pembelian(self):
        for detail in self:
            if detail.jumlah < 1:
                raise ValidationError('Pembelian {} harus diisi dengan jumlah yang lebih dari 0!'.format(detail.barang.name))