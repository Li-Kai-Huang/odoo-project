# Day 16 — 任務分派 & 即時進度回報設計

嗨，大家好！歡迎回到我們的 Odoo 開發旅程 🚀  

經過前幾天的奮戰，我們已經成功地把 **零件庫存** 與 **專案任務** 串聯起來，讓每一個領料申請都有了出處。  
但一個機器人隊伍的成功，從來不只是零件的管理，更重要的是 **「人」的協作**。  

今天我們要從更宏觀的角度出發：如何管理與追蹤每個隊員的任務？  

---

## 1) 為什麼要做任務分派與回報？

Odoo 原生的 Project 模組功能強大，但對於一個追求精實的機器人隊伍來說，它可能顯得過於複雜。  
我們不需要所有功能，只需要一個：  
- 簡單直觀  
- 隊員能快速回報進度  
- 教練能一目了然掌握專案狀態  

所以今天的核心，就是在 **project.task** 上建立兩座橋樑：  
👉 任務指派 ＋ 即時進度回報。  

---

## 2) 為什麼需要獨立的整合模組？

你可能會問：「這部分是不是應該獨立出來？不然之後整合 Dashboard 會出依賴問題吧？」  

這個問題非常專業！答案是肯定的。這正是 Odoo 模組化開發的精髓：**關注點分離 (Separation of Concerns)**。  

- **team_management** → 管理「人」與「團隊」  
- **parts_inventory** → 管理「零件」  
- **任務分派與回報** → 屬於「人」與「專案」的交集  

因此我們決定創建一個全新的輕量級模組：**project_team_integration**。  
這樣能保持架構清晰，也為 **Day 17 的 Dashboard** 打下堅實基礎。  

---

## 3) 實作：建立 project_team_integration 模組

### 3.1 新增 `__manifest__.py`

```python
# -*- coding: utf-8 -*-
{
    'name': "Project Team Integration",
    'summary': "Integrates Project and Task management with Team Management.",
    'description': "Adds fields and views to project.task for team assignment & progress tracking.",
    'author': "Your Name",
    'website': "http://www.yourwebsite.com",
    'category': 'Project',
    'version': '17.0.1.0.0',
    'depends': ['project', 'team_management'],
    'data': [
        'views/project_task_views.xml',
    ],
    'license': 'AGPL-3',
}
```

📌 關鍵：`depends` 中要同時寫入 `project` 和 `team_management`。  

---

### 3.2 新增 `models/project_task_inherit.py`

```python
# -*- coding: utf-8 -*-
from odoo import fields, models

class ProjectTask(models.Model):
    _inherit = "project.task"

    # 新增進度欄位
    progress = fields.Float(string="Progress (%)", group_operator="avg", default=0.0)
```

小提醒：別忘了在 `__init__.py` 中加入：  
```python
from . import project_task_inherit
```

---

### 3.3 新增 `views/project_task_views.xml`

```xml
<?xml version="1.0" encoding="utf-8"?>
<odoo>
    <record id="view_task_form_inherit_assignment" model="ir.ui.view">
        <field name="name">project.task.form.inherit.assignment</field>
        <field name="model">project.task</field>
        <field name="inherit_id" ref="project.view_task_form2"/>
        <field name="arch" type="xml">
            <xpath expr="//sheet/group" position="after">
                <group string="Task Assignment &amp; Progress">
                    <field name="user_ids" widget="many2many_tags" />
                    <field name="progress" widget="progressbar"/>
                </group>
            </xpath>
        </field>
    </record>

    <record id="view_task_kanban_inherit" model="ir.ui.view">
        <field name="name">project.task.kanban.inherit</field>
        <field name="model">project.task</field>
        <field name="inherit_id" ref="project.view_task_kanban"/>
        <field name="arch" type="xml">
            <xpath expr="//kanban/templates//ul" position="inside">
                <li t-if="record.user_ids.raw_value">
                    <field name="user_ids" widget="many2many_tags"/>
                </li>
                <li>
                    <field name="progress" widget="progressbar"/>
                </li>
            </xpath>
        </field>
    </record>
</odoo>
```

---

### 3.4 讓進度條動起來

`widget="progressbar"` 只是視覺化，並不會自動計算。  
因此需要 **隊員手動輸入進度值**（如 50%），再儲存。  

這樣的設計貼近真實情境：  
- 隊員回報進度 → 手動輸入數字  
- 系統更新進度條 → 教練即時掌握狀態  

---

## 4) 今日成果

- [x] 建立 **project_team_integration** 模組  
- [x] 在任務中新增 **進度欄位**  
- [x] 表單 / Kanban UI 中能同時顯示「指派人」與「進度」  
- [x] 架構清晰，為 Dashboard 打好基礎  

---

## 5) 今日心得

今天的收穫不是功能本身，而是 **架構設計的思維**。  
模組化、分層次，讓系統更容易維護與擴充。  
這比單純寫程式更有價值。  

---

## 6) 明日預告（Day 17）

明天我們將挑戰打造 **專屬的 Dashboard**！  
把「零件庫存」「任務狀態」「進度回報」全部整合到一個畫面，讓教練能一眼掌握全局。  
準備好迎接大整合吧 ⚡