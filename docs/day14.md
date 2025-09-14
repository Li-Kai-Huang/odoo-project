# Day 14 --- 審核流程上線 (Draft → To Approve → Approved / Rejected)

今天是我們零件庫存系統的一個大轉折：之前所有庫存異動（Stock Move）都可以直接「Confirm」，這其實很危險。如果某個同仁不小心按錯，或是有人惡意輸入數據，整個庫存就亂掉。所以 Day 14 的目標就是 **導入「審核制」**，把流程變得更嚴謹。  

---

## 1) 模型升級：多了審核狀態  

在 `parts.inventory.stock.move` 裡，我們把 `state` 重新設計為：  

- **Draft**：草稿，尚未送出  
- **To Approve**：送審中，等待 Manager 處理  
- **Approved**：已核准（這裡才會真正動到庫存數量）  
- **Rejected**：退回，不影響庫存  
- **Cancelled**：取消  

另外還加了欄位：  

- `submitted_by`：送審人  
- `approved_by`：審核人  
- `approved_date`：審核時間  

這樣一來，誰動了什麼就能完整記錄。  

---

## 2) UI 按鈕調整  

- 草稿狀態會看到 **Submit** 按鈕。  
- 送審後，Manager 才會看到 **Approve / Reject**。  
- Manager 群組是透過 `security.xml` 定義的，只有他們能執行審核。  

我們也把 Tree / Form 頁面調整好，避免不同狀態亂顯示按鈕。  

---

## 3) Debug 過程（血淚教學）  

- **錯誤 1**：`action_confirm is not a valid action`  
  → 原因是我們改掉了 confirm 流程，結果 XML 還留著舊的 button，必須換成 `action_submit / action_approve / action_reject`。  

- **錯誤 2**：`attrs / states 屬性不再支援`  
  → Odoo 17 改規則了，舊的 attrs/states 全部換掉，用 `invisible="state != 'draft'"` 這種方式處理。  

- **錯誤 3**：權限不生效  
  → 一開始 `ir.model.access.csv` 沒寫好，結果 User 可以亂 approve。後來補上 `groups="parts_inventory.group_parts_manager"` 才鎖起來。  

---

## 4) 為什麼要這樣設計？  

- **審核制比直接確認安全**：庫存異動變成「兩段式」，降低誤操作風險。  
- **責任清楚**：誰送審、誰核准，系統都會記錄。  
- **擴充彈性**：未來可以再加「多級審核」，或「自動通知」。  

---

## 5) 今日驗收清單  

- [x] 改寫 `state` 流程，導入審核制  
- [x] 新增 Submit / Approve / Reject 按鈕  
- [x] 加入送審人 / 審核人欄位  
- [x] 修復 attrs / states 在 Odoo 17 的相容性問題  
- [x] 完成權限控制（Manager 才能核准）  

---

## 6) 明日預告（Day 15）  

明天我們要讓 **Team 不只是管庫存，還能管任務**。也就是說：每個 Team 都會有自己的 **Task 列表**，並且能追蹤成員進度。這樣就從「倉管」走向「專案管理」了 🚀  