from odoo import fields, models, api


class BOM(models.Model):
    _name = 'u.bomi'
    _description = 'Bill of Materials'

    product = fields.Many2one(comodel_name='u.barang', string='Product', required=True)
    components = fields.Many2many(comodel_name='u.barang', relation='u_bom_component_rel',
                                column1='bom_id', column2='component_id', string='Components', required=True)
    bom_detail_ids = fields.One2many(comodel_name='u.bomdetail', inverse_name='bom', string='BOM Details')

    total_cost = fields.Float(string='Total Cost', compute='compute_total_cost')

    @api.depends('bom_detail_ids')
    def compute_total_cost(self):
        for bom in self:
            total_cost = 0.0
            for bom_detail in bom.bom_detail_ids:
                component_cost = bom_detail.component_id.harga_beli * bom_detail.quantity
                total_cost += component_cost
            bom.total_cost = total_cost


class BomDetail(models.Model):
    _name = 'u.bomidetail'
    _description = 'Bill of Materials Detail'

    bom = fields.Many2one(comodel_name='u.bomi', string='Bill of Materials', required=True)
    component_id = fields.Many2one(comodel_name='u.barang', string='Component', required=True)
    quantity = fields.Float(string='Quantity', required=True)
