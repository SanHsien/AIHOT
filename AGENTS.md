# AGENTS.md — AI Coding Agent 指引（單一真相源）

本專案是一套行業熱點網站框架：收集信源、以模型篩選與寫作、歸組事件、產出日報／週報／月報，並透過網站、RSS、公開 API、Agent Markdown 與 MCP 對外提供內容。預設設定是 AI 行業示範站。

動工前先讀 [README.md](README.md)，再依任務讀 `docs/` 對應文件。所有回覆、文件與說明使用繁體中文；技術術語及程式碼識別符保留原文。

## Fork 邊界

- 上游：`KKKKhazix/AIHOT`；本 fork：`SanHsien/AIHOT`。
- 完成並通過驗證後直接 commit、push `origin/main`；不開長期分支或 fork 內 PR。
- 未經主人在當次對話明確同意，不得對上游開 PR、Issue、發布 Release 或 push。
- 修改上游持有檔案時，同步更新 [`docs/DIVERGENCE.md`](docs/DIVERGENCE.md)，並執行 `python tools/check_divergence.py`。
- 上游 commit、PR、issue、branch、tag、release 的審查結果記在 [`docs/UPSTREAM.md`](docs/UPSTREAM.md) 與 `tools/upstream_baseline.json`，避免重複判斷。
- 修復 `REVIEW.md` 列出的缺陷時，回註修復 commit 與日期。

## 最常見的任務：改成另一個行業

依 [`docs/customize.md`](docs/customize.md) 的順序處理。行業內容集中在 `industry/`：

- `site.ts`：站名、行業詞、首頁與關於頁文案。
- `taxonomy.ts`、`topics.json`：分類、標籤與主題。
- `chronicle.ts`、`chronicles/`：主題頁大事記規則與可選人工歷史。
- `sources.json`：示範信源。
- `prompts/`：精選與寫作標準。
- `selection.ts`：入選門檻。
- `features.ts`：模組開關。
- `brand/`、`pages/`：品牌、使用規則與隱私說明。

通常不需要改 `apps/` 或 `packages/`。

以下內容必須問使用者本人，不得代為決定：站名、要追蹤的信源、重要消息與雜訊的定義、分類方式，以及上線前的使用規則與隱私說明。

修改評分標準時保留原有結構（內容類型、五個加權維度、雜訊壓制、安全邊界），只替換行業案例。門檻必須用使用者標註樣本依 [`docs/selection.md`](docs/selection.md) 重新校準，不得憑感覺調整。

## 架構與硬性規則

- Node.js 24 直接執行 TypeScript；npm workspaces 為 `apps/*`、`packages/*`、`industry`。
- `apps/web` 只透過 HTTP 讀取 `apps/api`；資料庫、模型呼叫與密鑰只在後端。
- 所有公開出口都從 `packages/backend/src/publication/` 單一讀取層取資料。
- 讀者開頁不觸發模型；模型只在 worker 工作內呼叫。
- 付費請求必須經過 `providers/receipts.ts` 與預算熔斷。
- 安全閥只有設成 `true` 才開啟。開發時保持 `COLLECT_ENABLED`、`MODEL_CALLS_ENABLED`、`FEISHU_*_ENABLED`、`INDEXNOW_SUBMIT_ENABLED` 關閉；測試只連本地假服務。
- 信源預設只展示摘要與原文連結；只有來源明確允許時才開啟全文。
- 公開內容匿名，管理後台只允許管理員。
- 停用或替換功能時，同一改動要一併移除程式碼、測試、文件與保存狀態；若會刪除使用者資料，必須在 `docs/deploy.md` 寫明升級影響。
- 資料庫遷移按編號追加至 `database/migrations/`，不得改動已發布遷移；刪表或刪欄也要新增遷移。
- 不得提交 `.env`、密鑰或 `.data/`。
- 自建站不得使用 AIHOT 名稱與 Logo。

## 寫程式碼

匹配周圍程式碼的命名、寫法與註解密度。選擇可清楚解決問題的最簡方案，只建立實際會用到的抽象。重要行為要有測試；單純樣式調整不必硬加測試。

## 驗證

至少執行：

```bash
npm run typecheck
npm run build -w @aihot/web
node --test apps/web/tests/*.test.ts
python tools/check_divergence.py
python tests/test_fork_divergence.py
```

有可建立資料庫的 PostgreSQL 帳號時，再執行：

```bash
DATABASE_URL=postgres://127.0.0.1:5432/aihot_test npm test
```

站點啟動後執行：

```bash
node scripts/smoke.ts --base http://localhost:3000
```
