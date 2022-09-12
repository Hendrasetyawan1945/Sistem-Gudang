from odoo import fields, models, api


class petugas(models.Model):
    _inherit = 'res.partner'
    _description = 'New Description'

    jabatan = fields.Selection(
        string='Jabatan',
        selection=[('junior', 'Junior'),
                   ('Senior', 'Senior'), ],
        required=False, )

