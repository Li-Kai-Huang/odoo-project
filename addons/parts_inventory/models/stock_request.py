from odoo import fields, models ,api

class StockRequest(models.Model):
    _name = 'parts.inventory.stock.request'
    _description = 'Stock Request'
    _order = 'name desc'

    name = fields.Char(
        string='Request No.',
        required=True,
        readonly=True,
        default='New'
    )
    # 連結到專案模組的任務
    task_id = fields.Many2one(
        'project.task',
        string='Project Task',
        required=True
    )
    # 連結到團隊管理模組的團隊
    team_id = fields.Many2one(
        'team.management.team',
        string='Requesting Team',
        required=True
    )
    # 領料單明細，這是關鍵的 One2many 欄位
    line_ids = fields.One2many(
        'parts.inventory.stock.request.line',
        'request_id',
        string='Request Lines'
    )
    # 緊急程度欄位
    urgency = fields.Selection([
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ], string='Urgency', default='medium')

    # 狀態流轉欄位
    state = fields.Selection([
        ('draft', 'Draft'),
        ('to_approve', 'To Approve'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('done', 'Done'),
        ('cancelled', 'Cancelled')
    ], string='Status', default='draft')
    
    # 備註
    note = fields.Text(string='Note')
    
    submitted_by = fields.Many2one("res.users", string="Submitted By", readonly=True)
        # 在 create 方法中自動產生流水號
    @api.model
    def create(self, vals):
        # 如果 name 還是 'New'，代表是新單據，就去抓流水號
        if vals.get('name', 'New') == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code('parts.inventory.stock.request') or 'New'
        result = super(StockRequest, self).create(vals)
        return result

    def action_approve(self):
        """
        覆寫 Odoo 預設的按鈕行為。
        當領料單被核准時，自動產生對應的 Stock Move。
        """
        for request in self:
            if request.state != 'to_approve':
                continue
            
            # 在這裡，我們將為每一筆領料單明細建立 Stock Move
            Move = self.env['parts.inventory.stock.move']
            for line in request.line_ids:
                # 建立一筆出庫異動
                move = Move.create({
                    'part_id': line.part_id.id,
                    'move_type': 'out',
                    'quantity': line.quantity,
                    'note': f"From Stock Request: {request.name}",
                })
            # 關鍵修改！我們現在只呼叫「送審」，而不是直接核准
            move.action_submit()

            # 最後，將領料單狀態設為已核准
            request.write({'state': 'approved'})
            
        # 送審（不動庫存）
    def action_submit(self):
        for rec in self:
            if rec.state != "draft":
                continue
            rec.write({
                "state": "to_approve",
                "submitted_by": self.env.user.id,
            })
    def action_reject(self):
        for request in self:
            if request.state == 'to_approve':
                request.write({'state': 'rejected'})
                