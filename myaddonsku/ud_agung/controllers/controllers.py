# -*- coding: utf-8 -*-
# from odoo import http


# class UdAgung(http.Controller):
#     @http.route('/ud_agung/ud_agung', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/ud_agung/ud_agung/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('ud_agung.listing', {
#             'root': '/ud_agung/ud_agung',
#             'objects': http.request.env['ud_agung.ud_agung'].search([]),
#         })

#     @http.route('/ud_agung/ud_agung/objects/<model("ud_agung.ud_agung"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('ud_agung.object', {
#             'object': obj
#         })
