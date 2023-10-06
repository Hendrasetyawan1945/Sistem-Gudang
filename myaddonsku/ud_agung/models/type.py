from odoo import fields, models, api,_


class type(models.Model):
    _name = 'u.type'
    _description = 'Description'
    _rec_name = 'id_type'

    id_type = fields.Char(
        string='Id Type',
        required=True, default=lambda self: _('New ID Type'),
        copy=False, readonly='True')

    type = fields.Char(
        string='Type Barang',
        required=False,
        size=30)

    ids_barang = fields.One2many(
        comodel_name='u.barang',
        inverse_name='tipe',
        string='Ids_Barang',
        required=False)

    @api.model
    def create(self, vals):
        if vals.get('id_type', _('New')) == _('New'):
            vals['id_type'] = self.env['ir.sequence'].next_by_code('u.type') or _('New')
        record = super(type, self).create(vals)
        return record
    
    