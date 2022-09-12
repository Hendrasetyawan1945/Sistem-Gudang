# -*- coding: utf-8 -*-
# from odoo import http


# class Hendra(http.Controller):
#     @http.route('/hendra/hendra', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/hendra/hendra/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('hendra.listing', {
#             'root': '/hendra/hendra',
#             'objects': http.request.env['hendra.hendra'].search([]),
#         })

#     @http.route('/hendra/hendra/objects/<model("hendra.hendra"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('hendra.object', {
#             'object': obj
#         })
