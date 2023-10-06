from odoo import fields, models, api,_


class type(models.Model):
    _name = 'g.type'
    _description = 'Description'
    _rec_name = 'id_type'

    id_type = fields.Char(
        string='Id Type',
        required=True,
        default=lambda self: _('New'),
        copy=False, readonly='True')

    # name = fields.Char(
    #     string='ID Type',
    #     required=True,)
    
    type = fields.Char(
        string='Type Barang',
        required=False,)

    # ids_barang = fields.One2many(
    #     comodel_name='g.barang',
    #     inverse_name='tipe',
    #     string='Ids_Barang',
    #     required=False)

    @api.model
    def create(self, vals):
        if vals.get('id_type', _('New')) == _('New'):
            vals['id_type'] = self.env['ir.sequence'].next_by_code('g.type') or _('New')
        record = super(type, self).create(vals)
        return record
    
    