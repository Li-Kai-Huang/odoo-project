from odoo import models, fields, api

class QuickMoveWizard(models.TransientModel):
    _name = "parts.inventory.quick.move.wizard"
    _description = "Quick Move Wizard"

    part_id = fields.Many2one("parts.inventory.part", required=True)
    move_type = fields.Selection([("in","Stock In"),("out","Stock Out")], default="in", required=True)
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
            move.action_confirm()
        return {"type": "ir.actions.act_window_close"}
