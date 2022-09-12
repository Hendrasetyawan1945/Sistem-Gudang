# -*- coding: utf-8 -*-
# from odoo import http


# class Perpus(http.Controller):
#     @http.route('/perpus/perpus', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/perpus/perpus/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('perpus.listing', {
#             'root': '/perpus/perpus',
#             'objects': http.request.env['perpus.perpus'].search([]),
#         })

#     @http.route('/perpus/perpus/objects/<model("perpus.perpus"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('perpus.object', {
#             'object': obj
#         })
