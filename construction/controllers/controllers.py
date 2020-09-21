# -*- coding: utf-8 -*-
# from odoo import http


# class Expert(http.Controller):
#     @http.route('/expert/expert/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/expert/expert/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('expert.listing', {
#             'root': '/expert/expert',
#             'objects': http.request.env['expert.expert'].search([]),
#         })

#     @http.route('/expert/expert/objects/<model("expert.expert"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('expert.object', {
#             'object': obj
#         })
