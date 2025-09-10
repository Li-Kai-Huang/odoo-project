# Day 11 --- 紀錄庫存變動 (Log 與 Report)

今天是我們零件庫存系統的「升級日」。\
前面雖然能入庫 /
出庫，但只有一個數字在跳，沒有歷史紀錄，感覺就像「錢包餘額」只能看到數字，卻不知道錢怎麼來、怎麼花，超沒安全感。

所以今天的目標就是：\
✅ 把每一次庫存的變動都記錄下來，未來可以回溯、查帳，甚至做報表。

------------------------------------------------------------------------

## 1) 模型設計：Part 與 Stock Move

我們在 `parts_inventory` 裡面做了兩個模型：

### Part（零件主檔）

- **核心欄位**
  - `name`（名稱）
  - `code`（料號，唯一）
  - `quantity`（目前庫存）
  - `team_id`（歸屬小隊）
  - `active`（是否啟用，軟刪除用）
- **重點**
  - `quantity` 永遠表示「即時庫存」。\
  - `active` 幫我們處理舊料號，不需要硬刪。

### Stock Move（異動紀錄）

- **核心欄位**
  - `part_id`（對應零件）
  - `move_type`（入庫 / 出庫）
  - `quantity`（異動數量）
  - `date`（異動時間）
  - `state`（Draft / Confirmed / Cancelled）
  - `note`（備註）
- **流程**
  - 建立時 → Draft（只是一張草稿，不影響庫存）
  - 確認 → 真的動數量
  - 取消 → 回滾（如果之前已經 Confirmed，就逆向操作）

------------------------------------------------------------------------

## 2) UI 設計：把 Move 放進 Part 底下

- 在 **Part Form** 下面加了一個 One2many list，直接顯示所有該零件的
    Stock Moves。\

- 這樣打開零件時，就能馬上知道它歷史的進出狀況。\

- 例子：

        Part: M3-001 螺絲
        Moves:
          - 2025/09/10 入庫 100 (Draft)
          - 2025/09/11 出庫 20 (Confirmed)

------------------------------------------------------------------------

## 3) Debug 過程（血淚記錄）

### 問題 1：`External ID not found: parts_inventory.action_parts`

- 原因：menu.xml 引用了 `action_parts`，但 `part_views.xml`
    裡沒定義。\

- 解法：先在 `part_views.xml` 裡補上：

    ``` xml
    <record id="action_parts" model="ir.actions.act_window">
        <field name="name">Parts</field>
        <field name="res_model">parts.inventory.part</field>
        <field name="view_mode">tree,form</field>
    </record>
    ```

### 問題 2：UI 空白，沒有 Tree / Form

- 原因：menu 綁到 action，但 action 沒有 view_mode 或沒掛上 model。\
- 解法：加上 `view_mode="tree,form"`。\
- 最後可以看到 list / form 了。

### 問題 3：Shell 測試 `move_in` 報錯

- 一開始 `part_id` 沒正確帶入 → SQL 報
    `null value in column "part_id" not-null constraint`。\
- 解法：要先確認 Part 有建立，然後把 `p.id` 傳進去。

------------------------------------------------------------------------

## 4) 為什麼要這樣設計？

- **Draft → Confirm → Cancel** 三階段很重要\
    → 防止誤操作，給使用者「後悔藥」。\
- **One2many 顯示紀錄**\
    → 比單純存一個數字更清楚，能知道來源。\
- **Active = False**\
    → 未來料號變動時，不需要硬刪，直接停用即可。

------------------------------------------------------------------------

## 5) 今日驗收清單

- [x] 建立 Part 與 Stock Move 模型，並串起來。\
- [x] UI：Part form 下方顯示 Moves 歷史。\
- [x] 入庫 / 出庫 → 確認能正確影響 `quantity`。\
- [x] 取消 → 能回滾庫存。\
- [x] 解決 `action_parts` 找不到、UI 空白、part_id NULL 的錯誤。

------------------------------------------------------------------------

## 6) 明日預告（Day 12）

明天要挑戰把我們的「自製 Parts 模組」和 Odoo 官方 **Inventory 模組**
對接。\
看看能不能用我們的 Stock Move 當「簡化版」，再跟 Odoo
原生的庫存流（Stock Picking / Location）做對照。
