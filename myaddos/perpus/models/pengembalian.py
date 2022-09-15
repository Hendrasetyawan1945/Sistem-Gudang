from datetime import datetime
from odoo import fields, models, api


class pengembalian(models.Model):
    _name = 'p.pengembalian'
    _description = 'Description'

    name = fields.Char(
        compute='_compute_nama_peminjam',
        string='nama peminjam')
    peminjaman_id = fields.Many2one(
        comodel_name='p.peminjaman',
        string='Peminjaman_id',
        required=False)
    tgl_kesepakatan = fields.Date(
        compute='_compute_tgl',
        string='Tgl_kesepakatan',
        required=False)
    tgl_pengembalian = fields.Date(
        string='Tanggal Kembali',
        default=fields.Date.today())
    terlambat = fields.Integer(
        compute='_compute_keterlambatan',
        string='Terlambat', 
        required=False)
    # td = fields.Integer(
    #     compute='_compute_denda',
    #     string='Total Denda',
    #     required=False)
    denda = fields.Integer(
        compute='test',
        string='Total Denda',
        required=False)

    def test(self):
        for record in self:
            if record.terlambat < 0:
                record.denda = 0.0
            elif record.terlambat > 5:
                record.denda = 2000 * record.terlambat
            elif record.terlambat > 10:
                record.denda = 4000 * record.terlambat

    # @api.depends('terlambat')
    # def _compute_denda(self):
    #     for i in self:
    #         if i.terlambat < 0:
    #             i.denda = 0
    #         elif i.terlambat > 5:
    #             i.denda = i.terlambat * 5000
    #         elif i.terlambat > 10:
    #             i.denda = i.terlambat * 10000
    #         else:
    #             pass
    @api.depends('peminjaman_id')
    def _compute_nama_peminjam(self):
        for record in self:
            record.name = self.env['p.peminjaman'].search([('id', '=', record.peminjaman_id.id)]).mapped('nama_peminjaman')
    @api.depends('tgl_kesepakatan')
    def _compute_tgl(self):
        for a in self:
            a.tgl_kesepakatan = a.peminjaman_id.tgl_kembali    
    @api.depends('tgl_kesepakatan', 'tgl_pengembalian')
    def _compute_keterlambatan(self):
        for i in self:
            if self.tgl_kesepakatan and self.tgl_pengembalian:
                i.terlambat = (i.tgl_pengembalian - i.tgl_kesepakatan).days
            else:
                i.terlambat = 0

    # @api.depends('terlambat')
    # def _compute_d(self):
    #     for i in self:
    #         if i.terlambat < 0:
    #             i.denda = 0
    #         elif i.terlambat > 5:
    #             i.denda = i.terlambat * 5000
    #         elif i.terlambat > 10:
    #             i.denda = i.terlambat * 10000
    #         else:
    #             pass

    # @api.depends('denda', 'terlambat')
    # def _compute_denda(self):
    #     for i in self:
    #         if i.terlambat < 0:
    #             i.denda = 0
    #         elif i.terlambat > 5:
    #             i.denda = i.terlambat * 5000
    #         elif i.terlambat > 10:
    #             i.denda = i.terlambat * 10000
    #         else:
    #             pass
    # @api.depends('terlambat', 'td')
    # def _compute_tb(self):
    #     for a in self:
    #         if a.terlambat < 0:
    #             a.td = 0
    #         elif a.terlambat > 5:
    #             a.td = a.terlambat * 2000
    #         elif a.terlambat > 10:
    #             a.td = a.terlambat * 5000

       



