from datetime import datetime
from odoo import fields, models, api,_
from odoo.exceptions import ValidationError


class pengembalian(models.Model):
    _name = 'p.pengembalian'
    _description = 'Description'
    _rec_name = 'id_pengembalian'

    id_pengembalian = fields.Char(
        string='Id Pengembalian',
        required=True, default=lambda self: _('New'),
        copy=False, readonly='True')
    name = fields.Char(
        compute='_compute_nama_peminjam',
        string='nama peminjam')
    peminjaman_id = fields.Many2one(
        comodel_name='p.peminjaman',
        string='Peminjaman_id',
        required=True)
    @api.depends('peminjaman_id')
    def _compute_nama_peminjam(self):
        for record in self:
            record.name = self.env['p.peminjaman'].search([('id', '=', record.peminjaman_id.id)]).mapped('nama_peminjaman')

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
        compute='test',
        string='Total Denda',
        required=False)

    @api.model
    def create(self, vals):
        record = super(pengembalian, self).create(vals)
        if record.tgl_pengembalian:
            self.env['p.peminjaman'].search([('id', '=', record.peminjaman_id.id)]).write({'sudah_kembali': True})
            return record

    def test(self):
        for record in self:
            if record.terlambat < 0:
                record.denda = 0.0
            elif record.terlambat > 5:
                record.denda = 2000 * record.terlambat
            elif record.terlambat > 10:
                record.denda = 4000 * record.terlambat

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
    @api.model
    def create(self, vals):
        if vals.get('id_pengembalian', _('New')) == _('New'):
            vals['id_pengembalian'] = self.env['ir.sequence'].next_by_code('p.pengembalian') or _('New')
        record = super(pengembalian, self).create(vals)
        return record