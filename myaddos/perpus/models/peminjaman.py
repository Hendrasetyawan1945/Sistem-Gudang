from odoo import fields, models, api
from odoo.exceptions import ValidationError

class peminjaman(models.Model):
    _name = 'p.peminjaman'
    _description = 'Description'

    name = fields.Char(string='Kode Peminjaman')
    no_anggota = fields.Many2one(
        comodel_name='p.anggota',
        string='No_anggota',
        required=False)
    petugas_id = fields.Many2one(
        comodel_name='res.partner',
        string='Petugas_id',
        required=False)
    peminjaman_ids = fields.One2many(
        comodel_name='p.peminjamandetail',
        inverse_name='peminjaman_id',
        string='Peminjaman_ids',
        required=False)
    cek = fields.Boolean(
        compute="_compute_cek",
        string='Apakah Anggota ',
        required=False)
    nama_peminjaman = fields.Char(
        compute="_compute_nama",
        string='Nama_peminjaman',
        required=False)
    # @api.constrains('cek')
    # def cek_anggota(self):
    #     if self.cek == 'False':
    #         raise ValidationError("Maaf tidak dapat meminjam buku karena belum termasuk anggota !!!")

    @api.constrains('cek')
    def _check_anggota(self):
        for record in self:
            if record.cek == False:
                raise ValidationError("Maaf tidak dapat meminjam buku karena belum termasuk anggota !!")
    @api.depends('cek')
    def _compute_cek(self):
        for a in self:
            a.cek = a.no_anggota.anggota
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
        string='Judul',
        required=False)
    qty = fields.Integer(
        string='Qty',
        required=False)
    tgl_pinjam = fields.Datetime(
        string='Tanggal Pinjam',
        required=False,
        default=fields.Datetime.now())
    tgl_kembali = fields.Date(
        string='Tanggal Kembali',
        required=False)

    @api.model
    def create(self, vals):
        record = super(peminjamandetail, self).create(vals)
        if record.qty:
            self.env['p.buku'].search([('id', '=', record.kd_register.id)]).write({
                'stok': record.kd_register.stok - record.qty})
            return record
    @api.depends('jdl')
    def _compute_jdl(self):
        for i in self:
            i.jdl = i.kd_register.judul
