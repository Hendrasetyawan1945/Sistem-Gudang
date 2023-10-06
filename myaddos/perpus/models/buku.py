from odoo import fields, models, api


class ModelName(models.Model):
    _name = 'p.buku'
    _description = 'Description'

    name = fields.Char(string='kode_buku')
    judul = fields.Char(
        string='Judul',
        required=False)
    penulis = fields.Char(
        string='Penulis', 
        required=False)
    penerbit = fields.Char(
        string='Penerbit',
        required=False)
    id_rak = fields.Many2one(
        comodel_name='p.rak',
        string='Id_rak',
        required=False)
    stok = fields.Integer(
        string='Stok', 
        required=False)

    def _get_produk_qrcode(self):
        for rec in self:
            rec.produk_qrcode = str(rec.id)

    def print_qrcode(self):
        return {
            'type': 'ir.actions.report',
            'report_name': 'buku.report_buku_qrcode_id',
            'report_type': 'qweb-pdf',
        }

    produk_qrcode = fields.Char(
        string="Produk QR Code",
        compute=_get_produk_qrcode,
        required =False
    )

