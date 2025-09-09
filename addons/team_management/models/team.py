from odoo import models, fields

class Team(models.Model):
    _name = "team.management.team"
    _description = "Team"

    name = fields.Char(required=True)
    description = fields.Text()
    member_ids = fields.One2many("team.management.member", "team_id", string="Members")
    project_id = fields.Many2one("project.project", string="Related Project")

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
    role = fields.Selection([("coach","Coach"),("leader","Leader"),("member","Member")], default="member")
    team_id = fields.Many2one("team.management.team", string="Team", ondelete="cascade", required=True)
