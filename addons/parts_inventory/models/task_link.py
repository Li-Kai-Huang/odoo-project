# -*- coding: utf-8 -*-
from odoo import models, fields

class ProjectTask(models.Model):
    _inherit = "project.task"

    part_id = fields.Many2one(
        "parts.inventory.part",
        string="Related Part",
        index=True,
        help="Link this task to a specific part from Parts Inventory."
    )
    # 方便在 Task 看 Part 的 Team（唯讀）
    part_team_id = fields.Many2one(
        related="part_id.team_id",
        string="Part Team",
        readonly=True,
        store=False,
    )
