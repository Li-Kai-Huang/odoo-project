from odoo import models, fields, api
from odoo.exceptions import ValidationError

class ExportMovesWizard(models.TransientModel):
    _name = "parts.inventory.export.moves.wizard"
    _description = "Export Part Moves Wizard"

    # 來源：從 Part 打開時，預設會帶 active_id 進來（我們之前在 action 有 context）
    part_id = fields.Many2one("parts.inventory.part", string="Part")
    team_id = fields.Many2one("team.management.team", string="Team")

    date_from = fields.Date(string="Date From", required=True)
    date_to   = fields.Date(string="Date To", required=True)

    export_format = fields.Selection(
        [("xlsx", "Excel (.xlsx)"), ("csv", "CSV")],
        string="Format",
        required=True,
        default="xlsx",
    )
    include_note = fields.Boolean(string="Include Note", default=True)

    @api.constrains("date_from", "date_to")
    def _check_dates(self):
        for w in self:
            if w.date_from and w.date_to and w.date_from > w.date_to:
                raise ValidationError("Date From must be <= Date To.")

    def action_export(self):
        """先回傳一個篩選後的清單畫面（之後要做真正匯出再加）。"""
        self.ensure_one()
        domain = [("date", ">=", self.date_from), ("date", "<=", self.date_to)]
        if self.part_id:
            domain.append(("part_id", "=", self.part_id.id))
        if self.team_id:
            domain.append(("team_id", "=", self.team_id.id))

        return {
            "type": "ir.actions.act_window",
            "name": "Filtered Moves",
            "res_model": "parts.inventory.stock.move",
            "view_mode": "tree,form",
            "domain": domain,
            "target": "current",
        }
