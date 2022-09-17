from odoo import fields, models, api


class peminjamanreport(models.Model):
    _name = 'p.peminjamanreport'
    _description = 'Description'

    peminjam_id = fields.Many2one(
        comodel_name='p.peminjaman',
        string='Peminjam_id',
        required=False)
    tgl_mulai = fields.Date(
        string='Tgl Mulai',
        required=False)
    tgl_sampai = fields.Date(
        string='Tgl sampai',
        required=False)

    def action_peminjamanreport(self):
        filter = []
        peminjam_id = self.peminjam_id
        tgl_mulai = self.tgl_mulai
        tgl_sampai = self.tgl_sampai
        if peminjam_id:
            filter += [('nama_peminjaman', '=', peminjam_id.id)]
        if tgl_mulai:
            filter += [('tgl_pinjam', '>=', tgl_mulai)]
        if tgl_sampai:
            filter += [('tgl_pinjam', '<=', tgl_sampai)]
        print(filter)
        peminjam = self.env['p.peminjaman'].search_read(filter)
        print(peminjam)
        data = {
            'form': self.read()[0],
            'peminjamxxx': peminjam,
        }
        print(data)
        return self.env.ref('perpus.report_peminjaman_pdf').report_action(self, data=data)