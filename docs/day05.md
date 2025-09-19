# Day 05 — 建立第一個自製模組 (Hello Odoo)

今天終於進入重頭戲：**寫我人生的第一個 Odoo 模組**！前幾天像是在搭舞台（環境、OCA 地圖、Docker 配置），今天就是第一次上台表演。模組名稱很霸氣 —— **Team Management**。雖然目前只是個「骨架版」，但這一步很關鍵，因為它讓我從「讀文件」跨到「能裝得起來的模組」。

---

## 1) 模組設計目標

- **建立 Team**：能輸入隊伍名稱、描述。  
- **成員管理**：Team 下面能有多個 Members，角色可選 Coach / Leader / Member。  
- **專案關聯**：隊伍可綁定 Project 模組中的專案。  
- **Smart Button**：如果有專案，表單右上會出現按鈕，一鍵跳轉到對應專案。  

簡單四件事，卻涵蓋了 Model、View、Access、Menu 四大核心，足夠讓我走完整個流程。

---

## 2) 模組結構與檔案

- `__manifest__.py`：模組定義（名字、相依模組、載入的檔案路徑）。  
- `__init__.py`：初始化，決定載入哪些 Python 檔。  
- `models/`：Python ORM 類別。這次寫了 `Team` 與 `Member`，並透過 One2many / Many2one 建立關聯。  
- `views/`：XML 視圖，包含 Tree（清單）、Form（表單）、Kanban（卡片）。  
- `security/ir.model.access.csv`：權限表，讓一般使用者也能 CRUD。  
- `menuitem + action`：把功能掛到 Odoo 主選單，否則模組就像隱形。  

---

## 3) Odoo 17 的新坑位（必看！）

- **attrs / states RIP**：在 17 版完全廢棄了，以前寫 `attrs="{'invisible': [('field','=',False)]}"`，現在會直接 ParseError。  
  - ✅ 新寫法 → `invisible="not project_id"`  
- **Smart Button 新姿勢**：不要再硬綁外部 XML ID，例如 `project.project_action_project`。  
  - ✅ 解法 → 在 Python 模型裡寫 `action_open_project`，直接回傳 `ir.actions.act_window`。穩、好維護、版本相容。  

---

## 4) 今日踩坑日記

- 忘記在 `__init__.py` 匯入 model → KeyError `team_id`，嚇到以為資料庫壞了。  
- 外部 ID 不存在 → 模組升級爆炸，學乖了以後都走 Python method。  
- 連錯資料庫 → debug 模式發現跑到 `ironman`，才知道 `dbfilter` 沒設好。  
- ParseError → 原因就是 attrs 語法在 17 涼了，乖乖改用新寫法才過關。  

> 這些坑我都記下來，因為大概新手 Odoo 17 都會遇到 XD

---

## 5) 今日驗收清單

- [x] Team Management 模組能安裝成功  
- [x] 在選單中出現「Team Management」→「Teams」  
- [x] 可以建立一個隊伍，新增成員（支援清單與 Kanban）  
- [x] 如果隊伍綁了專案，右上會出現 **Project** 按鈕，能正確跳轉  

---

## 6) 明日預告（Day 06）

明天要挑戰 **Odoo ORM 的基礎**，開始操作 Model / Field / Record。特別是要把 Member 綁到 `res.users`，讓「名單上的人」真正對應到能登入的使用者。到時候才能玩「任務分派與進度回報」，越來越有實戰味道！
