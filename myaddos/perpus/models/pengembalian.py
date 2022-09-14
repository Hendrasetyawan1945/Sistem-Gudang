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

    @api.depends('peminjaman_id')
    def _compute_nama_peminjam(self):
        for record in self:
            record.name = self.env['p.peminjaman'].search([('id', '=', record.peminjaman_id.id)]).mapped('nama_peminjaman')

    tgl_pengembalian = fields.Date(
        string='Tanggal Kembali',
        default=fields.Date.today())