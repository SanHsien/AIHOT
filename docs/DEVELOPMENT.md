# 開發與部署指南（DEVELOPMENT.md）

本文件提供 SanHsien/AIHOT 的本機開發環境建置、除錯與驗證指引。

---

## 一、系統架構速覽

```
AIHOT Monorepo
├── apps/
│   ├── web/          # 前端網站（React Router SSR、Tailwind CSS、繁中/簡中介面）
│   ├── api/          # 後端 API 服務（Fastify）
│   └── worker/       # 背景任務排程器（pg-boss，負責爬取、LLM 調用、熱度計分）
├── packages/
│   ├── contracts/    # 前後端共享型別合約（TypeScript）
│   └── backend/      # 後端共用業務邏輯與資料庫存取（ publication 讀取層）
├── industry/         # 行業客製化設定（站名、分類、示範信源、Prompt 與門檻）
├── database/         # PostgreSQL 遷移腳本（migrations/）與種子資料（seeds/）
├── tools/            # 本 Fork 維護工具與上游分岔檢查腳本
└── scripts/          # 環境初始化與輔助驗證腳本
```

---

## 二、環境先決條件

- **作業系統**：Windows 11（原生環境）或 Linux / macOS
- **Node.js**：`>= 24.11.0`（本機建議使用 Node.js 24 或以上，原生支援 TypeScript 與 `--env-file`）
- **npm**：`>= 11.0.0`
- **Python**：`>= 3.10`（用於維護工具與分岔比對檢查器）
- **Docker & Docker Compose**：推薦用於一鍵啟動 PostgreSQL 與整套服務

---

## 三、快速開始

### 方式 A：Docker Compose 一鍵啟動（推薦）

```bash
# 1. 初始化環境設定檔並注入你的 LLM API Key
node scripts/init-env.ts --llm-key <你的_API_KEY>

# 2. 構建並啟動全部容器（Web + API + Worker + PostgreSQL）
docker compose up -d --build

# 3. 查看服務狀態與日誌
docker compose ps
docker compose logs -f
```

瀏覽服務：
- 前台網站：<http://localhost:3000>
- 後台管理：<http://localhost:3000/admin>（密碼見 `.env` 的 `ADMIN_PASSWORD`）
- API 端點：<http://localhost:3001>

### 方式 B：本地分項開發啟動

若已有本機 PostgreSQL 17 執行個體：

```bash
# 1. 安裝依賴
npm install

# 2. 複製設定檔並填入 DATABASE_URL 與 LLM 金鑰
cp .env.example .env

# 3. 執行資料庫遷移
npm run db:migrate

# 4. 啟動後端 API
npm run dev:api

# 5. 另開終端啟動背景 Worker
npm run dev:worker

# 6. 另開終端啟動前端 Web
npm run dev:web
```

---

## 四、本地驗證品質指令（CI 閘門）

在提交任何程式碼或文件變更前，務必依序執行下列指令：

```bash
# 1. 靜態型別檢查（涵蓋 contracts, backend, api, worker, tests, web）
npm run typecheck

# 2. 前端 SSR 服務建置
npm run build -w @aihot/web

# 3. 前端單元測試
node --test apps/web/tests/*.test.ts

# 4. 上游分岔登記比對（與 docs/DIVERGENCE.md 100% 一致）
python tools/check_divergence.py

# 5. 分岔檢查器本身之單元合約測試
python tests/test_fork_divergence.py
```

若本機有 PostgreSQL 測試資料庫（名為 `aihot_test`）：
```bash
DATABASE_URL=postgres://127.0.0.1:5432/aihot_test npm test
```

---

## 五、開發注意事項與安全準則

1. **嚴格禁止向上游開 PR**：本庫為個人 Fork，對外操作只打 `SanHsien/AIHOT`。
2. **測試安全閥預設關閉**：
   - 開發時維持 `COLLECT_ENABLED=false` 與 `MODEL_CALLS_ENABLED=false`，避免本地除錯或測試無端消耗付費 Token。
3. **換行符號管理**：
   - 本倉庫根目錄已設定 `.gitattributes`（`* text=auto eol=lf`），請確保編輯器在 Windows 上使用 LF 換行。
4. **品牌替換提醒**：
   - 「AIHOT」名稱及 Logo 僅供官方參考，自訂站點請務必至 `industry/site.ts` 與 `industry/brand/` 替換為自有站名與圖標。
