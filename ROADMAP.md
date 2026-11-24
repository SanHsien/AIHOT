# 路線圖

> 本 repo 後續工作的單一真相源。做完一項，就在同一個 commit 刪掉那一列；新工作只加在這裡。
> 現況段的數字是 2026-10-29 依 `main` `94a3df150d2b` 查的快照，開工前先重查 GitHub。

## 現況
2026-11-25：從工作分支 `codex/upstream-1124` 的 `67116b6` 接續，已逐筆審完上游 `7140b6f..bc57d79` 全部 103 筆：採納 6、延後 85、拒絕 12。審查水位為 `bc57d793fb4d3e35fbe908d59514664b3539b0e7`，不是整樹整合水位；產品仍以 `7140b6f` 加既有 fork 補丁與本輪兩組修正為準。DNS 備援／內網拒絕及 JSON 診斷共 22 項本機測試通過，修前失敗證據見 [docs/UPSTREAM.md](docs/UPSTREAM.md)。完整 `pwsh -NoProfile -File tools/dev_check.ps1` exit 0（網頁 67/67、分岔 352/352、契約 9/9 及 2/2）；standalone 初跑 290/291，唯一失敗是 Node.js 26 的 IP SNI 夾具，修後只重跑該檔 5/5 通過。只提交目前分支，不 push；`713caec` 的 Actions 觸發限制保留。

這是以信源採集、模型精選與自動成刊為核心的行業網站框架 fork（[AGENTS.md:3](AGENTS.md)）。2026-10-29 `gh` 查詢記錄各主要 workflow 最近結果成功；2026-11-08 重查 Dependabot 與 Code scanning open 告警各 0；issues 停用，未查到 issue（2026-10-29 `gh` 查詢）。安全修正與 CI 分岔檢查已有驗證，REVIEW 驗證證據表已校正；上游審查文件已對齊現行安全與導航分岔，closed PR 依實際缺陷與分岔變動重審（[docs/UPSTREAM.md](docs/UPSTREAM.md)）。Agent 輸出已支援站內時間（`timelineAt`）並附時間過濾提示，V1 契約與回歸測試已補齊。

2026-11-03：以 `92d91d7` 為起點整樹採納上游 `79d962e..41cee09`（48 個 commit、7 個新增遷移），保留已登記安全、導航與站內時間分岔；其後追加採納 #323 合併的 `dcb366e`、`cd424b0`（Menu 鍵盤導航）；commit 水位為完整 `cd424b0a513c7c8535b6f291b106a3086d6b75bf`，PR 水位 #332，無追蹤中的 open PR。Node.js 24.22.1 的完整本機閘門通過（`27ced027`：網頁 65/65、standalone 249/249、分岔契約 9/9；追加採納 `cd424b0` 後 `dev_check` 網頁 67/67、分岔契約 9/9），上游 `--strict` exit 0；本機無可用 `_test`／`_ci` PostgreSQL（5432 無監聽）。2026-11-03 `27ced027` 推送後的 [check.yml run 41619101964](https://github.com/SanHsien/AIHOT/actions/runs/41619101964)：`check`、`docker` 兩個 job 均成功，該 job 的 PostgreSQL 是空庫（`aihot_ci`），驗到的是全新安裝。2026-11-09 以 PostgreSQL 17.11 在有資料的 0089 庫上驗證 7 個遷移（0090、0091、0092、0105、0121、0122、0123）的升級路徑：全部套用、原有資料雜湊不變、升級後 schema 與全新安裝相同（[docs/UPSTREAM.md](docs/UPSTREAM.md)「既有資料庫升級驗證」）。

2026-11-10：再以 `cd424b0..7140b6f`（52 個 commit、4 個新遷移 0124–0127）整樹採納，commit 水位改為完整 `7140b6f6f5a336fbd5668021c5ada750c7333ff2`（含追加採納 #383 合併的 `7140b6f`），PR 水位 #383、issue 水位 #340，追蹤中的 open PR 為 #375（defer）。Node.js 24.22.1 下 typecheck、SSR build、網頁 67/67、standalone 280/280 通過，`--strict` exit 0；仍無本機 PostgreSQL。

## 近期：可以直接動手
| 項目 | 為什麼 | 驗收方式 | 建議執行者 | 證據 |
| --- | --- | --- | --- | --- |

