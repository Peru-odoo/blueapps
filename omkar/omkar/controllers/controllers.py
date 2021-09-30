# -*- coding: utf-8 -*-
# from odoo import http


# class Omkar(http.Controller):
#     @http.route('/omkar/omkar/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/omkar/omkar/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('omkar.listing', {
#             'root': '/omkar/omkar',
#             'objects': http.request.env['omkar.omkar'].search([]),
#         })

#     @http.route('/omkar/omkar/objects/<model("omkar.omkar"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('omkar.object', {
#             'object': obj
#         })
