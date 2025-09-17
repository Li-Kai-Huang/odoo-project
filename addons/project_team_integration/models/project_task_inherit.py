# -*- coding: utf-8 -*-
from odoo import fields, models

class ProjectTask(models.Model):
    _inherit = "project.task" # 關鍵：繼承 project.task 模型

    # 新增進度欄位
    progress = fields.Float(string="Progress (%)", group_operator="avg", default=0.0)