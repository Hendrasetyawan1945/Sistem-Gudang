from odoo import fields, models, api,_
from odoo.exceptions import ValidationError


class pembelian(models.Model):
    _name = 'u.beli'
    _description = 'Description'
    
    name = fields.Char(
        string='Id Beli',
        required=True, default=lambda self: _('New'),
        copy=False, readonly=True,)

    barang = fields.Many2one(
        comodel_name='u.barang',
        string='Kode_Barang',
        required=False)

    nama = fields.Char(
        compute="_compute_name",
        string='Nama Barang',
        readonly='True',
        required=False)

    @api.depends('nama')
    def _compute_name(self):
        for i in self:
            i.nama = i.barang.name

    ket = fields.Char(string='Keterangan')

    supplier = fields.Many2one(
        comodel_name='u.supplier',
        string='ID Supplier'
        )

    namasupplier = fields.Char(
        compute='_compute_namesup',
        string='Nama Supplier',
        readonly=True)
    
    @api.depends('namasupplier')
    def _compute_namesup(self):
        for i in self:
            i.namasupplier = i.supplier.name

    tgl_pembelian = fields.Date(
        string='Tanggal pembelian',
        default=fields.Date.context_today,
        required=False)

    harga_beli = fields.Integer(
        string='Harge Beli',
        compute="_compute_hb",
        required=False)

    jumlah = fields.Integer(
        string='Jumlah',
        required=False)

    subtotal = fields.Integer(
        string='Subtotal',
        compute="_compute_subtotal",
        required=False)
    
    state = fields.Selection(string='Status',
                            selection=[('draf', 'Draf'),                                 
                                        ('confirm', 'Confirm'),
                                        ('done', 'Done'),
                                        ('cancel', 'Cancel')],
                            required=True,
                            readonly=True,
                            default='draf')

    def action_confirm(self):
        self.write({'state': 'confirm'})
    def action_done(self):
        self.write({'state': 'done'})
    def action_cancel(self):

        self.write({'state': 'cancel'})
    def action_draf(self):
        self.write({'state': 'draf'})

    def unlink(self):
        if self.filtered(lambda line: line.state != 'draf'):
            raise ValidationError('Tidak dapat menghapus selain yang masih DRAFT')


    def unlink(self):
        for record in self:
            if record.state != 'draf':
                raise ValidationError("Maaf, Anda hanya dapat menghapus rekaman yang berstatus 'Draf'.")

            if record.barang:
                record.barang.qty -= record.jumlah

        return super(pembelian, self).unlink()

    @api.depends('harga_beli')
    def _compute_hb(self):
        for i in self:
            i.harga_beli = i.barang.hargabeli

    @api.depends('subtotal')
    def _compute_subtotal(self):
        for record in self:
            record.subtotal = record.jumlah * record.harga_beli

    @api.depends('total_bayar')
    def _compute_totalbayar(self):
        for record in self:
            a = sum(self.env['u.pembeliandetail'].search(
                [('pembelian_id', '=', record.id)]).mapped('subtotal'))
            record.total_bayar = a

    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('u.pembelian') or _('New')
        record = super(pembelian, self).create(vals)
        return record
