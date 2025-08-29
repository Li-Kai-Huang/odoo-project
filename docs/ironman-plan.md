# 2025 IT 鐵人賽：Odoo 專案 30 天計畫

這份文件是本次鐵人賽的 **30 天文章與研究規劃**。  
每天會針對 Odoo 開發、模組、API、AI 與專案實作做一步步的紀錄。  

---

## 📅 發文規劃

### Week 1：專案起手式 & 基礎環境
- **Day 01**：為什麼選 Odoo？專案動機 & Odoo 生態介紹  
- **Day 02**：Odoo 17 新功能與社群資源 (OCA, Github, 套件資源)  
- **Day 03**：用 Docker 建立 Odoo + PostgreSQL 開發環境  
- **Day 04**：Odoo 模組結構 (addons, models, views, security)  
- **Day 05**：建立第一個自製模組 (Hello Odoo)  
- **Day 06**：Odoo ORM 基礎：Model / Field / Record  
- **Day 07**：Odoo View 與 XML / QWeb 基礎  

---

### Week 2：核心功能 — 隊伍 & 庫存管理
- **Day 08**：建立「隊伍管理」模組：Team / Member 資料模型  
- **Day 09**：建立「零件庫存」模組：Parts / Stock  
- **Day 10**：零件入庫 / 出庫流程設計  
- **Day 11**：紀錄庫存變動 (Log 與 Report)  
- **Day 12**：進一步使用 Odoo Inventory 模組整合  
- **Day 13**：報表輸出：QWeb PDF & Excel 匯出  
- **Day 14**：權限管理 (教練 / 組長 / 組員 / 管理員)  

---

### Week 3：人力管理 & 外部串接
- **Day 15**：Odoo Project / Task 模組應用  
- **Day 16**：任務分派 & 即時進度回報設計  
- **Day 17**：建立 Dashboard (看板、圖表、Gantt)  
- **Day 18**：Odoo API 串接介紹 (JSON-RPC / XML-RPC)  
- **Day 19**：串接 Google Sheet (自動匯入 / 匯出)  
- **Day 20**：串接 Slack / LINE Bot (通知與回報)  
- **Day 21**：前端網站 (Odoo Website 模組) — 隊伍官網雛形  

---

### Week 4：AI 助手 & 行動端應用
- **Day 22**：導入 AI 助手：自動生成進度摘要  
- **Day 23**：AI 問答功能 (庫存查詢 / 任務狀態)  
- **Day 24**：Odoo 行動端 / PWA 打造  
- **Day 25**：優化 UX：Dashboard、Kanban、快速操作  
- **Day 26**：雲端部署 (Docker Compose + VPS / AWS / GCP)  
- **Day 27**：效能優化 (Cache, Worker, Logging)  
- **Day 28**：錯誤排查與 Debug 技巧  

---

### Week 5：收尾與展示
- **Day 29**：專案 Demo 總整理 (完整系統展示)  
- **Day 30**：鐵人賽心得、挑戰回顧、未來規劃  

---

## 🚀 最終成果
- 一個可用的 **Odoo 隊伍管理平台**：  
  - 庫存查詢  
  - 任務管理  
  - 網頁展示  
  - 行動端應用  
  - AI 助手  

---

## 📂 專案結構建議
```bash
repo-root/
├── addons/               # 自製模組
│   ├── team_management/
│   ├── parts_inventory/
│   └── task_manager/
├── docs/                 # 文件與文章
│   ├── ironman-plan.md   # 本計畫文件
│   └── dayXX.md          # 每日文章內容
├── docker-compose.yml
├── README.md
└── requirements.txt
