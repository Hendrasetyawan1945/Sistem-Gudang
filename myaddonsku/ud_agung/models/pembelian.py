from odoo import fields, models, api,_
from odoo.exceptions import ValidationError


class pembelian(models.Model):
    _name = 'u.pembelian'
    _description = 'Description'
    
    name = fields.Char(
        string='Id Pembelian',
        required=True, default=lambda self: _('New'),
        copy=False,
        readonly=True, 
        )


    pembelian_ids = fields.One2many(
        comodel_name='u.pembeliandetail',
        inverse_name='pembelian_id',
        string='Daftar Pembelian',
    )

    barang_ids = fields.Many2many(
        comodel_name='u.barang',
        relation='u_pembelian_barang_rel',
        column1='pembelian_id',
        column2='barang_id',
        string='Barang yang Dibeli',
        compute='_compute_barang_ids',
        store=True,  # Tambahkan parameter store=True untuk menyimpan nilai yang dihitung
    )

    barang_names = fields.Char(
        string='Daftar Pembelian Nama Barang',
        compute='_compute_barang_names',
        store=True,  # Tambahkan parameter store=True untuk menyimpan nilai yang dihitung
    )

    @api.depends('pembelian_ids')
    def _compute_barang_ids(self):
        for pembelian in self:
            pembelian.barang_ids = pembelian.pembelian_ids.mapped('barang')

    @api.depends('barang_ids')
    def _compute_barang_names(self):
        for pembelian in self:
            pembelian.barang_names = ', '.join(pembelian.barang_ids.mapped('name'))

    ket = fields.Char(string='Keterangan')

    supplier = fields.Many2one(
        comodel_name='u.supplier',
        string='ID Supplier'
        )
    sup_bar = fields.Char(
        string='Nama Barang',
        related='supplier.name',
        readonly=True
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
    total_bayar = fields.Integer(
        compute="_compute_totalbayar",
        string='Total_bayar',
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
        for pembelian in self:
            for pembeliandetail in pembelian.pembelian_ids:
                if pembeliandetail.jumlah:
                    pembeliandetail.barang.qty += pembeliandetail.jumlah

    def action_done(self):
        self.write({'state': 'done'})

    def action_cancel(self):
        self.write({'state': 'cancel'})
        for pembelian in self:
            for pembeliandetail in pembelian.pembelian_ids:
                if pembeliandetail.jumlah:
                    pembeliandetail.barang.qty -= pembeliandetail.jumlah
                    
    def action_draf(self):
        self.write({'state': 'draf'})

    def unlink(self):
        if self.filtered(lambda line: line.state != 'draf'):
            raise ValidationError('Tidak dapat menghapus selain yang masih DRAFT')

    def unlink(self): #berguna untuk menghapus record
        if self.filtered(lambda line: line.state != 'draf'):
            raise ValidationError("Maaf tidak dapat menghapus record pembelian silahkan kembalikan de Draf !!!")
        else:
            if self.pembelian_ids:
                a = []
                for x in self:
                    a = self.env['u.pembeliandetail'].search(
                        [('pembelian_id', '=', x.id)])
                    print(a)
                for i in a:
                    print(str(i.barang.id_barang) + ' ' + str(i.jumlah))
                    i.barang.qty -= i.jumlah
            record = super(pembelian, self).unlink()

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


class pembeliandetail(models.Model):
    _name = 'u.pembeliandetail'
    _description = 'Description'
    #_rec_name = 'id_pembeliandetail'

    barang = fields.Many2one(
        comodel_name='u.barang',
        string='Kode_Barang',
        required=False)

    barang_bar = fields.Char(
        string='Nama Barang',
        related='barang.name',
        readonly=True
    )
    
    nama = fields.Char(
        compute="_compute_name",
        string='Nama Barang',
        required=False)
    
    pembelian_id = fields.Many2one(
        comodel_name='u.pembelian',
        string='pembelian_id',
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

    @api.depends('nama')
    def _compute_name(self):
        for i in self:
            i.nama = i.barang.name

    @api.depends('harga_beli')
    def _compute_hb(self):
        for i in self:
            i.harga_beli = i.barang.hargabeli

    @api.depends('subtotal')
    def _compute_subtotal(self):
        for record in self:
            record.subtotal = record.jumlah * record.harga_beli

