from odoo import fields, models, api
import random
from odoo.exceptions import ValidationError
import string

class BarangKeluar(models.Model):
    _name = 'u.barangkeluar'
    _description = 'Barang Keluar'

    name = fields.Char(string='Nomor Barang Keluar', required=True, readonly=True, copy=False,
                    default=lambda self: self._generate_nomor_barang_keluar())
    tanggal = fields.Date(string='Tanggal', required=True, default=fields.Date.today())
    detail_ids = fields.One2many(comodel_name='u.barangkeluardetail', inverse_name='barang_keluar',
                                string='Detail Barang Keluar')
    state = fields.Selection(string='Status',
                            selection=[('draft', 'Draft'),
                                        ('confirm', 'Confirm'),
                                        ('done', 'Done'),
                                        ('cancel', 'Cancel')],
                            required=True,
                            readonly=True,
                            default='draft')

    @api.depends('detail_ids.jumlah')
    def _compute_total_jumlah(self):
        for barang_keluar in self:
            barang_keluar.total_jumlah = sum(barang_keluar.detail_ids.mapped('jumlah'))

    total_jumlah = fields.Integer(string='Total Jumlah', compute='_compute_total_jumlah')

    @staticmethod
    def _generate_nomor_barang_keluar():
        digits = ''.join(random.choice(string.digits) for _ in range(4))
        nomor_barang_keluar = 'BK' + digits
        return nomor_barang_keluar

    def action_confirm(self):
        self.write({'state': 'confirm'})
        for barang_keluar in self:
            for detail in barang_keluar.detail_ids:
                if detail.jumlah:
                    detail.barang.stok -= detail.jumlah

    def action_cancel(self):
        self.write({'state': 'cancel'})
        for barang_keluar in self:
            for detail in barang_keluar.detail_ids:
                if detail.jumlah:
                    detail.barang.stok += detail.jumlah

    def action_done(self):
        self.write({'state': 'done'})

    def action_draft(self):
        self.write({'state': 'draft'})

    def unlink(self):
        if self.filtered(lambda line: line.state != 'draft'):
            raise ValidationError('Tidak dapat menghapus selain yang masih DRAFT')
        else:
            for barang_keluar in self:
                for detail in barang_keluar.detail_ids:
                    if detail.jumlah:
                        detail.barang.stok += detail.jumlah
            return super(BarangKeluar, self).unlink()


class BarangKeluarDetail(models.Model):
    _name = 'u.barangkeluardetail'
    _description = 'Detail Barang Keluar'

    barang_keluar = fields.Many2one(comodel_name='u.barangkeluar', string='Barang Keluar', required=True)
    barang = fields.Many2one(comodel_name='u.barang', string='Barang', required=True)
    jumlah = fields.Integer(string='Jumlah', required=True)

