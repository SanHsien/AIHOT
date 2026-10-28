# AGENTS.md — AI Coding Agent 指引（單一真相源）

本專案是一套行業熱點網站框架：收集信源、以模型篩選與寫作、歸組事件、產出日報／週報／月報，並透過網站、RSS、公開 API、Agent Markdown 與 MCP 對外提供內容。預設設定是 AI 行業示範站。

動工前先讀 [README.md](README.md)，再依任務讀 `docs/` 對應文件。所有回覆、文件與說明使用繁體中文；技術術語及程式碼識別符保留原文。回覆先結論後細節，不說客套話；工具輸出先消化，再以白話結論回報。

## Fork 邊界

- 上游：`KKKKhazix/AIHOT`；本 fork：`SanHsien/AIHOT`。
- 完成並通過驗證後直接 commit、push `origin/main`；不開長期分支或 fork 內 PR。
- 未經維護者在當次對話明確同意，不得對上游開 PR、Issue、發布 Release 或 push。
- 修改上游持有檔案時，同步更新 [`docs/DIVERGENCE.md`](docs/DIVERGENCE.md)，並執行 `python tools/check_divergence.py`。
- 上游 commit、PR、issue、branch、tag、release 的審查結果記在 [`docs/UPSTREAM.md`](docs/UPSTREAM.md) 與 `tools/upstream_baseline.json`，避免重複判斷。
- 修復 `REVIEW.md` 列出的缺陷時，回註修復 commit 與日期。

## 最常見的任務：改成另一個行業

依 [`docs/customize.md`](docs/customize.md) 的順序處理。這個站自己的東西在 `site/`：站名文案（`site.ts`）、每一步的模型（`models.ts`）、品牌與 Logo（`brand/`）、條款頁（`pages/`）、發布在網站根目錄的固定檔案（`public/`，替換佔位符後發布）、更新日誌（`changelog.json`）。行業知識在 `industry/`：分類標籤（`taxonomy.ts`）、主題（`topics.json`）、示範信源（`sources.json`）、提示詞（`prompts/`）、門檻（`selection.ts`）。通常不需要改 `apps/` 與 `packages/`；框架裡沒有、只有這個站要的功能，做成模組放進 `modules/`（見 `docs/architecture.md` 的「模組」）。

以下內容必須問使用者本人，不得代為決定：站名、要追蹤的信源、重要消息與雜訊的定義、分類方式，以及條款與隱私說明（`site/pages/` 只是模板，上線前需本人確認）。

修改評分標準時保留原有結構（內容類型、五個加權維度、雜訊壓制、安全邊界），只替換行業案例。門檻必須用使用者標註樣本依 [`docs/selection.md`](docs/selection.md) 重新校準，不得憑感覺調整。

## 架構與硬性規則

- Node.js 24 直接執行 TypeScript，後端沒有建置步驟。npm workspaces：`apps/*`、`packages/*`、`industry`、`site`、`modules/*`。本機執行與 Docker 見 `docs/deploy.md`。
- `apps/web` 只透過 HTTP 讀取 `apps/api`；資料庫、模型呼叫與密鑰只在後端。
- 所有公開出口都從 `packages/backend/src/publication/` 單一讀取層取資料，新增公開出口也一樣。
- 讀者開頁不觸發模型；模型只在 worker 工作內呼叫。
- 付費請求必須經過 `providers/receipts.ts` 與預算熔斷，不得繞開。
- 安全閥只有設成 `true` 才開啟。開發時保持 `COLLECT_ENABLED`、`MODEL_CALLS_ENABLED`、`FEISHU_*_ENABLED`、`INDEXNOW_SUBMIT_ENABLED` 關閉；測試只連本地假服務，不訪問任何外部服務。
- 信源預設只展示摘要與原文連結（`site_fulltext` 關）；只有來源明確允許時才開啟全文。
- 公開內容匿名，管理員與訪客看到的一樣；管理後台只允許管理員。
- 停用或替換功能、機制時，同一改動要一併移除程式碼、測試、文件與保存狀態（庫表與欄位、排程、settings、環境變數與 `.env.example` 的項目）；若會刪除使用者資料，必須在 `docs/deploy.md` 的更新說明寫明。加鎖、重試、相容舊格式、開關與兜底，先要有證據：真實部署發生過，或平台語義決定它會發生。
- 資料庫遷移放在 `database/migrations/`（只屬於某模組的表放在該模組的 `migrations/`），按完整檔名排序執行與記帳；編號相同的不同檔案分別執行，新增遷移使用新檔名，已發布的遷移不得修改。從 `0055` 起每個檔案只放一條可線上執行的語句，上游 PR 會檢查；索引使用 `CONCURRENTLY IF NOT EXISTS`，大批資料回填不放進發布遷移。約束驗證與破壞性變更先依[遷移約定](docs/architecture.md#数据库迁移)設計，不得修改歷史檔案或關閉檢查繞過。
- 不得提交 `.env`、密鑰或 `.data/`。
- 自建站不得使用 AIHOT 名稱與 Logo。
- `tests/` 裡部分測試使用示例行業的分類、標籤與公司；改了 `industry/taxonomy.ts` 後，把這些例子換成新行業的對應項。

## 寫程式碼

匹配周圍程式碼的命名、寫法與註解密度。選擇可清楚解決問題的最簡方案，只建立實際會用到的抽象。重要行為要有測試；單純樣式調整不必硬加測試。

測試守行為，不守寫法：複現問題的測試併進該功能已有的測試檔；不斷言私有常數、CSS 類名、像素位置或瀏覽器自身行為。動了採集、日期、正文清洗、精選或歸組時，用一批公開的真實訂閱與網頁比對改動前後。中文網頁的時間常不帶時區，按信源時區讀（預設 `+08:00`）；測試結果不得取決於執行機器的時區。新的環境變數寫進 `.env.example`，新的站點設定寫進 `site/`。

## 驗證

至少執行：

```bash
npm run typecheck
npm run build -w @aihot/web
node --test apps/web/tests/*.test.ts
python tools/check_divergence.py
python tests/test_fork_divergence.py
```

有可建立資料庫的 PostgreSQL 帳號時，再執行（庫名必須以 `_test` 或 `_ci` 結尾，沒有會自動建立並遷移；帳號需 `CREATEDB` 權限）：

```bash
DATABASE_URL=postgres://127.0.0.1:5432/aihot_test npm test
```

站點啟動後執行：

```bash
node scripts/smoke.ts --base http://localhost:3000
```

## 上游 PR 規則（僅在維護者明確同意回貢時適用）

要把改動提回 `KKKKhazix/AIHOT` 時先讀上游 `CONTRIBUTING.md`：只收對所有站都成立的改進，新開關與新設定入口先開 Issue；加函式或設定前先搜既有實作；依賴與鎖檔、`AGENTS.md`、`CONTRIBUTING.md`、`SECURITY.md`、規則目錄與二進制檔不收外部 PR 修改。

## 路線圖

- `ROADMAP.md` 是本 repo 後續工作的單一真相源。完成或新增工作時，在同一個 commit 更新它：做完的列刪掉、新工作加進去。不要在其他文件另列待辦。
