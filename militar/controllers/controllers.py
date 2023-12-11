# -*- coding: utf-8 -*-
# from odoo import http


# class Militar(http.Controller):
#     @http.route('/militar/militar', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/militar/militar/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('militar.listing', {
#             'root': '/militar/militar',
#             'objects': http.request.env['militar.militar'].search([]),
#         })

#     @http.route('/militar/militar/objects/<model("militar.militar"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('militar.object', {
#             'object': obj
#         })
