from odoo import models, fields

class Part(models.Model):
    _name = "parts.inventory.part"
    _description = "Part"

    name = fields.Char(required=True)
    code = fields.Char(required=True)
    description = fields.Text()
    quantity = fields.Float(default=0.0)
    team_id = fields.Many2one("team.management.team")
    active = fields.Boolean(default=True)

    # 關鍵：一定要有正確的 one2many 反向欄位
    move_ids = fields.One2many(
        "parts.inventory.stock.move",  # 目標模型
        "part_id",                     # 反向 Many2one 欄位名 ← 必須跟 Move 裡的一致
        string="Stock Moves",
    )

    _sql_constraints = [
        ("uniq_part_code", "unique(code)", "Part code must be unique."),
    ]
