# Day 12 --- 與官方 Inventory 模組接軌 (Smart Button & Product 整合)

昨天我們的系統已經能做到「零件 → 紀錄進出貨」。  
但光自己玩還不夠，如果真的要進公司環境跑，勢必要考慮 **和 Odoo 官方 Inventory 模組對接**。  
今天的目標就是：  
✅ 在 Product 上加上 **Team 欄位** 和 **Smart Button**，讓它可以跳轉到對應的庫存紀錄。

---

## 1) 設計思路

- **Product Template 增強**
  - 加上 `team_id`（方便做分組）
  - 顯示 `qty_available`（官方計算的即時庫存，不再只靠我們自家的 quantity）
- **Smart Button**
  - 放在 Product form 的 header
  - 點下去 → 開啟一個 Action，顯示所有對應的 Stock Moves

這樣使用者在看產品時，不只知道它是什麼料，還能直接切到它的出入庫紀錄，一頁完成。

---

## 2) UI 實作

### 修改 Product Form 與 Tree

```xml
<xpath expr="//sheet/notebook/page[@name='general_information']/group" position="inside">
  <group string="Team">
    <field name="team_id"/>
    <field name="qty_available" string="On Hand" readonly="1"/>
  </group>
</xpath>

<xpath expr="//header" position="inside">
  <button type="action" name="%(action_team_moves)d"
          string="Team Moves" class="oe_stat_button"/>
</xpath>
```

這段加在 `product_views.xml` 裡，能在 Product form 看到一顆新按鈕。

---

## 3) Debug 血淚紀錄

### 問題 1：`External ID not found: parts_inventory.action_team_moves`

- **原因**：Smart Button 指到一個不存在的 action。  
- **解法**：要在 `stock_move_views.xml` 補上 Action，例如：

```xml
<record id="action_team_moves" model="ir.actions.act_window">
  <field name="name">Team Moves</field>
  <field name="res_model">parts.inventory.stock.move</field>
  <field name="view_mode">tree,form</field>
</record>
```

---

### 問題 2：Smart Button 沒有出現

- **可能原因**：
  1. `xpath` 路徑寫錯，button 沒插到 header。
  2. Action 沒定義，Odoo 自動跳過按鈕。  

- **解法**：
  - 確認 `<xpath expr="//header" position="inside">` 路徑正確。  
  - Action id 要能被正確找到，否則按鈕不會顯示。

---

### 問題 3：Validation Error「Part code must be unique」

- **原因**：`code` 有 `_sql_constraints`，同一個料號只能出現一次。  
- **解法**：換一個 code（例如 aaa → aaa01），或是直接複用現有的料號。

---

## 4) 今日收穫

- [x] 成功在 **Product** 上加上 Team 與 On Hand 欄位。  
- [x] 在表單 header 加上 **Smart Button**，能連動到 Move 紀錄。  
- [x] Debug 過程中學會：Action / Menu / Button 這三者一定要成對，不然就會出現「看不到按鈕」的狀況。  

---

## 5) 明日預告（Day 13）

明天我們要來處理 **權限與流程控制**。  
不再讓所有人都能隨便入庫 / 出庫，可能需要分角色（例如倉管、審核人員），也會加入 **審核流程**。  
這樣才符合真實環境，不然現在就像「開放式冰箱」，誰都能拿，庫存一定爆炸。