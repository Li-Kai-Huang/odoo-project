# -*- coding: utf-8 -*-
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

    # 關聯 Team（必填，刪除團隊時連帶刪除成員）
    team_id = fields.Many2one(
        "team.management.team",
        string="Team",
        required=True,
        ondelete="cascade",
    )

    # 連到系統使用者，建立與 `res.users` 模型的關聯
    user_id = fields.Many2one("res.users", string="Related User")

    # DB 層約束：同隊伍內成員名稱不可重複
    _sql_constraints = [
        (
            "uniq_member_name_per_team",
            "unique(name, team_id)",
            "Member name must be unique within the same team.",
        )
    ]

    @api.onchange("user_id")
    def _onchange_user_id(self):
        """
        當在表單中選擇 Odoo 使用者時，如果「成員名稱」欄位為空，
        則自動填入該使用者的名稱。
        """
        if self.user_id and not self.name:
            self.name = self.user_id.name

    @api.onchange("user_id", "role")
    def _onchange_user_group(self):
        """
        當使用者或角色改變時，自動更新相關聯的 Odoo 使用者群組。
        - 教練會獲得所有群組（coach, leader, member）
        - 隊長會獲得 leader 和 member 群組
        - 成員只會獲得 member 群組
        """
        if self.user_id:
            # 取得所有相關的群組
            coach_group = self.env.ref('team_management.group_team_coach')
            leader_group = self.env.ref('team_management.group_team_leader')
            member_group = self.env.ref('team_management.group_team_member')

            # 移除所有 team_management 相關的群組，確保權限不會累積
            all_tm_groups = coach_group | leader_group | member_group
            self.user_id.groups_id -= all_tm_groups

            # 根據角色分配新的群組
            if self.role == 'coach':
                self.user_id.groups_id |= coach_group | leader_group | member_group
            elif self.role == 'leader':
                self.user_id.groups_id |= leader_group | member_group
            else: # self.role == 'member'
                self.user_id.groups_id |= member_group

    @api.constrains("role", "team_id")
    def _check_unique_leader(self):
        """業務規則：確保每個隊伍最多只有一位隊長"""
        for rec in self:
            if rec.role == "leader" and rec.team_id:
                leaders = self.search_count([
                    ("team_id", "=", rec.team_id.id),
                    ("role", "=", "leader"),
                ])
                if leaders > 1:
                    raise ValidationError("Each team can only have one Leader.")