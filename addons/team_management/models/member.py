#-*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError

class TeamMember(models.Model):
    _name = "team.management.member"
    _description = "Team Member"

    name = fields.Char(string="Member Name", required=True)

    role = fields.Selection(
        [
            ("coach", "Coach"),
            ("leader", "Leader"),
            ("member", "Member"),
        ],
        string="Role",
        default="member",
        required=True,
    )

    # 關聯 Team（必填，刪 Team 連帶刪成員）
    team_id = fields.Many2one(
        "team.management.team",
        string="Team",
        required=True,
        ondelete="cascade",
    )

    # 連到系統使用者（之後做任務/權限很好用）
    user_id = fields.Many2one("res.users", string="Related User")

    # 同隊伍內成員名稱不可重複（DB 層約束）
    _sql_constraints = [
        (
            "uniq_member_name_per_team",
            "unique(name, team_id)",
            "Member name must be unique within the same team.",
        )
    ]

    # 表單選使用者時，若 name 還沒填，自動帶入使用者名稱
    @api.onchange("user_id")
    def _onchange_user_id(self):
        if self.user_id and not self.name:
            self.name = self.user_id.name

    # 業務規則：每個隊伍最多一位 Leader
    @api.constrains("role", "team_id")
    def _check_unique_leader(self):
        for rec in self:
            if rec.role == "leader" and rec.team_id:
                leaders = self.search_count([
                    ("team_id", "=", rec.team_id.id),
                    ("role", "=", "leader"),
                ])
                if leaders > 1:
                    raise ValidationError("Each team can only have one Leader.")
