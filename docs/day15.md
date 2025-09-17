# Day 15 — Odoo Project / Task 模組應用：任務領料

大家好，歡迎回到我們的開發旅程！  

經過前幾天的努力，我們已經把「零件庫存」這個模組打造得有模有樣了。  
但一個好的系統，不應該是各自為政的獨立模組。在真實的工作情境中，專案經理或工程師們在執行任務時，往往需要向倉管申請零件，若這個流程沒有被整合進系統，就可能導致混亂與溝通成本。  

今天的任務，就是打造一座堅固的橋樑，將 Project / Task 模組與我們的 Parts Inventory 模組無縫串聯起來。  
這個橋樑，我們稱之為 **任務領料單 (Stock Request)**。  

---

## 1. 核心思想：讓申請流程更嚴謹

一個好的領料流程，不僅要有效率，更要權責分明。  
我們設計了一個 **兩階段審核機制**，確保每一筆庫存異動都有人負責：

- **第一階段 (管理者審核)**：專案成員發起領料申請，由管理者核准或駁回，代表「同意這份申請」。  
- **第二階段 (倉管審核)**：管理者核准後，系統會自動產生一張「待審核的庫存異動單」，交由倉管人員進行最終核准，代表「同意出庫並實際修改庫存」。  

這樣的設計確保了管理者負責需求審核，而倉管人員負責確認庫存與出貨，避免權責不明或重複審核的問題。  

---

## 2. 實作：讓程式碼動起來

要實現這個功能，我們需要新增三個檔案，並對現有模組做調整。

### 2.1 建立領料單流水號 (data/sequence.xml)

為了讓每張領料單都有獨一無二的編號，我們建立一個自動流水號規則：  

**data/sequence.xml**

```xml
<?xml version="1.0" encoding="utf-8"?>
<odoo>
    <data noupdate="1">
        <record id="parts_inventory_stock_request_sequence" model="ir.sequence">
            <field name="name">Stock Request Sequence</field>
            <field name="code">parts.inventory.stock.request</field>
            <field name="prefix">REQ</field>
            <field name="padding">5</field>
            <field name="company_id" eval="False"/>
        </record>
    </data>
</odoo>
```

📌 小提醒：別忘了將這個檔案加入 `__manifest__.py` 的 `data` 列表中。  

### 2.2 定義領料單模型

我們需要兩個模型：`StockRequest` 與 `StockRequestLine`。  

**models/stock_request_line.py**

```python
from odoo import fields, models

class StockRequestLine(models.Model):
    _name = 'parts.inventory.stock.request.line'
    _description = 'Stock Request Line'
    _order = 'request_id, part_id'

    request_id = fields.Many2one(
        'parts.inventory.stock.request',
        string='Stock Request',
        required=True,
        ondelete='cascade'
    )
    part_id = fields.Many2one(
        'parts.inventory.part',
        string='Part',
        required=True
    )
    quantity = fields.Float(string='Quantity', required=True, default=1.0)
    on_hand_quantity = fields.Float(
        string='On Hand Quantity',
        related='part_id.quantity',
        readonly=True
    )
```

**models/stock_request.py**  

```python
from odoo import fields, models, api

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
    task_id = fields.Many2one(
        'project.task',
        string='Project Task',
        required=True
    )
    team_id = fields.Many2one(
        'team.management.team',
        string='Requesting Team',
        required=True
    )
    line_ids = fields.One2many(
        'parts.inventory.stock.request.line',
        'request_id',
        string='Request Lines'
    )
    urgency = fields.Selection([
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ], string='Urgency', default='medium')

    state = fields.Selection([
        ('draft', 'Draft'),
        ('to_approve', 'To Approve'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('done', 'Done'),
        ('cancelled', 'Cancelled')
    ], string='Status', default='draft')
    
    note = fields.Text(string='Note')

    # ========== 按鈕方法 ==========
    @api.model
    def create(self, vals):
        if vals.get('name', 'New') == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code('parts.inventory.stock.request') or 'New'
        return super().create(vals)
        
    def action_submit(self):
        for rec in self:
            rec.write({'state': 'to_approve'})

    def action_approve(self):
        for request in self:
            if request.state != 'to_approve':
                continue
            
            Move = self.env['parts.inventory.stock.move']
            for line in request.line_ids:
                move = Move.create({
                    'part_id': line.part_id.id,
                    'move_type': 'out',
                    'quantity': line.quantity,
                    'note': f"From Stock Request: {request.name}",
                })
                move.action_submit()  # 自動送審庫存異動單

            request.write({'state': 'approved'})

    def action_reject(self):
        for request in self:
            if request.state == 'to_approve':
                request.write({'state': 'rejected'})
```

