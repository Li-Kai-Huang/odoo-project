# Day 02 — Odoo 17 新功能與社群地圖

今天依照原訂計畫，先從「**Odoo 17 的重點**」與「**社群資源地圖**」出發，把後面客製與開發會用到的資訊一次整理清楚。先講結論：Odoo 的威力不只在於官方 App，而是「核心框架 + 社群模組（OCA）+ 自製模組」三者拼起來的綜效。了解這張地圖，能讓我們少走很多冤枉路。

---

## 1) Odoo 17 的幾個重點（以 Community 角度）

- **使用者體驗與速度**：後台操作體驗更順，清單、看板、表單的互動細節更一致；搜尋、篩選與群組化更流暢，有利日後我們做任務/庫存的操作。  
- **模組整合更緊密**：像 Project、Inventory、CRM、Website 彼此的橋接更自然，流程從「任務 → 物料 → 對外資訊」更容易串起來。  
- **報表與匯入匯出**：大多數模組都有 Excel/CSV 匯入匯出與基礎報表能力，足以支撐 Day 1~Day 14 的實作（盤點、出入庫、任務追蹤）。  
- **開發者友善**：ORM 穩定、QWeb/OWL 前端可擴充；對於我們要做的自製模組（team/parts/task）與 API 串接相當友好。  

> 註：Enterprise 版會多一些視覺化工具與特定進階模組；我們本系列以 **Community** 為主，確保免費、可開源。

---

## 2) 社群地圖：OCA 與常用資源

- **OCA（Odoo Community Association）**  
  開源模組最大集合，品質與維護度高，遵守嚴格的代碼與審核流程。常用倉庫（之後會用到）：  
  - `OCA/stock-logistics-warehouse`：庫存/倉儲加值（批號、條碼、路線等）  
  - `OCA/project`：專案/任務強化  
  - `OCA/website`：網站與對外整合  
  - `OCA/reporting-engine`：報表與匯出能力  
  - `OCA/connector`：與外部系統整合（之後做 Google Sheet/Slack/LINE 可參考理念）  
- **官方文件與原始碼**  
  - 官方 docs：了解 ORM / 安全權限 / QWeb 規則  
  - 官方 `odoo/odoo` 倉庫：查 core 模組實作方式  
- **套件授權小抄**  
  - 官方核心多為 **LGPLv3**，OCA 常見 **AGPLv3**；若我們要混用/發佈，需留意授權相容性。

---

## 3) 將 OCA 帶進開發環境（可先備好）

在 repo 中新增 OCA 子模組或直接 clone 到獨立資料夾並掛載：

```bash
mkdir -p oca-addons
git submodule add https://github.com/OCA/stock-logistics-warehouse.git oca-addons/stock-logistics-warehouse
git submodule add https://github.com/OCA/project.git oca-addons/project
git submodule add https://github.com/OCA/website.git oca-addons/website
git submodule add https://github.com/OCA/reporting-engine.git oca-addons/reporting-engine
```

### docker-compose.yml 增加掛載（示例）

```yaml
volumes:
  - odoo-data:/var/lib/odoo
  - ./addons:/mnt/extra-addons
  - ./oca-addons:/mnt/oca-addons
  - ./odoo.conf:/etc/odoo/odoo.conf:ro
```

### odoo.conf 追加 addons_path

```ini
addons_path = /usr/lib/python3/dist-packages/odoo/addons,/mnt/extra-addons,/mnt/oca-addons
```

重啟後到 Apps（取消右上的「Apps」篩選），點 Update Apps List，就能搜尋到 OCA 模組。先別急著安裝，等 Day 08~Day 14 的庫存/任務主線成形，再挑選性安裝，避免環境過重。

## 4) 今日驗收清單

 了解 Odoo 17 的重點與本專案取向（Community 為主）

 Star & Watch OCA 相關倉庫，準備日後挑模組

 專案加入 oca-addons/ 與 addons_path 擴充（可先不安裝）

 在 Apps 內能看到 OCA 模組（證明路徑正確）

## 5) 明日預告（Day 03）

依規劃將回到環境面：用 Docker 把 Odoo + Postgres 的開發體驗打磨完善（healthcheck、資料持久化、odoo.conf 與 dbfilter），並確保任何人 clone repo 就能一鍵啟動。
