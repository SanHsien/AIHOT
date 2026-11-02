# 路線圖

> 本 repo 後續工作的單一真相源。做完一項，就在同一個 commit 刪掉那一列；新工作只加在這裡。
> 現況段的數字是 2026-10-29 依 `main` `94a3df150d2b` 查的快照，開工前先重查 GitHub。

## 現況
這是以信源採集、模型精選與自動成刊為核心的行業網站框架 fork（[AGENTS.md:3](AGENTS.md)）。2026-10-29 `gh` 查詢記錄各主要 workflow 最近結果成功、開啟中的安全告警為 0；issues 停用，未查到 issue（2026-10-29 `gh` 查詢）。安全修正與 CI 分岔檢查已有驗證，REVIEW 驗證證據表已校正；上游審查文件已對齊現行安全與導航分岔，closed PR 依實際缺陷與分岔變動重審（[docs/UPSTREAM.md](docs/UPSTREAM.md)）。

## 近期：可以直接動手
| 項目 | 為什麼 | 驗收方式 | 建議執行者 | 證據 |
| --- | --- | --- | --- | --- |
| 整樹採納上游 `79d962e..6e0cfaf`（40 個 commit、212 檔、+4107／-1728、4 個資料庫遷移），含已合併的 #263 全文譯文入口與 #291 站點補充字體 | commit 水位卡在 `79d962e`，`python tools/check_upstream_updates.py --strict` 持續 exit 1；`check_divergence.py` 以該水位為基準，只能整樹採納才能推進，不能只挑幾筆。含 issue #278（admin cookie Secure，fork 的 `admin-auth.ts:26` 有同一缺陷）與 #282（部分政務站 TLS 握手）的修正 | 照上一輪做法把差量以 3-way 套到 fork 樹，逐一重做 DIVERGENCE 已登記的分岔檔（`admin-auth.ts`、`item.tsx`、`FeedItem.tsx`、`http-policy.ts`、兩個 `package.json`、lock、README、AGENTS）；`npm run typecheck`、`npm run build -w @aihot/web`、`node --test apps/web/tests/*.test.ts`、`python tools/check_divergence.py`、`python tests/test_fork_divergence.py` 全綠；備有 PostgreSQL 時加跑整合測試與 4 個遷移；之後推進 commit 水位、`--strict` exit 0 | Codex | [docs/UPSTREAM.md](docs/UPSTREAM.md) 的 2026-11-02 一節（逐 commit／PR／issue 裁決與工作量依據） |
| 讓 agent 輸出帶站內時間（`timelineAt`） | 服務端以 `timeline_at`／`sort_at` 判斷視窗與排序，但 agent 文字只印 `publishedAt`；兩者差數小時時，依「最近 N 小時」自行過濾的 agent 會誤刪視窗內條目（上游 #194 的 `itemTimeBits` 是同一修法） | `V1ItemPayload` 與 v1 OpenAPI 加可選 `timelineAt`；`itemLines` 輸出「站內時間」，差距 ≥ 1 分鐘才另列原文發布時間，舊帳本 payload 缺欄位時退回現狀；`BRIEF_HINTS` 加按站內時間過濾的提示；補一條 `publishedAt` 早於 `timelineAt` 數小時的回歸測試；`linkText` 反斜線跳脫與 `fork-security-fixes.standalone.test.ts` 仍綠；不得整段套用 #194 的 hunk | Codex | [docs/UPSTREAM.md](docs/UPSTREAM.md) 的 #194 條目；`packages/backend/src/publication/agent.ts:48`、`publish.ts:91-105`、`v1.ts:47-48` |

## 中期：等條件成立再做
| 項目 | 觸發條件 | 驗收方式 | 建議執行者 | 證據 |
| --- | --- | --- | --- | --- |
| 建立自訂行業站與選文校準 | 維護者確認品牌、信源、條款與標註樣本 | 依 customize 與 selection 文件完成設定、跑標註評測與本機 smoke；開啟外部採集及付費模型前確認預算 | 維護者 | [AGENTS.md:20](AGENTS.md)、[AGENTS.md:22](AGENTS.md)、[README.md:94](README.md) |
| 收斂上游已修好的 fork 補丁 | 上游修改對應安全或導航檔案 | 比較分岔行為，等效修正才刪 fork 補丁與登記列；相關回歸及 `python tools/check_divergence.py` 通過 | Codex | [docs/DECISIONS.md:63](docs/DECISIONS.md)、[AGENTS.md:12](AGENTS.md) |

## 刻意不做
| 不做什麼 | 理由 | 什麼情況下重新考慮 |
| --- | --- | --- |
| 重開已逐筆判讀的 CodeQL 項目或採用未發布安全候選整包 | 判讀與修正依 [docs/DECISIONS.md:41](docs/DECISIONS.md)；未採用的候選（ingest `Bearer` 手寫解析、static.ts 拿掉快取、json-list 改 cheerio、init-env `flag: "wx"`）經判讀為送不進的 ReDoS、已被正則擋住的誤報或 won't fix，判讀見 [docs/DECISIONS.md:41](docs/DECISIONS.md) | 新告警或 source/sink、防護邊界改變 |
| 為無共同祖先改寫歷史 | 歷史壓縮已知，採用基準差量套用即可 | 維護者另立歷史遷移需求 |
| 為測試開啟外部採集、模型與通知 | 安全閥與費用邊界見 [AGENTS.md:30](AGENTS.md)、[AGENTS.md:31](AGENTS.md) | 獲准執行有停止條件的實機驗收 |

## 維護方式
依 [tools/upstream_baseline.json](tools/upstream_baseline.json) 做增量巡檢；只有新 commit、追蹤 PR head、issue 狀態或 release 改變才重審，判斷記 [docs/UPSTREAM.md](docs/UPSTREAM.md)。依賴更新沿用 freshness 與安全告警流程；同步後跑 [AGENTS.md](AGENTS.md) 指定檢查，完整後端與瀏覽器驗證可沿用對應 SHA 的 CI 證據。
