from odoo import fields, models, api,_


class stok(models.Model):
    _name = 'u.stok'
    _description = 'Description'
    #_rec_name = 'id_type'

    name = fields.Char(
        string='Id Stok',
        required=True, default=lambda self: _('New'),
        copy=False, readonly='True')

    id_barang = fields.Many2one(
        comodel_name='u.barang', 
        string='ID Barang')
    
    jumlah = fields.Integer(string='Jumlah')

    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('u.stok') or _('New')
        record = super(stok, self).create(vals)
        return record
    
    