from odoo import models, fields

class Part(models.Model):
    _name = "parts.inventory.part"
    _description = "Part"

    name = fields.Char(string="Part Name", required=True)
    code = fields.Char(string="Part Code", required=True)
    description = fields.Text(string="Description")
    quantity = fields.Float(string="Quantity in Stock", default=0.0)
    team_id = fields.Many2one("team.management.team", string="Team")
    active = fields.Boolean(string="Active", default=True)

    # <<< 新增：表單底下要顯示的異動明細 >>>
    move_ids = fields.One2many(
        "parts.inventory.stock.move", "part_id", string="Stock Moves", readonly=True
    )

    _sql_constraints = [
        ("uniq_part_code", "unique(code)", "Part code must be unique."),
    ]
