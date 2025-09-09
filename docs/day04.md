# Day 04 — Odoo 模組結構完整解析與實作

昨天我已經完成了 Docker 環境架設，今天正式踏入 Odoo 的核心：**模組 (Module)**。  
在 Odoo 世界裡，模組是一切的基礎。不管是存貨、專案管理，還是我們自己要開發的功能，都必須透過模組來實現。  

本篇要好好把 Odoo 模組的結構、每個檔案的作用，以及怎麼去寫，完整解釋清楚。

---

## 1. 模組的檔案架構

在 Odoo 裡，每個模組都是一個資料夾，通常會長得像這樣：
```graphql
team_management/
├─ manifest.py ← 模組的「身分證」
├─ init.py ← 告訴 Python/Odoo 要載入哪些模組程式
├─ models/ ← 存放資料模型 (ORM)
│ ├─ init.py
│ └─ team.py
├─ views/ ← 畫面定義 (XML)
│ ├─ team_views.xml
│ └─ member_views.xml
├─ security/ ← 權限管理
│ └─ ir.model.access.csv
├─ demo/ ← 測試或展示用的假資料 (非必要)
└─ static/ ← 前端資源：JS/CSS/圖片 (非必要)

```
這些檔案彼此有分工，缺一不可。  
下面逐一解釋每種檔案的作用、範例與注意事項。

---

## 2. `__manifest__.py` — 模組的「身分證」

這個檔案是 Odoo 模組最重要的入口，沒有它 Odoo 根本不知道這個資料夾是一個模組。  
它的作用是 **描述模組的基本資訊**，以及 **告訴 Odoo 要載入哪些檔案**。

範例：

```python
{
    "name": "Team Management",
    "version": "17.0.1.0.0",
    "summary": "Basic team and member management for competition",
    "author": "Me",
    "website": "https://example.com",
    "license": "LGPL-3",
    "category": "Tools",
    "depends": ["base"],  # 模組依賴，沒有 base 就跑不起來
    "data": [
        "security/ir.model.access.csv",
        "views/team_views.xml",
        "views/member_views.xml",
    ],
    "installable": True,
    "application": True,
}
```
重點：

depends：列出依賴模組，否則 Odoo 會報錯（例如使用 project.project 卻沒 depends project）。

data：模組要載入的 XML/CSV，順序很重要，通常 security → views → data。

application=True：這個模組會在左上角主選單出現。

## 3. __init__.py — 匯入 Python 模組
這個檔案是 Python 的模組初始化檔。
在 Odoo 裡，它的作用是 告訴 Odoo 要去載入哪些 Python 檔。

範例：

```python
from . import models
```
在 models/__init__.py 裡：

```python
from . import team
```
這樣 Odoo 啟動時就會讀取 models/team.py。

## 4. Models — 定義資料結構 (ORM)
Models 是 Odoo 的核心，它會自動對應到資料庫。
每個模型就是一張資料表，欄位對應到表格的欄位。

範例：models/team.py

```python

from odoo import models, fields

class Team(models.Model):
    _name = "team.management.team"     # 模型技術名稱 → DB 表名 team_management_team
    _description = "Team"

    name = fields.Char(required=True)  # 隊伍名稱
    description = fields.Text()        # 描述
    member_ids = fields.One2many(      # 一個隊伍對多個成員
        "team.management.member", "team_id", string="Members"
    )

class Member(models.Model):
    _name = "team.management.member"
    _description = "Team Member"

    name = fields.Char(required=True)
    role = fields.Selection([("coach","Coach"),("leader","Leader"),("member","Member")], default="member")
    team_id = fields.Many2one("team.management.team", ondelete="cascade")  # 成員屬於一個隊伍

```
常見欄位型態：

Char：短字串

Text：長文字

Integer,Float,Boolean

Date、Datetime

Many2one：多對一

One2many：一對多

Many2many：多對多

