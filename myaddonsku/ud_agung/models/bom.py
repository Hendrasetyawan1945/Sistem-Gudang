from odoo import fields, models


class BOM(models.Model):
    _name = 'u.bom'
    _description = 'Bill of Materials'

    name = fields.Char(string='Name')
    product_id = fields.Many2one(
        comodel_name='u.barang',
        string='Product',
        required=True
    )
    bom_line_ids = fields.One2many(
        comodel_name='u.bom.line',
        inverse_name='bom_id',
        string='BOM Lines'
    )


class BOMLine(models.Model):
    _name = 'u.bom.line'
    _description = 'Bill of Materials Line'

    bom_id = fields.Many2one(
        comodel_name='u.bom',
        string='BOM',
        required=True,
        inverse_name='bom_line_ids'  # Add this line to define the inverse relationship
    )
    component_id = fields.Many2one(
        comodel_name='u.barang',
        string='Component',
        required=True
    )
    quantity = fields.Float(string='Quantity', default=1.0)