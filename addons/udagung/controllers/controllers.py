# -*- coding: utf-8 -*-
# from odoo import http


# class Udagung(http.Controller):
#     @http.route('/udagung/udagung', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/udagung/udagung/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('udagung.listing', {
#             'root': '/udagung/udagung',
#             'objects': http.request.env['udagung.udagung'].search([]),
#         })

#     @http.route('/udagung/udagung/objects/<model("udagung.udagung"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('udagung.object', {
#             'object': obj
#         })
