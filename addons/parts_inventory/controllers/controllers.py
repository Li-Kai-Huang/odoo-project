# -*- coding: utf-8 -*-
# from odoo import http


# class PartsInventory(http.Controller):
#     @http.route('/parts_inventory/parts_inventory', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/parts_inventory/parts_inventory/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('parts_inventory.listing', {
#             'root': '/parts_inventory/parts_inventory',
#             'objects': http.request.env['parts_inventory.parts_inventory'].search([]),
#         })

#     @http.route('/parts_inventory/parts_inventory/objects/<model("parts_inventory.parts_inventory"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('parts_inventory.object', {
#             'object': obj
#         })

