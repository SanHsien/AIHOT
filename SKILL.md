---
name: aihot
description: 維護 SanHsien/AIHOT：自動化行業熱點彙整與日報系統框架。處理多元信源抓取、LLM 預篩與雙重打分、事件聚類與熱度排序、前端 SSR 與 Agent 對外接口（MCP/RSS/API）。
---

# AIHOT（行業熱點網站框架）

## 適用任務

- 改動或新增信源規則（RSS、網頁抓取、JSON API、X/微信/Webhook）。
- 調整特定行業之 Prompt 評分標準、寫作模板與入選門檻（`industry/`）。
- 維護前端 UI/SSR 渲染（`apps/web`）、後端 API（`apps/api`）與背景排程 Worker（`apps/worker`）。
- 維護事件聚類（Clustering）與熱度衰減（Hotness）演算法。
- 維護 Agent 對外接口（MCP 服務、Agent Markdown、RSS、OpenAPI）。
- 維護 Docker Compose 部署、PostgreSQL 遷移與本地驗證腳本。
- 檢查與同步上游 `KKKKhazix/AIHOT` 之更新與分岔登記（`docs/DIVERGENCE.md`）。

## 不適用

- 使用未經授權的「AIHOT」官方品牌與 Logo 進行外部宣傳。
- 在前端直接調用外部 LLM API 或直連資料庫。
- 在未經使用者同意下對上游 repo 發起 Pull Request 或 Issue。
- 將真實 API Key、`.env` 檔案或私密運營數據提交入 Git 版控。

## 主要入口

- `README.md` / `README.en.md`：專案首頁（繁中 / 上游鏡像）。
- `AGENTS.md`：AI Coding Agent 單一真相源與開發約定。
- `CLAUDE.md`：Claude Code 專屬薄補丁。
- `FORK.md`：Fork 維護宗旨與上游追蹤原則。
- `NOTICE.md`：授權、品牌限制與第三方素材致謝。
- `apps/web/`：React Router SSR 前端頁面與元件。
- `apps/api/`：Fastify 後端 API 服務。
- `apps/worker/`：pg-boss 背景工作排程器（抓取、打分、成刊）。
- `packages/contracts/`：前後端共享資料合約與型別定義。
- `packages/backend/`：後端共享領域邏輯與資料庫存取層。
- `industry/`：行業客製化（提示詞、分類、信源、門檻、品牌）。
- `tools/check_divergence.py`：上游分岔登記比對工具。
- `docs/DIVERGENCE.md`：分岔檔案登記表。
- `docs/DEVELOPMENT.md`：本地開發與部署文件。
- `docs/DECISIONS.md`：架構決策備忘錄。
- `REVIEW.md`：最新質量覆核紀錄。

## 最小驗證指令

```bash
npm run typecheck
npm run build -w @aihot/web
node --test apps/web/tests/*.test.ts
python tools/check_divergence.py
```
