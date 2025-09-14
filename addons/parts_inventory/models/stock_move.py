# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError, AccessError

class StockMove(models.Model):
    _name = "parts.inventory.stock.move"
    _description = "Stock Move"
    _order = "date desc, id desc"

    part_id = fields.Many2one("parts.inventory.part", string="Part", required=True, ondelete="cascade")
    move_type = fields.Selection([("in", "Stock In"), ("out", "Stock Out")], required=True, default="in")
    quantity = fields.Float(string="Quantity", required=True)
    note = fields.Char(string="Note")
    date = fields.Datetime(string="Date", default=fields.Datetime.now)

    state = fields.Selection([
        ("draft", "Draft"),
        ("to_approve", "To Approve"),
        ("approved", "Approved"),
        ("rejected", "Rejected"),
        ("cancel", "Cancelled"),
    ], default="draft", string="Status")

    submitted_by = fields.Many2one("res.users", string="Submitted By", readonly=True)
    approved_by = fields.Many2one("res.users", string="Approved By", readonly=True)
    approved_date = fields.Datetime(string="Approved On", readonly=True)

    @api.constrains("quantity")
    def _check_qty_positive(self):
        for rec in self:
            if rec.quantity <= 0:
                raise ValidationError("Quantity must be > 0.")

    # 送審（不動庫存）
    def action_submit(self):
        for rec in self:
            if rec.state != "draft":
                continue
            rec.write({
                "state": "to_approve",
                "submitted_by": self.env.user.id,
            })

    # 核准（這裡才動庫存）
    def action_approve(self):
        if not self.env.user.has_group("parts_inventory.group_parts_manager"):
            raise AccessError("Only Parts Manager can approve.")
        for rec in self:
            if rec.state != "to_approve":
                continue
            part = rec.part_id.sudo()
            if rec.move_type == "in":
                part.quantity += rec.quantity
            else:
                if part.quantity < rec.quantity:
                    raise ValidationError("Not enough stock to move out.")
                part.quantity -= rec.quantity
            rec.write({
                "state": "approved",
                "approved_by": self.env.user.id,
                "approved_date": fields.Datetime.now(),
            })

    # 退回（不動庫存）
    def action_reject(self):
        if not self.env.user.has_group("parts_inventory.group_parts_manager"):
            raise AccessError("Only Parts Manager can reject.")
        for rec in self:
            if rec.state == "to_approve":
                rec.write({"state": "rejected"})

    # ✅ 容錯：某些舊呼叫仍用 action_confirm
    # 一般使用者：當成送審；Manager：送審後立刻核准
    def action_confirm(self):
        for rec in self:
            if rec.state != "draft":
                continue
            rec.action_submit()
            if self.env.user.has_group("parts_inventory.group_parts_manager"):
                rec.action_approve()
