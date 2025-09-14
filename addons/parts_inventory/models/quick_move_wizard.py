# -*- coding: utf-8 -*-
from odoo import models, fields

class ExportMovesWizard(models.TransientModel):
    _name = "parts.inventory.export.moves.wizard"
    _description = "Quick Move Wizard"

    part_id = fields.Many2one("parts.inventory.part", required=True)
    move_type = fields.Selection([("in", "Stock In"), ("out", "Stock Out")], default="in", required=True)
    quantity = fields.Float(required=True, default=1.0)
    note = fields.Char()

    def action_apply(self):
        Move = self.env["parts.inventory.stock.move"]
        for w in self:
            move = Move.create({
                "part_id": w.part_id.id,
                "move_type": w.move_type,
                "quantity": w.quantity,
                "note": w.note,
            })
            # ➜ 走審核流程：先送審（不動庫存）
            move.action_submit()
        return {"type": "ir.actions.act_window_close"}
