# -*- coding: utf-8 -*-
from odoo import models, fields, api

class Team(models.Model):
    _name = "team.management.team"
    _description = "Team"

    name = fields.Char(string="Team Name", required=True)
    description = fields.Text(string="Description")

    # 與 Project 的關聯（可選用，但若啟用，需安裝 Project 模組）
    project_id = fields.Many2one("project.project", string="Related Project")

    # 成員一對多，使用 `team.management.member` 模型
    member_ids = fields.One2many(
        "team.management.member",
        "team_id",
        string="Members"
    )

    # 計算欄位：成員數，會自動計算 member_ids 的數量
    member_count = fields.Integer(
        string="Member Count",
        compute="_compute_member_count",
        store=True
    )

    @api.depends("member_ids")
    def _compute_member_count(self):
        """根據關聯的成員數量來計算成員數"""
        for rec in self:
            rec.member_count = len(rec.member_ids)

    def action_open_project(self):
        """表單右上角按鈕：若有 project_id 就打開專案表單"""
        self.ensure_one()
        if not self.project_id:
            return {"type": "ir.actions.act_window_close"}
        return {
            "type": "ir.actions.act_window",
            "name": "Project",
            "res_model": "project.project",
            "view_mode": "form",
            "res_id": self.project_id.id,
            "target": "current",
        }