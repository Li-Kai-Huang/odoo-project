# Odoo + Docker 指令速查手冊

這份手冊整理了開發 Odoo 模組時常用的 **Docker 指令** 和 **Odoo 指令**，
方便你在除錯或日常開發時快速查找。

---

## 🚢 Docker 指令

### 基本容器操作

```bash
# 啟動容器（背景模式）
docker compose up -d

# 停止容器
docker compose down

# 重新啟動容器
docker compose restart

# 查看容器狀態
docker ps

# 查看服務日誌（最新 100 行）
docker compose logs --tail=100 odoo

# 持續追蹤日誌
docker compose logs -f odoo
```

### 進入容器

```bash
# 進入 Odoo 容器
docker compose exec odoo bash

# 進入 Postgres 容器
docker compose exec db bash
```

---

## 🐘 PostgreSQL 指令

在 **db** 容器內：

```bash
# 進入資料庫
psql -U odoo -d db

# 查看所有資料庫
psql -U odoo -d postgres -c "\l"

# 查看所有資料表
psql -U odoo -d db -c "\dt"

# 查詢某張表資料
psql -U odoo -d db -c "SELECT * FROM team_management_team;"
```

---

## 🦉 Odoo 指令

### 啟動與更新

```bash
# 啟動 Odoo (用指定設定檔)
odoo -c /etc/odoo/odoo.conf

# 更新特定模組
odoo -c /etc/odoo/odoo.conf -d db -u team_management --stop-after-init

# 安裝模組
odoo -c /etc/odoo/odoo.conf -d db -i team_management --stop-after-init
```

### Odoo Shell（互動模式）

```bash
# 啟動 Shell
odoo -c /etc/odoo/odoo.conf -d db shell

# 建立資料
team = env["team.management.team"].create({"name": "Test Team"})
print(team.id, team.name)

# 查詢
env["team.management.team"].search([])

# 更新
team.write({"description": "更新描述"})

# 刪除
team.unlink()
```

---

## 🧹 清除與維護

```bash
# 清除快取與重新載入
docker compose exec odoo bash -lc "rm -rf /var/lib/odoo/.local/*"

# 移除資料庫
docker compose exec db psql -U odoo -d postgres -c "DROP DATABASE db;"

# 新建資料庫
docker compose exec db psql -U odoo -d postgres -c "CREATE DATABASE db OWNER odoo;"
```

---

## ✅ 常見除錯步驟

1. **模組安裝錯誤**
   - 檢查 `__manifest__.py` 是否正確。
   - 檢查 `views/` XML 語法，有沒有多餘的 tag。

2. **找不到模組**
   - 確認 `addons_path` 包含 `/mnt/extra-addons`。
   - 進入 UI → Apps → Update Apps List。

3. **資料表沒建出來**
   - 確認 model 有 `models.Model`。
   - 確認模組有被安裝/升級。

---

## 📌 推薦用法

把這份手冊丟到專案目錄下的 `docs/cheatsheet.md`，
以後團隊誰遇到錯誤都能馬上查。 🚀
