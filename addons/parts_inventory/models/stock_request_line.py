from odoo import fields, models

class StockRequestLine(models.Model):
    _name = 'parts.inventory.stock.request.line'
    _description = 'Stock Request Line'
    _order = 'request_id, part_id'

    # 反向連結回單頭，這是關鍵的 Many2one 欄位
    request_id = fields.Many2one(
        'parts.inventory.stock.request',
        string='Stock Request',
        required=True,
        ondelete='cascade'
    )
    # 連結到零件主檔
    part_id = fields.Many2one(
        'parts.inventory.part',
        string='Part',
        required=True
    )
    # 申請數量
    quantity = fields.Float(string='Quantity', required=True, default=1.0)
    # 零件在庫數量
    on_hand_quantity = fields.Float(
        string='On Hand Quantity',
        related='part_id.quantity',
        readonly=True
    )