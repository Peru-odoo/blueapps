# -*- coding: utf-8 -*-
# from odoo import http


# class InboxNotifEmail(http.Controller):
#     @http.route('/inbox_notif_email/inbox_notif_email/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/inbox_notif_email/inbox_notif_email/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('inbox_notif_email.listing', {
#             'root': '/inbox_notif_email/inbox_notif_email',
#             'objects': http.request.env['inbox_notif_email.inbox_notif_email'].search([]),
#         })

#     @http.route('/inbox_notif_email/inbox_notif_email/objects/<model("inbox_notif_email.inbox_notif_email"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('inbox_notif_email.object', {
#             'object': obj
#         })
