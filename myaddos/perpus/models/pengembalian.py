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
    denda = fields.Integer(
        compute='_compute_denda',
        string='Denda',
        required=False)
    @api.depends('peminjaman_id')
    def _compute_nama_peminjam(self):
        for record in self:
            record.name = self.env['p.peminjaman'].search([('id', '=', record.peminjaman_id.id)]).mapped('nama_peminjaman')
    @api.depends('tgl_kesepakatan')
    def _compute_tgl(self):
        for a in self:
            a.tgl_kesepakatan = a.peminjaman_id.tgl_kembali    
    @api.depends('tgl_kesepakatan', 'tgl_pengembalian', 'terlambat')
    def _compute_keterlambatan(self):
        if self.tgl_kesepakatan and self.tgl_pengembalian:
            d1 = datetime.strptime(str(self.tgl_kesepakatan), '%Y-%m-%d')
            d2 = datetime.strptime(str(self.tgl_pengembalian), '%Y-%m-%d')
            d3 = d2 - d1
            self.terlambat = str(d3.days)
        
    @api.depends('denda', 'terlambat')
    def _compute_denda(self):
        for i in self:
            if i.terlambat > 1:
                i.denda = i.terlambat * 5000
            elif i.terlambat > 7:
                i.denda = i.terlambat * 7000
            elif i.terlambat > 10:
                i.denda = i.terlambat * 10000


       



class pengembaliandetail(models.Model):
    _name = 'p.pengembaliandetail'
    _description = 'ModelName'
    _rec_name = 'detailpeminjaman'
    _rec_name = 'pengembalian_id'
        
    detailpeminjaman = fields.Many2one(
        comodel_name='p.peminjamandetail',
        string='Detailpeminjaman',
        required=False)
    pengembalian_id = fields.Many2one(
        comodel_name='p.pengembalian',
        string='Pengembalian_id',
        required=False)
    tgl_kesepakatan = fields.Date(
        compute='_compute_tgl',
        string='Tgl_kesepakatan',
        required=False)
    tgl_pengembalian = fields.Date(
        string='Tanggal Kembali',
        default=fields.Date.today())



    # @api.model
    # def _compute_tgl(self):
    #     for i in self:  # mapped = mengambil
    #         i.tgl_kesepakatan = self.env['p.peminjamandetail'].search([('tgl_kembali', '=', i.id)]).mapped('tgl_kembali')

    