## 5. Views — 定義畫面與選單 (XML)
Odoo 的畫面不是寫死的，而是透過 XML 定義。
常見的元素：

tree：清單

form：表單

kanban：卡片

ir.actions.act_window：定義點選單後打開的動作

menuitem：建立選單階層

範例：views/team_views.xml

```xml
<odoo>
  <!-- Tree View -->
  <record id="view_team_tree" model="ir.ui.view">
    <field name="name">team.management.team.tree</field>
    <field name="model">team.management.team</field>
    <field name="arch" type="xml">
      <tree>
        <field name="name"/>
        <field name="description"/>
      </tree>
    </field>
  </record>

  <!-- Form View -->
  <record id="view_team_form" model="ir.ui.view">
    <field name="name">team.management.team.form</field>
    <field name="model">team.management.team</field>
    <field name="arch" type="xml">
      <form>
        <sheet>
          <group>
            <field name="name"/>
            <field name="description"/>
            <field name="member_ids"/>
          </group>
        </sheet>
      </form>
    </field>
  </record>

  <!-- Action -->
  <record id="action_team_management" model="ir.actions.act_window">
    <field name="name">Teams</field>
    <field name="res_model">team.management.team</field>
    <field name="view_mode">tree,form</field>
  </record>

  <!-- Menu -->
  <menuitem id="menu_team_root" name="Team Management" sequence="10"/>
  <menuitem id="menu_team" name="Teams"
            parent="menu_team_root"
            action="action_team_management"/>
</odoo>
```
裝好模組後，UI 左上角就會出現 Team Management → Teams。

## 6. Security — 權限管理
沒有權限檔，使用者就算安裝模組也會遇到錯誤。
最基本的檔案是 ir.model.access.csv，定義 CRUD 權限。

範例：security/ir.model.access.csv

```csv
id,name,model_id:id,group_id:id,perm_read,perm_write,perm_create,perm_unlink
access_team,access_team_management_team,model_team_management_team,base.group_user,1,1,1,1
access_member,access_team_management_member,model_team_management_member,base.group_user,1,1,1,1
```
重點：

model_id:id 對應自動生成的模型 External ID，例如 model_team_management_team。

group_id:id 通常用 base.group_user（內部使用者群組）。

後面四個數字分別是 讀、寫、建立、刪除。

## 7. 其他檔案
demo/：可放假資料，讓安裝模組時自動建立一些範例。

static/：前端資源，例如自製 JS、CSS、圖片。通常寫前端整合才會用到。

## 8. 安裝與驗收流程
建立應用資料庫（不要用 postgres/db）

UI：Database Manager → 建立 ironman

CLI：odoo -d ironman -i base --without-demo=all --stop-after-init

Update Apps List

UI：Apps → Debug → Update Apps List

CLI：在 odoo shell 裡跑 env["ir.module.module"].update_list()

安裝模組

UI：搜尋 Team Management → Install

CLI：odoo -d ironman -i team_management --stop-after-init

驗收

左上有 Team Management → Teams

建立隊伍、成員，CRUD 正常

## 9. 今日心得
今天最大的收穫是徹底理解 Odoo 模組的骨架。
從 manifest 的身分證、models 的資料結構、views 的畫面描述，到 security 的權限設定，這些檔案缺一不可。

最常見的錯誤就是：

少了 ir.model.access.csv → 報權限錯誤

__manifest__.py 的 data 路徑錯 → FileNotFoundError

沒有 Update Apps List → 找不到模組

修正之後，我的模組終於出現在 UI 的主選單裡，這感覺就像完成了 Odoo 開發的第一個「Hello World」。

## 10. 明日預告（Day 05）
擴充模組：

加上 Kanban 視圖，讓成員管理更直觀

在 Team 表單加 Project Smart Button，把隊伍連結到 Odoo 的專案模組
這樣模組就能從「獨立小功能」變成「與原生應用整合」的實戰案例。