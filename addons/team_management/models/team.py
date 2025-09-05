from odoo import models, fields

class Team(models.Model):
    _name = "team.management.team"
    _description = "Team"

    name = fields.Char(required=True)
    description = fields.Text()
    member_ids = fields.One2many("team.management.member", "team_id", string="Members")

class Member(models.Model):
    _name = "team.management.member"
    _description = "Team Member"

    name = fields.Char(required=True)
    role = fields.Selection(
        [("coach","Coach"),("leader","Leader"),("member","Member")],
        default="member",
    )
    team_id = fields.Many2one("team.management.team", ondelete="cascade")
