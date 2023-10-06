from odoo import fields, models, api,_
from odoo.exceptions import ValidationError


class produk(models.Model):
    _name = 'u.produk'
    _description = 'Description'

    name = fields.Char(
        string='Id Produksi',
        required=True, default=lambda self: _('New'),
        copy=False)

    id_barang = fields.Many2one(
        comodel_name='u.barang', 
        string='ID Barang')

    id_bk = fields.Many2one(
        comodel_name='u.barangkeluar',
        string='ID Barang Keluar')


    tgl_jadi = fields.Date(
        string='Tanggal Jadi')
    
    jumlah = fields.Integer(
        string='Jumlah')

    namabk = fields.Char(
        compute="_compute_name",
        string='Nama Barang Keluar',
        required=False)

    @api.depends('namabk')
    def _compute_name(self):
        for i in self:
            i.namabk = i.id_bk.nama

    @api.model
    def create(self, vals):
        record = super(produk, self).create(vals)
        if record.jumlah:
            self.env['u.barangkeluar'].search([('id', '=', record.id_bk.id)]).write({
                'jumlah': record.id_bk.jumlah - record.jumlah})
            return record

    @api.model
    def create(self, vals):
        record = super(produk, self).create(vals)
        if record.jumlah:
            self.env['u.barang'].search([('id', '=', record.id_barang.id)]).write({
                'qty': record.id_barang.qty + record.jumlah})
            return record


    @api.constrains('jumlah')
    def _checkpemjualan(self):
        for i in self:
            if (i.jumlah > i.id_bk.jumlah):
                raise ValidationError(
                    'Maaf {} mencukupi untuk produksi stok untuk produksi sisa {} !!!'.format(
                        i.id_bk.nama,i.id_bk.jumlah))

    _sql_constraints = [
        ('unique_id_name', 'unique(name)', 'No. ID produksi harus unik yaaa...')
    ]