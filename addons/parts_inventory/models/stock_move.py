from odoo import models, fields, api
from odoo.exceptions import ValidationError

class StockMove(models.Model):
    _name = "parts.inventory.stock.move"
    _description = "Stock Move"
    _order = "date desc, id desc"

    part_id = fields.Many2one(
        "parts.inventory.part",
        string="Part",
        required=True,
        ondelete="cascade"
    )
    team_id = fields.Many2one(related="part_id.team_id", store=True, string="Team")
    move_type = fields.Selection(
        [("in", "Stock In"), ("out", "Stock Out")],
        string="Move Type",
        required=True,
        default="in",
    )
    quantity = fields.Float(string="Quantity", required=True)
    note = fields.Char(string="Note")
    date = fields.Datetime(string="Date", default=fields.Datetime.now)
    state = fields.Selection(
        [("draft", "Draft"), ("confirmed", "Confirmed"), ("cancel", "Cancelled")],
        default="draft",
        string="Status",
    )

    @api.constrains("quantity")
    def _check_qty_positive(self):
        for rec in self:
            if rec.quantity <= 0:
                raise ValidationError("Quantity must be > 0.")

    def action_confirm(self):
        for rec in self:
            if rec.state != "draft":
                continue
            part = rec.part_id.sudo()
            if rec.move_type == "in":
                part.quantity += rec.quantity
            else:
                if part.quantity < rec.quantity:
                    raise ValidationError("Not enough stock to move out.")
                part.quantity -= rec.quantity
            rec.state = "confirmed"

    def action_cancel(self):
        for rec in self:
            if rec.state != "confirmed":
                rec.state = "cancel"
                continue
            part = rec.part_id.sudo()
            if rec.move_type == "in":
                if part.quantity < rec.quantity:
                    raise ValidationError("Cannot cancel: stock not enough to revert.")
                part.quantity -= rec.quantity
            else:
                part.quantity += rec.quantity
            rec.state = "cancel"
