from odoo import fields, models, api,_


class barang(models.Model):
    _name = 'g.barang'
    _description = 'Description'
    _rec_name = 'id_barang'

    id_barang = fields.Char(
        string='Id Barang',
        required=True,
        default=lambda self: _('New'),
        copy=False, readonly='True')


    name = fields.Char(
        string='Nama Barang',
        required=False,)
    satuan = fields.Selection(
        string='Satuan',
        selection=[('m3', 'M3'),],
        required=False, )

    @api.model
    def create(self, vals):
        if vals.get('id_barang', _('New')) == _('New'):
            vals['id_barang'] = self.env['ir.sequence'].next_by_code('g.barang') or _('New')
        record = super(type, self).create(vals)
        return record