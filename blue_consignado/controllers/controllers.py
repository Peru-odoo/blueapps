# -*- coding: utf-8 -*-
# from odoo import http


# class BlueConsultarCpf(http.Controller):
#     @http.route('/blue_consultar_cpf/blue_consultar_cpf/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/blue_consultar_cpf/blue_consultar_cpf/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('blue_consultar_cpf.listing', {
#             'root': '/blue_consultar_cpf/blue_consultar_cpf',
#             'objects': http.request.env['blue_consultar_cpf.blue_consultar_cpf'].search([]),
#         })

#     @http.route('/blue_consultar_cpf/blue_consultar_cpf/objects/<model("blue_consultar_cpf.blue_consultar_cpf"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('blue_consultar_cpf.object', {
#             'object': obj
#         })
