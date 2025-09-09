# Day 06 — Odoo ORM 基礎：Model / Field / Record

今天要進入 Odoo 的靈魂 — **ORM（Object Relational Mapping）**。  
白話一點：就是「不需要寫 SQL，照樣能呼風喚雨地操控資料庫」。  
想像一下，你只要在 Python 裡定義一個類別，Odoo 會乖乖幫你在 PostgreSQL 生出一張表，還附送增刪改查的 API，這感覺是不是有點像自動煮飯機？你只要丟米和水，白飯就熱騰騰上桌。

---

## 1) Model：你的資料表分身

在 Odoo，Model ≈ Table。不同的繼承類型，對應不同場景：

- **`models.Model`** → 正式住戶，真的會在資料庫蓋房子（建 table）。  
- **`models.TransientModel`** → 臨時帳篷，通常 Wizard 用完就消失。  
- **`models.AbstractModel`** → 純工具人，自己不能住，專門給別人繼承。  

範例：
```python
class Team(models.Model):
    _name = "team.management.team"
    _description = "Team"

    name = fields.Char(string="Name", required=True)
    description = fields.Text(string="Description")
```
👉 一瞬間，你就多了一張 `team_management_team` 表。很省事對吧？

---

## 2) Field：決定這棟房子裡有什麼家具

Field = 欄位，就是每張表的家具配置。  

- **基本款**：  
  - `Char`：短文字（沙發）  
  - `Text`：長文字（衣櫃）  
  - `Integer` / `Float`：數字（計算機）  
  - `Boolean`：布林值（開關）  
  - `Date` / `Datetime`：日期時間（時鐘）  

- **進階款（關聯）**：  
  - `Many2one`：多對一（房客 → 房東）  
  - `One2many`：一對多（房東 → 房客）  
  - `Many2many`：多對多（室友互相串門子）  

範例：
```python
class TeamMember(models.Model):
    _name = "team.management.member"
    _description = "Team Member"

    name = fields.Char(string="Member Name", required=True)
    role = fields.Selection([
        ("leader", "Leader"),
        ("member", "Member"),
    ], string="Role", default="member")

    team_id = fields.Many2one("team.management.team", string="Team")
```

---

## 3) Record：開始操控資料吧！

Record 就是「這張表的一筆資料」，操作起來像操控 Python 物件一樣簡單。

```python
# 建立
team = env["team.management.team"].create({
    "name": "Ironman Devs",
    "description": "專案鐵人賽小組"
})

# 查詢
teams = env["team.management.team"].search([("name", "ilike", "ironman")])

# 更新
team.write({"description": "更新後的描述"})

# 刪除
team.unlink()
```

這些動作背後會自動變成 SQL，但你完全不用動到 `SELECT * FROM ...` 這些老掉牙語法。  
（而且還不會打錯 SQL 關鍵字，真香。）

---

## 進階補充：@api 魔法小幫手

Odoo 的 ORM 不只 CRUD，還能透過 **`@api` 裝飾器**來讓程式自動反應資料變化或表單操作：

- **`@api.depends`** → 定義計算欄位（例如 `member_count`，自動算團隊人數）  
- **`@api.onchange`** → 表單操作時即時反應（例如選了使用者，就自動填寫成員名字）  
- **`@api.constrains`** → Python 驗證（例如：一個團隊只能有一個 Leader）  
- **`_sql_constraints`** → 資料庫層級的限制（避免重複資料）  

這些東西會在之後的章節慢慢派上用場，但現在你先知道，ORM 不只是「存取資料」，還能讓規則跟邏輯跟著資料跑。

---

## 4) 今日驗收清單

- [x] 知道 Model / TransientModel / AbstractModel 各自幹嘛用  
- [x] 幫 TeamMember 加上一個 Many2one，連到 Team  
- [x] 進 Odoo Shell 測試 CRUD：

  ```bash
  docker compose exec odoo bash -lc 'odoo shell -d db -c /etc/odoo/odoo.conf'
  ```

  然後輸入：

  ```python
  env["team.management.team"].search([])
  ```
  
  能看到資料，代表一切正常。

---

## 5) 明日預告（Day 07）

明天要換個場子，來到 **View / XML / QWeb** 的世界。  
今天只是把資料表建好，明天才是「怎麼把資料漂漂亮亮搬到畫面上」。  
準備好進入 Odoo 前端的宇宙吧 🚀。