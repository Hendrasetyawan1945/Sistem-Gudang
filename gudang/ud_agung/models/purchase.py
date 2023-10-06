from odoo import fields, models, api
from odoo.exceptions import ValidationError
import random
import string


class Purchase(models.Model):
    _name = 'u.purchase'
    _description = 'purchase'

    name = fields.Char(string='Nomor Pembelian', required=True, readonly=True, copy=False,
                    default=lambda self: self._generate_nomor_purchase())
    tanggal = fields.Date(string='Tanggal', required=True, default=fields.Date.today())
    supplier = fields.Many2one(comodel_name='u.supplier', string='Supplier', required=True)
    total = fields.Float(string='Total', compute='_compute_total_harga', store=True)
    detail_ids = fields.One2many(comodel_name='u.purchasedetail', inverse_name='purchase', string='Detail purchase')
    state = fields.Selection(string='Status',
                            selection=[('draft', 'Draft'),
                                        ('confirm', 'Confirm'),
                                        ('cancel', 'Cancel')],
                            required=True,
                            readonly=True,
                            default='draft')
    barang_ids = fields.Many2many(
        comodel_name='u.stok',
        relation='u_purchase_barang_rel',
        column1='purchase_id',
        column2='barang_id',
        string='Barang yang Dibeli',
        compute='_compute_barang_ids',
        store=True,
    )

    barang_jadi = fields.Boolean(string='Merupakan barang jadi',
                                required=False)

    @api.depends('detail_ids.subtotal')
    def _compute_total_harga(self):
        for purchase in self:
            purchase.total = sum(purchase.detail_ids.mapped('subtotal'))

    @api.depends('detail_ids.barang')
    def _compute_barang_ids(self):
        for purchase in self:
            purchase.barang_ids = purchase.detail_ids.mapped('barang')

    @api.depends('detail_ids')
    def _compute_total(self):
        for purchase in self:
            purchase.total = sum(detail.subtotal for detail in purchase.detail_ids)

    @staticmethod
    def _generate_nomor_purchase():
        digits = ''.join(random.choice(string.digits) for _ in range(4))
        nomor_purchase = 'PC' + digits
        return nomor_purchase

    def action_confirm(self):
        self.write({'state': 'confirm'})
        for purchase in self:
            for purchasedetail in purchase.detail_ids:
                if purchasedetail.jumlah:
                    if purchase.barang_jadi:  # Jika barang_jadi dicentang 
                        purchasedetail.barang.barangbertambah += purchasedetail.jumlah
                        purchasedetail.barang.stokbarang += purchasedetail.jumlah
                    else:
                        purchasedetail.barang.bahanbertambah += purchasedetail.jumlah
                        purchasedetail.barang.stokbahan += purchasedetail.jumlah

    def action_cancel(self):
        self.write({'state': 'cancel'})
        for purchase in self:
            for purchasedetail in purchase.detail_ids:
                if purchasedetail.jumlah:
                    if purchase.barang_jadi:  # Jika barang_jadi dicentang 
                        purchasedetail.barang.barangbertambah -= purchasedetail.jumlah
                        purchasedetail.barang.stokbarang -= purchasedetail.jumlah
                    else:
                        purchasedetail.barang.bahanbertambah -= purchasedetail.jumlah
                        purchasedetail.barang.stokbahan -= purchasedetail.jumlah

    # def action_cancel(self):
    #     self.write({'state': 'cancel'})
    #     for purchase in self:
    #         for purchasedetail in purchase.detail_ids:
    #             if purchasedetail.jumlah:
    #                 purchasedetail.barang.bahanbertambah -= purchasedetail.jumlah

    def action_draft(self):
        self.write({'state': 'draft'})

    def unlink(self):
        if self.filtered(lambda line: line.state != 'draft'):
            raise ValidationError('Tidak dapat menghapus selain yang masih DRAFT')
        else:
            for purchase in self:
                for purchase_detail in purchase.detail_ids:
                    if purchase_detail.jumlah:
                        purchase_detail.barang.bahanbertambah -= purchase_detail.jumlah
            return super(Purchase, self).unlink()



class purchaseDetail(models.Model):
    _name = 'u.purchasedetail'
    _description = 'Detail purchase'

    purchase = fields.Many2one(comodel_name='u.purchase', string='purchase', required=True)
    barang = fields.Many2one(comodel_name='u.stok', string='Barang', required=True)
    barang_kode = fields.Char(string='ID barang', compute="_compute_barang_kode", readonly=True)
    jumlah = fields.Integer(string='Jumlah Pembelian', required=True)
    harga_beli = fields.Float(string='Harga beli',compute="_compute_harga_beli", readonly=True)
    satuan = fields.Char(string='Satuan', compute="_compute_satuan", readonly=True)
    subtotal = fields.Integer(string='Subtotal',compute="_compute_subtotal",required=False)
    stoktersedia= fields.Char(string='Stok Yang Tersedia', compute="_compute_st", readonly=True)



    @api.depends('barang')
    def _compute_st(self):
        for barang in self:
            barang.stoktersedia = barang.barang.stokbahan
            
    @api.onchange('barang')
    def _onchange_satuan(self):
        if self.barang:
            self.satuan = self.barang.satuan
    
    @api.depends('barang')
    def _compute_satuan(self):
        for barang in self:
            barang.satuan = barang.barang.satuan

    @api.depends('barang')
    def _compute_barang_kode(self):
        for barang in self:
            barang.barang_kode = barang.barang.kode

    @api.onchange('barang')
    def _onchange_barang(self):
        if self.barang:
            self.barang_kode = self.barang.kode

    @api.depends('barang')
    def _compute_harga_beli(self):
        for detail in self:
            detail.harga_beli = detail.barang.hargabeli

    @api.depends('barang')
    def _compute_harga_beli(self):
        for detail in self:
            detail.harga_beli = detail.barang.hargabeli

    @api.depends('subtotal')
    def _compute_subtotal(self):
        for record in self:
            record.subtotal = record.jumlah * record.harga_beli


    @api.constrains('jumlah')
    def _check_purchase(self):
        for detail in self:
            if detail.jumlah < 1:
                raise ValidationError('Pembelian {} harus diisi dengan jumlah yang lebih dari 0!'.format(detail.barang.name))