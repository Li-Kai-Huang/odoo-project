from odoo import models, fields, api
from odoo.exceptions import ValidationError

class StockMove(models.Model):
    _name = "parts.inventory.stock.move"
    _description = "Stock Move"
    _order = "date desc, id desc"

    part_id = fields.Many2one("parts.inventory.part", required=True, ondelete="cascade")
    move_type = fields.Selection([("in","Stock In"),("out","Stock Out")], required=True, default="in")
    quantity = fields.Float(required=True)
    date = fields.Datetime(default=fields.Datetime.now)
    note = fields.Char()
    state = fields.Selection([("draft","Draft"),("confirmed","Confirmed"),("cancel","Cancelled")], default="draft")

    @api.constrains("quantity")
    def _check_qty(self):
        for r in self:
            if r.quantity <= 0:
                raise ValidationError("Quantity must be > 0.")

    def action_confirm(self):
        for r in self:
            if r.state != "draft":
                continue
            # 真正影響在 parts.inventory.part 的 compute（你已寫好）會自動反映
            # 這裡只需將狀態改為 confirmed
            r.state = "confirmed"

    def action_cancel(self):
        for r in self:
            # 若你要允許「已確認可回滾」，單純把狀態設為 cancel
            if r.state == "confirmed":
                r.state = "cancel"
            elif r.state == "draft":
                r.state = "cancel"
