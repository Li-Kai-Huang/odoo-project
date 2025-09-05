# Day 04 — 第一個自製模組：`team_management`（從 0 到看到選單）

今天的目標，是在 Odoo 17（Community）裡做出第一個**可安裝、可看到選單**的自製模組 `team_management`。過程中我遇到三個卡點：**容器/主機的寫入權限**、**沒有 Update Apps List**、以及 **manifest 與檔名不一致**。下面把可重現步驟與解法一次記錄。

---

## 1) 建骨架（scaffold）與權限處理

在容器裡用 scaffold 產生模組骨架（掛載到 `/mnt/extra-addons`）：

```bash
docker compose exec odoo odoo scaffold team_management /mnt/extra-addons
```

第一次會報 PermissionError: [Errno 13] Permission denied，因為目錄是容器內 odoo 使用者建立，主機帳號沒權限寫。解法（擇一）：

```bash
Copy code
# A. 把目錄所有權改回自己（建議）
sudo chown -R $USER:$USER addons/team_management

# B. 或暫時開放寫入（快速但不建議長期）
sudo chmod -R a+rw addons/team_management
小檢查：docker compose exec odoo ls -la /mnt/extra-addons/team_management 應能看到目錄與檔案。
```

## 2) 建立最小可用內容（models / views / access）

### 2.1 **manifest**.py

```python
Copy code
{
    "name": "Team Management",
    "version": "17.0.1.0.0",
    "summary": "Basic team and member management for competition",
    "author": "Me",
    "license": "LGPL-3",
    "category": "Tools",
    "depends": ["base"],
    "data": [
        "security/ir.model.access.csv",
        "views/team_views.xml",
        "views/member_views.xml",
    ],
    "installable": True,
    "application": True,
}
```

### 2.2 models/team.py

```python
Copy code
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
    role = fields.Selection([("coach","Coach"),("leader","Leader"),("member","Member")], default="member")
    team_id = fields.Many2one("team.management.team", ondelete="cascade")
```

### 2.3 views/team_views.xml

```xml
Copy code
<?xml version="1.0" encoding="utf-8"?>
<odoo>
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

  <record id="action_team_management" model="ir.actions.act_window">
    <field name="name">Teams</field>
    <field name="res_model">team.management.team</field>
    <field name="view_mode">tree,form</field>
  </record>

  <menuitem id="menu_team_root" name="Team Management" sequence="10"/>
  <menuitem id="menu_team" name="Teams" parent="menu_team_root" action="action_team_management"/>
</odoo>
```

### 2.4 views/member_views.xml

```xml
Copy code
<?xml version="1.0" encoding="utf-8"?>
<odoo>
  <record id="view_member_tree" model="ir.ui.view">
    <field name="name">team.management.member.tree</field>
    <field name="model">team.management.member</field>
    <field name="arch" type="xml">
      <tree>
        <field name="name"/>
        <field name="role"/>
        <field name="team_id"/>
      </tree>
    </field>
  </record>

  <record id="view_member_form" model="ir.ui.view">
    <field name="name">team.management.member.form</field>
    <field name="model">team.management.member</field>
    <field name="arch" type="xml">
      <form>
        <sheet>
          <group>
            <field name="name"/>
            <field name="role"/>
            <field name="team_id"/>
          </group>
        </sheet>
      </form>
    </field>
  </record>
</odoo>
```

### 2.5 security/ir.model.access.csv

```csv
Copy code
id,name,model_id:id,group_id:id,perm_read,perm_write,perm_create,perm_unlink
access_team,access_team_management_team,model_team_management_team,base.group_user,1,1,1,1
access_member,access_team_management_member,model_team_management_member,base.group_user,1,1,1,1
```

## 3) 更新 Apps、安裝/升級、驗收

### 重點 1：用對資料庫（建議 ironman）

如果只看到 postgres/db，代表還沒建立應用 DB。可用 Database Manager 新建，或指令：

```bash
Copy code
docker compose exec odoo odoo -c /etc/odoo/odoo.conf -d ironman -i base --without-demo=all --stop-after-init
docker compose up -d
```

### 重點 2：Update Apps List（沒更新會完全找不到模組）

UI：?debug=1 → Apps → 取消紫色篩選 → Update Apps List

指令（保險）：

```bash
Copy code
docker compose exec odoo bash -lc 'odoo shell -d ironman -c /etc/odoo/odoo.conf << "PY"
env["ir.module.module"].update_list()
PY'
安裝或升級
```

```bash
Copy code
docker compose exec odoo bash -lc 'odoo -c /etc/odoo/odoo.conf -d ironman -i team_management --stop-after-init' \
|| docker compose exec odoo bash -lc 'odoo -c /etc/odoo/odoo.conf -d ironman -u team_management --stop-after-init'
docker compose up -d
```

驗收

左上主選單應出現 Team Management → Teams。

建立 Team、在表單中新增 Members，CRUD 正常。

## 4) 今日踩雷與排除

```EACCES: permission denied：主機帳號對```

 ```ini
  addons/team_management 沒寫入權限 →
  ```

  ```bash
  sudo chown -R $ USER:$ USER addons/team_management。
  ```

找不到模組：忘了 Update Apps List 或用錯 DB（db/postgres 不是應用 DB）。

RPC_ERROR File not found: team_management/views/team_views.xml：manifest 的 data 指向的檔名不存在或大小寫不對 → 依上面檔名建立檔案，或改回 views/views.xml 但內容要包含 menuitem 與 act_window。

沒有 Developer Mode：網址要 <http://localhost:8069/web?debug=1（?debug=1> 要在 # 前）。

## 5) 今日心得

第一個模組的關鍵不是功能，而是讓框架把你當一個完整的 App：manifest 宣告依賴與資料檔、模型與權限、視圖和選單對齊。今天把 scaffold 到可見選單的整套流程跑通後，接下來就能自信地往庫存、人力、網站與 AI 管家延伸。

## 6) 明日預告（Day 05）

把 Team 與 Odoo 的 Project 串起來：在 team.management.team 增加 project_id 欄位，讓每個 Team 對應一個 Project，並在表單畫面加上連結與快速開啟按鈕。
