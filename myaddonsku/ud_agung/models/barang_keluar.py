from odoo import fields, models, api,_


class barangkeluar(models.Model):
    _name = 'u.barangkeluar'
    _description = 'Description'

    name = fields.Char(
        string='Id Barang Keluar',
        required=True, default=lambda self: _('New'),
        copy=False,
        size=10)

    id_barang = fields.Many2one(
        comodel_name='u.barang',
        string='ID Barang',
        required=False)
    
    tgl_keluar = fields.Date(
        default=fields.Date.context_today,
        string='Tanggal Keluar')

    nama = fields.Char(
        compute="_compute_name",
        string='Nama Barang',
        required=False)

    jumlah = fields.Integer(
        string='Jumlah')

    @api.depends('nama')
    def _compute_name(self):
        for i in self:
            i.nama = i.id_barang.name

    @api.model
    def create(self, vals):
        record = super(barangkeluar, self).create(vals)
        if record.jumlah and record.id_barang:
            self.env['u.barang'].search([('id', '=', record.id_barang.id)]).write({
                'qty': record.id_barang.qty - record.jumlah})
        return record

    _sql_constraints = [
        ('unique_id_name', 'unique(name)', 'No. ID Barang Keluar harus unik yaaa...')
    ]
    # @api.model
    # def create(self, vals):
    #     if vals.get('name', _('New')) == _('New'):
    #         vals['name'] = self.env['ir.sequence'].next_by_code('u.barangkeluar') or _('New')
    #     record = super(barangkeluar, self).create(vals)
    #     return record

