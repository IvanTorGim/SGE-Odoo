# -*- coding: utf-8 -*-
# from odoo import http


# class Interstellar(http.Controller):
#     @http.route('/interstellar/interstellar', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/interstellar/interstellar/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('interstellar.listing', {
#             'root': '/interstellar/interstellar',
#             'objects': http.request.env['interstellar.interstellar'].search([]),
#         })

#     @http.route('/interstellar/interstellar/objects/<model("interstellar.interstellar"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('interstellar.object', {
#             'object': obj
#         })
