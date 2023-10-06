# -*- coding: utf-8 -*-
# from odoo import http


# class Gudang(http.Controller):
#     @http.route('/gudang/gudang', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/gudang/gudang/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('gudang.listing', {
#             'root': '/gudang/gudang',
#             'objects': http.request.env['gudang.gudang'].search([]),
#         })

#     @http.route('/gudang/gudang/objects/<model("gudang.gudang"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('gudang.object', {
#             'object': obj
#         })
