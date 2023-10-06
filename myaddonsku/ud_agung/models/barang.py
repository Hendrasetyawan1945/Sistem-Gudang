from odoo import fields, models, api,_
from odoo.exceptions import ValidationError
from odoo.exceptions import UserError


class barang(models.Model):
    _name = 'u.barang'
    _description = 'Description'
    _rec_name = 'id_barang'


    id_barang = fields.Char(
        string='Id Barang',
        default=lambda self: _('New ID Barang'),
        copy=False, readonly='True',required=True,)

    name = fields.Char(
        string="Nama barang",
        required=False,
        size=50)

    tipe = fields.Many2one(
        comodel_name='u.type',
        string='ID Type',
        required=False
    )

    type_bar = fields.Char(
        string='Type Barang',
        related='tipe.type',
        readonly=True
    )

    hargabeli = fields.Float(
        string='Harga Beli',
        digits=(12, 2),   
        default=0.0,
        required=True,
        )
        
    hargajual = fields.Integer(
        string='Harga Jual',
        digits=(12, 2),
        required=True,)

    satuan = fields.Selection(
    string='Satuan',
    selection=[
        ('m3', 'M3'),
        ('meter', 'Meter'),
        ('pcs', 'Pcs'),
        ('kg', 'Kg'),
        ('gram', 'Gram'),
        ('liter', 'Liter'),
        ('ton', 'Ton'),
        ('kw', 'KW'),
        ('kva', 'KVA'),
        ('batang', 'Batang'),
        ('box', 'Box'),
        ('ons', 'Ons'),
        ('buah', 'Buah'),
        ('lembar', 'Lembar'),
        ('roll', 'Roll'),
        ('set', 'Set'),
        ('pasang', 'Pasang'),
        ('lusin', 'Lusin'),
        ('rim', 'Rim'),
        ('pak', 'Pak'),
        ('kardus', 'Kardus'),
        ('kotak', 'Kotak'),
        ('batu', 'Batu'),
        ('gelas', 'Gelas'),
        ('kain', 'Kain'),
        ('tas', 'Tas'),
        ('dus', 'Dus'),
        ('batang', 'Batang'),
        ('tabung', 'Tabung'),
        ('botol', 'Botol'),
        ('kotak', 'Kotak'),
        ('pasang', 'Pasang'),
        ('lainya', 'Lainya'),

        # Tambahkan pilihan lainnya di sini
    ],
    required=False,
)

    qty = fields.Integer(string='Stok')

    @api.onchange('tipe')
    def on_type_change(self):
        if self.tipe:
            self.type_bar = self.tipe.type
        else:
            self.type_bar = False

    # @api.constrains('hargabeli')
    # def _check_hargabeli(self):
    #     for record in self:
    #         if not record.hargabeli.isdigit():
    #             raise ValidationError("Harga beli harus berupa angka atau numerik!")

    # @api.constrains('hargajual')
    # def _check_hargabeli(self):
    #     for record in self:
    #         if not record.hargabeli.isdigit():
    #             raise ValidationError("Harga beli harus berupa angka atau numerik!")    

    @api.model
    def create(self, vals):
        if vals.get('id_barang', _('New')) == _('New'):
            vals['id_barang'] = self.env['ir.sequence'].next_by_code('u.barang') or _('New')
        record = super(barang, self).create(vals)
        return record
