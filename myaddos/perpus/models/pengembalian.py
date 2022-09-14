from odoo import fields, models, api


class pengembalian(models.Model):
    _name = 'p.pengembalian'
    _description = 'Description'

    name = fields.Char(
        compute='_compute_nama_peminjam',
        string='nama peminjam')

    @api.depends('name')
    def _compute_nama_peminjam(self):
        for record in self:
            record.name = self.env['p.peminjaman'].search([('id', '=', record.kd_register.id)]).mapped('no_anggota')
