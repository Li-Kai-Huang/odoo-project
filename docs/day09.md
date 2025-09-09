# Day 09 — 建立「零件庫存」模組：Parts / Stock

今天我們把零件當主角，把庫存當配角，設計一個最小可用的庫存流。目標是：  

- `Part`（零件主檔）  
- `StockMove`（入／出庫紀錄）  
- 確認時自動更新 `Part.quantity`，出庫不足就禁止。

---

## 1) 我們要解哪個痛？

- 隊伍比賽時，螺絲、馬達、線材常常「用完才發現」。  
- 一張 Google Sheet 不是不能用，但沒有流程保障：誰加誰扣？扣完有沒有不夠？  
- 透過 Odoo ORM，我們實現基本的入庫 / 出庫流程，避免錯誤操作。

---

## 2) Models：兩個資料表

### `parts.inventory.part`

- **欄位**：`name`、`code`（唯一）、`description`、`quantity`、`team_id`、`active`  
- **設計重點**：  
  - `code` 唯一，避免重複。  
  - `quantity` 表示現況庫存。

```python
from odoo import models, fields

class Part(models.Model):
    _name = "parts.inventory.part"
    _description = "Part"
    _order = "code, id"

    name = fields.Char(string="Part Name", required=True)
    code = fields.Char(string="Part Code", required=True, index=True)
    description = fields.Text(string="Description")
    quantity = fields.Float(string="Quantity in Stock", default=0.0)
    team_id = fields.Many2one("team.management.team", string="Team")
    active = fields.Boolean(string="Active", default=True)

    _sql_constraints = [
        ("uniq_part_code", "unique(code)", "Part code must be unique."),
    ]
```

### `parts.inventory.stock.move`

- **欄位**：`part_id`、`move_type`、`quantity`、`note`、`date`、`state`  
- **流程**：  
  - 新建 → `draft`  
  - 確認 → `confirmed`，更新 `Part.quantity`  
  - 取消 → `cancel`，已確認則回滾庫存

```python
from odoo import models, fields, api
from odoo.exceptions import ValidationError

class StockMove(models.Model):
    _name = "parts.inventory.stock.move"
    _description = "Stock Move"
    _order = "date desc, id desc"

    part_id = fields.Many2one("parts.inventory.part", string="Part", required=True, ondelete="cascade")
    team_id = fields.Many2one(related="part_id.team_id", store=True, string="Team")
    move_type = fields.Selection([("in", "Stock In"), ("out", "Stock Out")],
                                 string="Move Type", required=True, default="in")
    quantity = fields.Float(string="Quantity", required=True)
    note = fields.Char(string="Note")
    date = fields.Datetime(string="Date", default=fields.Datetime.now)
    state = fields.Selection([("draft","Draft"),("confirmed","Confirmed"),("cancel","Cancelled")],
                             default="draft", string="Status")

    @api.constrains("quantity")
    def _check_qty_positive(self):
        for rec in self:
            if rec.quantity <= 0:
                raise ValidationError("Quantity must be > 0.")

    def action_confirm(self):
        for rec in self:
            if rec.state != "draft":
                continue
            if not rec.part_id:
                raise ValidationError("Part is required.")
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
            if rec.state == "cancel":
                continue
            part = rec.part_id.sudo()
            if rec.state == "confirmed":
                if rec.move_type == "in":
                    if part.quantity < rec.quantity:
                        raise ValidationError("Cannot cancel: stock not enough to revert.")
                    part.quantity -= rec.quantity
                else:
                    part.quantity += rec.quantity
            rec.state = "cancel"
```

---

## 3) 測試方法

進入 Odoo Shell：

```bash
docker compose exec odoo bash -lc 'odoo shell -d db -c /etc/odoo/odoo.conf'
```

測試 CRUD：

```python
env.cr.rollback()

Part = env['parts.inventory.part']
Move = env['parts.inventory.stock.move']

# 找不到就建立
p = Part.search([('code','=','M3-001')], limit=1) or Part.create({
    'name': 'M3 Screw',
    'code': 'M3-001',
    'description': '測試螺絲',
    'quantity': 0.0,
})
print("Part:", p.id, p.code, p.name, "qty:", p.quantity)

# 入庫 10
m_in = Move.create({'part_id': p.id, 'move_type': 'in', 'quantity': 10, 'note': '初次入庫'})
m_in.action_confirm()
p = Part.browse(p.id).with_context(prefetch_fields=False)
print("After IN 10 → qty:", p.read(['quantity'])[0]['quantity'])

# 出庫 4
m_out = Move.create({'part_id': p.id, 'move_type': 'out', 'quantity': 4, 'note': '領料'})
m_out.action_confirm()
p = Part.browse(p.id).with_context(prefetch_fields=False)
print("After OUT 4 → qty:", p.read(['quantity'])[0]['quantity'])

# 過量出庫
env.cr.rollback()
try:
    Move.create({'part_id': p.id, 'move_type': 'out', 'quantity': 999}).action_confirm()
except Exception as e:
    print("Expected:", type(e).__name__, str(e)[:120], "...")
```

---

## 4) 今日驗收清單

- [x] `parts_inventory` 模組安裝成功  
- [x] `Part` / `StockMove` 模型可用  
- [x] 入庫會加數量  
- [x] 出庫會減數量  
- [x] 出庫不足會報錯  
- [x] 取消可回滾  

---

## 5) 明日預告（Day 10）

進一步設計入庫／出庫流程：  

- 加上操作向導（Wizard）  
- 在 Part 表單加按鈕快速操作  
- 思考不同隊伍之間的獨立庫存管理
