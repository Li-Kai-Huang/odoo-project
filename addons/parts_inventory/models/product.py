from odoo import models, fields

class ProductTemplate(models.Model):
    _inherit = "product.template"

    team_id = fields.Many2one("team.management.team", string="Team")

    def action_open_quick_move_wizard(self):
        """在產品頁點 Quick Move 時開你現有的精靈，並預帶產品→零件對應"""
        self.ensure_one()
        # 這裡視你的對應而定：若你用自製 Part 管理庫存，可用 code 或其它邏輯找到對應 Part
        Part = self.env["parts.inventory.part"]
        part = Part.search([("code", "=", self.default_code)], limit=1)
        # 找不到就不讓開
        if not part:
            return {
                "type": "ir.actions.client",
                "tag": "display_notification",
                "params": {
                    "title": "No Part",
                    "message": "找不到對應的 Part（依 default_code 對應）。",
                    "type": "warning",
                },
            }
        return {
            "type": "ir.actions.act_window",
            "res_model": "parts.inventory.quick.move.wizard",
            "view_mode": "form",
            "target": "new",
            "context": {
                "default_part_id": part.id,
                "default_move_type": "in",
            },
        }
