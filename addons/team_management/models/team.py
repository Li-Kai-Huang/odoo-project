from odoo import models, fields, api

class Team(models.Model):
    _name = "team.management.team"
    _description = "Team"

    name = fields.Char(required=True)
    description = fields.Text()
    member_ids = fields.One2many("team.management.member", "team_id", string="Members")
    project_id = fields.Many2one("project.project", string="Related Project")

    # Day06: 計算欄位（成員數）
    member_count = fields.Integer(string="Member Count", compute="_compute_member_count", store=True)

    @api.depends("member_ids")
    def _compute_member_count(self):
        for rec in self:
            rec.member_count = len(rec.member_ids)

    def action_open_project(self):
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


class Member(models.Model):
    _name = "team.management.member"
    _description = "Team Member"

    name = fields.Char(required=True)
    role = fields.Selection(
        [("coach","Coach"),("leader","Leader"),("member","Member")],
        default="member",
    )
    team_id = fields.Many2one("team.management.team", string="Team", ondelete="cascade", required=True)

    # Day06: 連到系統使用者（之後做任務/權限很方便）
    user_id = fields.Many2one("res.users", string="Related User")

    # Day06: 選了使用者自動帶入名字
    @api.onchange("user_id")
    def _onchange_user_id(self):
        if self.user_id and not self.name:
            self.name = self.user_id.name

    # Day06: 唯一性（同一隊伍內成員名稱不可重複）
    _sql_constraints = [
        ("uniq_member_name_per_team",
         "unique(name, team_id)",
         "Member name must be unique within the same team.")
    ]
