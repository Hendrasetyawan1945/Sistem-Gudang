from odoo import fields, models, api


class peminjaman(models.Model):
    _name = 'p.peminjaman'
    _description = 'Description'

    name = fields.Char(string='Kode Peminjaman')
    no_anggota = fields.Many2one(
        comodel_name='p.anggota',
        string='No_anggota',
        required=False)
    peminjaman_ids = fields.One2many(
        comodel_name='p.peminjamandetail',
        inverse_name='peminjaman_id',
        string='Peminjaman_ids',
        required=False)
    nama_peminjaman = fields.Char(
        compute="_compute_nama",
        string='Nama_peminjaman',
        required=False)

    @api.depends('nama_peminjaman')
    def _compute_nama(self):
        for i in self:
            i.nama_peminjaman = i.no_anggota.nama

class peminjamandetail(models.Model):
    _name = 'p.peminjamandetail'
    _description = 'ModelName'
    
    kd_register = fields.Many2one(
        comodel_name='p.buku',
        string='Kode_register',
        required=True)
    peminjaman_id = fields.Many2one(
        comodel_name='p.peminjaman',
        string='Peminjaman_id',
        required=False)
    jdl = fields.Char(
        compute="_compute_jdl",
        string='JUdul',
        required=False)
    tgl_pinjam = fields.Datetime(
        string='Tgl_pinjam', 
        required=False,
        default=fields.Datetime.now())
    tgl_kembali = fields.Date(
        string='Tgl_kembali', 
        required=False)

    @api.depends('jdl')
    def _compute_jdl(self):
        for i in self:
            i.jdl = i.kd_register.judul
