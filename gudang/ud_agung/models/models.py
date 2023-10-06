# -*- coding: utf-8 -*-

# from odoo import models, fields, api


# class ud_agung(models.Model):
#     _name = 'ud_agung.ud_agung'
#     _description = 'ud_agung.ud_agung'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
