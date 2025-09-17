# Day 03 — 打磨 Odoo 開發環境：Docker Compose + odoo.conf 最佳化

昨天完成了 OCA 模組的引入，Apps List 已經能看到一堆 OCA 套件。今天要專注在「環境打磨」：確保開發環境足夠穩定，讓其他人 clone 專案下來也能一鍵起跑，不會踩到各種小坑。

---

## 1) 強化 docker-compose.yml

昨天我們已經能啟動 Odoo + Postgres，今天加上幾個改進：

- **healthcheck**：確保服務健康後再啟動依賴容器  
- **restart 策略**：容器掛掉時自動重啟  
- **資料持久化**：PostgreSQL 跟 Odoo filestore 都用 volume 保存

```yaml
version: "3.8"

services:
  db:
    image: postgres:15
    environment:
      POSTGRES_DB: postgres
      POSTGRES_USER: odoo
      POSTGRES_PASSWORD: odoo
      PGDATA: /var/lib/postgresql/data/pgdata
    volumes:
      - odoo-db-data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U odoo -d postgres"]
      interval: 5s
      timeout: 5s
      retries: 10
    restart: unless-stopped

  odoo:
    image: odoo:17
    depends_on:
      db:
        condition: service_healthy
    ports:
      - "8069:8069"   # web
      - "8072:8072"   # longpolling
    environment:
      HOST: db
      PORT: 5432
      USER: odoo
      PASSWORD: odoo
    volumes:
      - odoo-data:/var/lib/odoo
      - ./addons:/mnt/extra-addons
      - ./oca-addons:/mnt/oca-addons
      - ./odoo.conf:/etc/odoo/odoo.conf:ro
    command: ["odoo", "-c", "/etc/odoo/odoo.conf", "--dev=reload"]
    restart: unless-stopped

  pgadmin:
    image: dpage/pgadmin4:8
    depends_on:
      db:
        condition: service_healthy
    environment:
      PGADMIN_DEFAULT_EMAIL: admin@example.com
      PGADMIN_DEFAULT_PASSWORD: admin
    ports:
      - "5050:80"
    restart: unless-stopped

volumes:
  odoo-db-data:
  odoo-data:
```

## 2) 優化 odoo.conf

加入 `dbfilter` 避免一堆測試 DB 出現，同時定義路徑、管理密碼與 log level。

```ini
[options]
db_host = db
db_port = 5432
db_user = odoo
db_password = odoo
addons_path = /usr/lib/python3/dist-packages/odoo/addons,/mnt/extra-addons,/mnt/oca-addons
data_dir = /var/lib/odoo

admin_passwd = <請改密碼>
log_level = info

# 只允許指定 DB（例：db）
dbfilter = ^db$
```

## 3) 驗收步驟

### 1. 重建容器

```bash
docker compose up -d --force-recreate
docker compose ps
```

DB 應顯示 `healthy`。

### 2. Odoo log

```bash
docker compose logs --tail=100 odoo 
```

沒有 `Bad database manager password`，就表示設定正確。

### 3. pgAdmin 連線

- Host: db
- Port: 5432  
- User: odoo / Pass: odoo

能看到 `ironman` DB，展開 Schemas → public → Tables 就能確認表結構。

## 4) 測試與修正

在 log 中還有兩個小警告需要修正：

- **version: 已被棄用**  
  Compose v2 開始不需要在 `docker-compose.yml` 頂部加 `version:`，建議直接刪掉。

- **longpolling_port 已被棄用**  
  Odoo 17 把這個參數改名為 `gevent_port`。請把 `odoo.conf` 裡的：

```ini
longpolling_port = 8072
```

改成：

```ini
gevent_port = 8072
```

改完後再：

```bash
docker compose up -d --force-recreate
```

即可清除這些警告，讓環境更乾淨。

## 5) 今日心得

今天把環境做了三件事：

1. **強化 Compose**：避免 DB 還沒 ready 就啟動 Odoo
2. **優化 odoo.conf**：加上 `dbfilter`，避免雜 DB 干擾  
3. **根據 log 警告做修正**：讓設定更符合 Odoo 17 的官方標準

雖然都是小細節，但這些「地基工程」確保了未來開發不會被奇怪的錯誤困擾。

## 6) 明日預告（Day 04）

開始動手寫第一個「最小自製模組」：`team_management`，只包含最簡單的模型（Team / Member），確保模組骨架能正確安裝、升級、移除。
