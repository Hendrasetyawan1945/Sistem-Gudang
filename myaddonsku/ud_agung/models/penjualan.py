from odoo import fields, models, api,_
from odoo.exceptions import ValidationError


class penjualan(models.Model):
    _name = 'u.penjualan'
    _description = 'Description'
    #_rec_name = 'id_penjualan'

    name = fields.Char(
        string='Id Penjualan',
        required=True, default=lambda self: _('New'),
        copy=False, readonly=True,)

    penjualan_ids = fields.One2many(
        comodel_name='u.penjualandetail',
        inverse_name='penjualan_id',
        string='Penjualan ids',
        required=False)

    barang_ids = fields.Many2many(
        comodel_name='u.barang',
        relation='u_penjualan_barang_rel',
        column1='penjualan_id',
        column2='barang_id',
        string='Barang yang Dijual',
        compute='_compute_barang_ids',
        store=True,  # Tambahkan parameter store=True untuk menyimpan nilai yang dihitung
    )

    barang_names = fields.Char(
        string='Daftar penjualan Nama Barang',
        compute='_compute_barang_names',
        store=True,  # Tambahkan parameter store=True untuk menyimpan nilai yang dihitung
    )

    @api.depends('penjualan_ids')
    def _compute_barang_ids(self):
        for penjualan in self:
            penjualan.barang_ids = penjualan.penjualan_ids.mapped('barang')

    @api.depends('barang_ids')
    def _compute_barang_names(self):
        for penjualan in self:
            penjualan.barang_names = ', '.join(penjualan.barang_ids.mapped('name'))

    tgl_penjualan = fields.Date(
        string='Tanggal Penjualan',
        default=fields.Date.context_today,
        required=False)

    total_bayar = fields.Integer(
        compute="_compute_totalbayar",
        string='Total_bayar',
        required=False)
    
    ket = fields.Char(string='Keterangan')

    id_supplier = fields.Many2one(
        comodel_name='u.supplier', string='Id Supplier')
    
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
    

    @api.depends('total_bayar')
    def _compute_totalbayar(self):
        for record in self:
            a = sum(self.env['u.penjualandetail'].search(
                [('penjualan_id', '=', record.id)]).mapped('subtotal'))
            record.total_bayar = a

    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('u.penjualan') or _('New')
        record = super(penjualan, self).create(vals)
        return record

class penjualandetail(models.Model):
    _name = 'u.penjualandetail'
    _description = 'Description'
    #_rec_name = 'id_penjualandetail'

    barang = fields.Many2one(
        comodel_name='u.barang',
        string='Kode_Barang',
        required=False)

    nama = fields.Char(
        compute="_compute_name",
        string='Nama Barang',
        required=False)

    penjualan_id = fields.Many2one(
        comodel_name='u.penjualan',
        string='Penjualan_id',
        required=False)

    harga_jual = fields.Integer(
        string='Harge Jual',
        compute="_compute_hj",
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

    @api.depends('harga_jual')
    def _compute_hj(self):
        for i in self:
            i.harga_jual = i.barang.hargajual

    @api.model
    def create(self, vals):
        record = super(penjualandetail, self).create(vals)
        if record.jumlah:
            self.env['u.barang'].search([('id', '=', record.barang.id)]).write(
                {'qty': record.barang.qty - record.jumlah})
        return record


    @api.depends('subtotal')
    def _compute_subtotal(self):
        for record in self:
            record.subtotal = record.jumlah * record.harga_jual

    @api.constrains('jumlah')
    def _checkpemjualan(self):
        for i in self:
            if i.jumlah < 1:
                raise ValidationError(
                    'Maaf Penjulan {} harus di isi tidak boleh 0 !!!'.format(
                        i.barang.name))
            elif (i.jumlah > i.barang.qty):
                raise ValidationError('Stok  {} tidak mencukupi, hanya tersedia {}'
                                    .format(i.barang.name, i.barang.qty))
