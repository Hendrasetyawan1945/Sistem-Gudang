from odoo import fields, models, api,_


class supplier(models.Model):
    _name = 'u.supplier'
    _description = 'Description'
    _rec_name = 'id_supplier'

    id_supplier = fields.Char(
        string='Id Supplier',
        required=True, default=lambda self: _('New ID Supplier'),
        copy=False, readonly='True')

    name = fields.Char(
        string='Nama Supplier',
        required=False,
        size=50)
    
    alamat = fields.Char(
        string='Alamat',
        required=False,)
    no_tlpn = fields.Char(
        string='No Telepon',
        required=False)
    

    @api.model
    def create(self, vals):
        if vals.get('id_supplier', _('New')) == _('New'):
            vals['id_supplier'] = self.env['ir.sequence'].next_by_code('u.supplier') or _('New')
        record = super(supplier, self).create(vals)
        return record
    
    