### 2.3 建立使用者介面 (views/stock_request_views.xml)

最後，我們替領料單打造 UI：  

**views/stock_request_views.xml**

```xml
<?xml version="1.0" encoding="utf-8"?>
<odoo>
    <data>
        <record id="action_stock_request" model="ir.actions.act_window">
            <field name="name">Stock Requests</field>
            <field name="res_model">parts.inventory.stock.request</field>
            <field name="view_mode">tree,form</field>
            <field name="help" type="html">
                <p class="o_view_nocontent_smiling_face">
                    Create a new stock request
                </p>
            </field>
        </record>

        <menuitem id="menu_stock_requests"
                  name="Stock Requests"
                  parent="menu_parts_root"
                  action="action_stock_request"
                  sequence="10"/>
        
        <record id="view_stock_request_tree" model="ir.ui.view">
            <field name="name">parts.inventory.stock.request.tree</field>
            <field name="model">parts.inventory.stock.request</field>
            <field name="arch" type="xml">
                <tree string="Stock Requests">
                    <field name="name"/>
                    <field name="task_id"/>
                    <field name="team_id"/>
                    <field name="urgency"/>
                    <field name="state"/>
                </tree>
            </field>
        </record>

        <record id="view_stock_request_form" model="ir.ui.view">
            <field name="name">parts.inventory.stock.request.form</field>
            <field name="model">parts.inventory.stock.request</field>
            <field name="arch" type="xml">
                <form string="Stock Request">
                    <header>
                        <button name="action_submit" type="object" string="Submit"
                                class="oe_highlight" invisible="state != 'draft'"/>
                        <button name="action_approve" type="object" string="Approve"
                                class="oe_highlight" invisible="state != 'to_approve'"
                                groups="parts_inventory.group_parts_manager"/>
                        <button name="action_reject" type="object" string="Reject"
                                class="btn-secondary" invisible="state != 'to_approve'"
                                groups="parts_inventory.group_parts_manager"/>
                        
                        <field name="state" widget="statusbar"/>
                    </header>
                    <sheet>
                        <div class="oe_title">
                            <h1>
                                <field name="name" readonly="1"/>
                            </h1>
                        </div>
                        <group>
                            <group>
                                <field name="task_id"/>
                                <field name="team_id"/>
                            </group>
                            <group>
                                <field name="urgency"/>
                            </group>
                        </group>
                        <notebook>
                            <page string="Request Lines">
                                <field name="line_ids">
                                    <tree editable="bottom">
                                        <field name="part_id"/>
                                        <field name="quantity"/>
                                        <field name="on_hand_quantity"/>
                                    </tree>
                                </field>
                            </page>
                            <page string="Notes">
                                <field name="note"/>
                            </page>
                        </notebook>
                    </sheet>
                </form>
            </field>
        </record>
    </data>
</odoo>
```

---

## 3. 收尾工作

別忘了更新 `__init__.py` 與 `__manifest__.py`，確保所有新檔案正確載入。  

完成後，你的專案就擁有了一個嚴謹又實用的 **任務領料流程**，讓團隊協作更順暢！  

---

## 4. 今日心得

今天的重點在於 **模組之間的整合**。  
光有 Parts Inventory 還不夠，當它能與 Project / Task 緊密互動，才真正展現出 Odoo 的威力。  
這也讓我更深刻體會到：Odoo 的價值並不是單一模組，而是模組之間的互聯網絡。  

---

## 5. 明日預告（Day 16）

我們將會進一步延伸，讓庫存異動單與任務之間有更強的追蹤關係，並嘗試加入 **通知與自動化流程**，讓系統更貼近實際業務需求。