## 中期：等條件成立再做
| 項目 | 觸發條件 | 驗收方式 | 建議執行者 | 證據 |
| --- | --- | --- | --- | --- |
| G1：事件合併與討論熱度（8 筆） | 本工作樹具備可建立隔離 _test／_ci 庫的 PostgreSQL 後，合併最終鎖序與召回修正；用 events、signals、embedding-dimensions 的修前失敗／修後通過案例，另驗併發合併與回滾。 | 每項修前失敗、修後通過，完整 gate exit 0；逐筆 SHA 見決策表 | Codex | [103 筆裁決](docs/DECISIONS.md#2026-11-25上游-103-筆逐項裁決) |
| G2：工作、回執與告警（10 筆） | 可用隔離 PostgreSQL 並能驗證 PID birth 的 Linux／macOS 測試環境就緒後，驗 queue-recovery、translate、delivery-resolution、embedding-response／storage、alerts；確認付費不重放、舊 revision 不蓋新結果及恢復告警不遺漏。 | 每項修前失敗、修後通過，完整 gate exit 0；逐筆 SHA 見決策表 | Codex | [103 筆裁決](docs/DECISIONS.md#2026-11-25上游-103-筆逐項裁決) |
| G3：模組出口、帳號與登入（16 筆） | 維護者要啟用相應模組或停用飛書登入時，先確認資料保留／備份，再把授權、環境範例、升級說明及 0146／0147／0149／0150 成套處理；跑撤權、preview／admin 快取及同步衝突回歸，保留全站登入限流。 | 每項修前失敗、修後通過，完整 gate exit 0；逐筆 SHA 見決策表 | Codex | [103 筆裁決](docs/DECISIONS.md#2026-11-25上游-103-筆逐項裁決) |
| G4：前端動畫與版型（13 筆） | 安排前端版型更新且本工作樹有可用 WebKit 時，補行為回歸及桌面／手機、鍵盤／焦點、reduced-motion、字型備份驗收；motion 程式碼與 manifest／鎖檔同批移除，保留 phone view-transition 與 outline 捲動補丁。 | 每項修前失敗、修後通過，完整 gate exit 0；逐筆 SHA 見決策表 | Codex | [103 筆裁決](docs/DECISIONS.md#2026-11-25上游-103-筆逐項裁決) |
| G5：備份、媒體與出網路由（4 筆） | 安排備份或媒體／SocialData 路由更新時，先以本機假 S3、代理及供應商服務證明失敗；驗 multipart abort／complete、備份恢復、簽章竄改及 request 開始後不重放，再移植。 | 每項修前失敗、修後通過，完整 gate exit 0；逐筆 SHA 見決策表 | Codex | [103 筆裁決](docs/DECISIONS.md#2026-11-25上游-103-筆逐項裁決) |
| G6：內容政策與資料庫清理（11 筆） | 需要 EditorialPolicy／原文遮蔽或進行資料庫精簡時，先移除所有現行讀寫，再在含資料的舊版 _test 庫執行新遷移並比對資料；以 publication、events、content-publication、seed 與所有公開出口回歸證明安全。 | 每項修前失敗、修後通過，完整 gate exit 0；逐筆 SHA 見決策表 | Codex | [103 筆裁決](docs/DECISIONS.md#2026-11-25上游-103-筆逐項裁決) |
| G7：公開語料與語言判定（6 筆） | 備妥可離線重播的公開真實訂閱／頁面及英中日韓混語樣本後，對同批樣本比較前後正文、標題、圖片及翻譯／閱讀出口；不得只靠人工小字串證明正文清理與語言閾值適用。 | 每項修前失敗、修後通過，完整 gate exit 0；逐筆 SHA 見決策表 | Codex | [103 筆裁決](docs/DECISIONS.md#2026-11-25上游-103-筆逐項裁決) |
| G8：測試規則與 CI（8 筆） | 相關產品批次已採納時再整合測試搬移與新架構規則，對帳行為案例而非只看數量；逾時調整先重現。CI 修改等 Actions 恢復後驗 Linux job，始終保留 713caec 的 push 篩選。 | 每項修前失敗、修後通過，完整 gate exit 0；逐筆 SHA 見決策表 | Codex | [103 筆裁決](docs/DECISIONS.md#2026-11-25上游-103-筆逐項裁決) |
| G9：報告、SEO 與公開讀取層（6 筆） | 安排報告／SEO 同步且有隔離 PostgreSQL 時，驗新舊期次、穩定 section key、期號併發、分類導讀、sitemap／RSS／Agent／v1／通知；保留 timelineAt、Markdown 跳脫及百度 HTTPS／有界請求防線。 | 每項修前失敗、修後通過，完整 gate exit 0；逐筆 SHA 見決策表 | Codex | [103 筆裁決](docs/DECISIONS.md#2026-11-25上游-103-筆逐項裁決) |
| G10：英文站點（3 筆） | 維護者確認需要 /en 及英文文案後，將 ENGLISH、英文 taxonomy、路由／連結／SEO 與 parser 依賴成套採納；跑雙語導覽、歷史報告 section key 及各出口語言回歸，未確認前維持中文站。 | 每項修前失敗、修後通過，完整 gate exit 0；逐筆 SHA 見決策表 | Codex | [103 筆裁決](docs/DECISIONS.md#2026-11-25上游-103-筆逐項裁決) |
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
