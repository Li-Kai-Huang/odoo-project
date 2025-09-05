# -*- coding: utf-8 -*-
# from odoo import http


# class TeamManagement(http.Controller):
#     @http.route('/team_management/team_management', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/team_management/team_management/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('team_management.listing', {
#             'root': '/team_management/team_management',
#             'objects': http.request.env['team_management.team_management'].search([]),
#         })

#     @http.route('/team_management/team_management/objects/<model("team_management.team_management"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('team_management.object', {
#             'object': obj
#         })

