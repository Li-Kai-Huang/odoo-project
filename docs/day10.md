# Day 10 — 零件入庫 / 出庫流程設計

今天要動手把我們的 **Parts Inventory** 模組流程拉起來，  
從「零件」到「庫存異動」，規劃一個能跑起來的入庫 / 出庫機制。  
雖然跟官方 Inventory 模組比起來還很陽春，但重點是讓我們熟悉 ORM + 商業邏輯設計。

---

## 1) 痛點在哪？

到目前為止，我們只能單純紀錄一個零件（Part），  
但沒有流程來管理它的存量增減。  
換句話說，零件數量只能手動改，完全不可靠。  

所以 Day 10 的目標，就是要設計 **Stock Move** 機制：  
- 入庫 → 數量增加  
- 出庫 → 數量減少（還要檢查庫存夠不夠）  
- 可取消 → 把影響回滾  

---

## 2) 我們的模型關係

- **Part**  
  - `name`, `code`, `description`, `quantity`, `team_id`, `active`  

- **StockMove**  
  - `part_id`, `move_type`, `quantity`, `note`, `date`, `state`  

重點是：  
- `part_id` → 連到零件  
- `move_type` → 入庫 or 出庫  
- `quantity` → 異動數量  
- `state` → `draft` / `confirmed` / `cancel`

---

## 3) 基本流程

1. 建立一筆 Move → 預設 `draft`  
2. 點「確認」→  
   - 如果是入庫：加數量  
   - 如果是出庫：檢查庫存是否足夠，不夠就擋下來  
3. 點「取消」→ 把 confirmed 的影響回滾  

---

## 4) 為什麼 Part 要有 `active`？

這是一個 Odoo 的慣例：  
- 有時候我們不想刪掉資料，只是暫時不用（例如某顆螺絲停產）。  
- 這時候就把 `active` 設成 False，Odoo 就會在 UI 裡自動幫你隱藏掉。  
- 好處是：資料還在、不影響歷史紀錄，但不會干擾日常操作。  

---

## 5) 今日驗收清單

- [x] 能建立 Part  
- [x] 能建立 StockMove（in/out）  
- [x] 出庫時會檢查庫存  
- [x] Cancel 能回滾  
- [x] Part 有 active 欄位，可以封存不用的零件  

---

## 補充：怎麼找到被封存的資料？

Odoo 的 `active` 欄位，就像是開關一樣：  
- **開（True）** → 資料會正常出現在清單/看板裡  
- **關（False）** → 資料不會出現，但其實沒被刪掉，只是被「封存」了  

### 1) 在介面操作
- 進清單頁面，搜尋條件加上 **Active = False**  
- 或者右上角的 **⋮ 更多選項** → 勾選「Archived」，就能看到被封存的資料

### 2) 在 Odoo Shell 測試
```python
Part = env["parts.inventory.part"]

# 預設只抓 active=True
parts = Part.search([])
print("正常看到的：", parts.mapped("name"))

# 把 active_test 關掉，就能看到所有資料
all_parts = Part.with_context(active_test=False).search([])
print("全部資料：", [(p.name, p.active) for p in all_parts])

# 專門看封存的
archived = Part.with_context(active_test=False).search([("active", "=", False)])
print("封存的：", archived.mapped("name"))
```

### 3) 小結
所以咧，Odoo 只是把 `("active", "=", True)` 默默幫你塞進搜尋條件，  
平常看到的都是「活著的」資料。  
要翻出封存的，就用 **Archived 選項** 或 **`active_test=False`**。