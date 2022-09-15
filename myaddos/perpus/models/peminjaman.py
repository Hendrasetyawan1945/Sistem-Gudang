from odoo import fields, models, api
from odoo.exceptions import ValidationError

class peminjaman(models.Model):
    _name = 'p.peminjaman'
    _description = 'Description'

    name = fields.Char(string='Kode Peminjaman',
                       required=True,
                       )
    no_anggota = fields.Many2one(
        comodel_name='p.anggota',
        string='No_anggota',
        required=True)
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
    tgl_pinjam = fields.Datetime(
        string='Tanggal Pinjam',
        required=False,
        default=fields.Datetime.now())
    tgl_kembali = fields.Date(
        string='Tanggal Kembali',
        required=False)
    state = fields.Selection(string='Status',
                             selection=[('draf', 'Draf'),
                                        ('done', 'Done'),
                                        ('confirm', 'Confirm'),
                                        ('cancel', 'Cancel')],
                             required=True,
                             readonly=True,
                             default='draf')

    # write untuk mengedit suatu record
    def write(self, vals):
        for rec in self:
            a = self.env['p.peminjamandetail'].search(
                [('peminjaman_id', '=', rec.id)])
            print(a)
            print('--------------------------------------------------')
            for data in a:
                print(str(data.kd_register.name) + ' ' + str(data.qty))
                data.kd_register.stok += data.qty
        record = super(peminjaman, self).write(vals)
        for rec in self:
            b = self.env['p.peminjamandetail'].search(
                [('peminjaman_id', '=', rec.id)])
            print(a)
            print(b)
            print('++++++++++++++++++++++++++++++++++++++++++++++++++')
            for datab in b:
                if datab in a:  # jika ada yang ditambahkan
                    print(str(datab.kd_register.name) + ' ' + str(datab.qty))
                    datab.kd_register.stok -= datab.qty
                else:
                    pass  # jika tidak ada perubahan maka tidak ngapa"in
        return record
    def unlink(self): #berguna untuk menghapus record
        if self.filtered(lambda line: line.state != 'draf'):
            raise ValidationError("Maaf tidak dapat menghapus record pembelian silahkan kembalikan de Draf !!!")
        else:
            if self.peminjaman_ids:
                a = []
                for x in self:
                    a = self.env['p.peminjamandetail'].search(
                        [('peminjaman_id', '=', x.id)])
                    print(a)
                for i in a:
                    print(str(i.kd_register.name) + ' ' + str(i.qty))
                    i.kd_register.stok -= i.qty
            record = super(peminjaman, self).unlink()


    @api.constrains('cek')
    def _check_anggota(self):
        for record in self:
            if record.cek == '0':
                raise ValidationError("Maaf tidak dapat meminjam buku karena belum termasuk anggota !!")
    @api.depends('cek')
    def _compute_cek(self):
        for a in self:
            a.cek = a.no_anggota.anggota
    @api.depends('nama_peminjaman')
    def _compute_nama(self):
        for i in self:
            i.nama_peminjaman = i.no_anggota.nama

    def action_confirm(self):
        self.write({'state': 'confirm'})
    def action_done(self):
        self.write({'state': 'done'})
    def action_cancel(self):
        self.write({'state': 'cancel'})
    def action_draf(self):
        self.write({'state': 'draf'})
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
