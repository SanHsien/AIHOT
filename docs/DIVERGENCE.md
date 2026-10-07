# 分岔登記表

本檔只登記本 fork 對**上游持有檔案**的修改。Fork 新增檔案（例如 `FORK.md`、`README.en.md`、`docs/UPSTREAM.md`、`tools/`）不算逐檔分岔，清單見 [`FORK.md`](../FORK.md)。

## 維護契約

修改任何上游持有檔案，必須在表內加一列。[`tools/check_divergence.py`](../tools/check_divergence.py) 會比對 `tools/upstream_baseline.json` 的 `reviewed_through` 與目前工作樹；實際變更與登記不一致即失敗。

最後一欄必須寫可執行判準，讓下一次同步不用重做判斷。

| 上游檔案 | 上游原狀 | 本 fork 狀態 | 為什麼分岔 | 跟進上游時怎麼處理 |
|---|---|---|---|---|
| `README.md` | 簡體中文產品說明、快速開始、自訂行業與文件索引。 | 完整改寫為繁體中文，加入語言切換、Fork 說明、維護文件與本機驗證入口；產品內容已同步至上游公開介面 3.0.0。 | 公開入口以繁中為主，且需要向使用者揭露本 fork 的維護與驗證方式。 | 上游更新時，把新增或改變的產品能力人工翻譯整合到對應章節；保留 Fork 說明與繁中入口，不得整檔覆蓋。 |
| `README.en.md` | 上游沒有此路徑；來源內容位於簡體中文 `README.md`。 | 新增完整英文版，與繁中 README 維持同一資訊架構。 | GitHub About 與 README 皆提供繁中／英文雙語，讓非中文讀者可直接使用。此路徑由分岔檢查器視為 `README.md` 的語言鏡像。 | 上游 `README.md` 有產品能力變更時，同步更新繁中與英文版本；不得把簡中原文整份覆蓋到本檔。 |
| `AGENTS.md` | 簡體中文產品規則：自訂行業、執行檢查、架構邊界與程式碼風格。 | 繁中化並加入本 fork 的 GitHub 邊界、分岔檢查、上游水位紀錄與直接推 main 工作流；保留上游全部有效規則。 | `AGENTS.md` 是所有 coding agent 的單一真相源，必須同時承載產品規則與 fork 邊界。 | 上游新增規則時人工合併並翻成繁中；Fork 邊界保持不動。若上游規則已被新架構淘汰，依新版本更新，不為零 diff 保留舊規則。 |
| `CLAUDE.md` | 一行 `@AGENTS.md`。 | 薄補丁仍指向 `AGENTS.md`，另補繁中互動、main 工作流與分岔驗證指令。 | 保持 Claude Code 的入口明確，不在兩檔重複產品規則。 | 上游若改成實質規則，將有效內容併入 `AGENTS.md`；本檔只保留入口補丁。 |
| `docs/sources.md` | 未提及 `_aihot.initialBackfillOnly` 選項。 | 移植上游 PR #85：於信源規則補充 `_aihot.initialBackfillOnly: true` 說明。 | 讓自訂信源維護者清楚防止歷史資料過量灌入的設定方式。 | 上游若合併 PR #85 或自行補充相同說明，採用上游版本並刪除此列。 |
| `packages/backend/src/sources/collect.ts` | 首次匯入後之抓取對發布過久的歷史資料不做過濾（Issue #86）。 | 移植上游 PR #85：當配置 `_aihot.initialBackfillOnly: true` 時，後續抓取過濾早於加入前 48 小時之歷史存量。 | 防止長歷史 RSS 信源在第二次抓取時大量灌入舊資料造成分析費用浪費。 | 上游若合併 PR #85 或以等效機制解決，採用上游版本並刪除此列。 |
| `packages/backend/src/sources/config-keys.ts` | `_aihot` 僅支援 `initialBackfillLimit` 與 `initialBackfillMonths`。 | 移植上游 PR #85：在 `_aihot` 新增 `"initialBackfillOnly"`。 | 與 `collect.ts` 配合放行該設定欄位。 | 上游若合併 PR #85 則刪除此列。 |
| `packages/backend/src/sources/rss.ts` | `feedText` 判定本文要求 `bodyText.length > 280 && !teaser`。 | 移植上游 PR #83：當配置 `summaryIsBody: true` 時，即使短摘要亦放行作為本文。 | 播客或短訊息類 RSS 信源摘要即本文，避免非預期發起無效詳情頁抓取。 | 上游若合併 PR #83 則刪除此列。 |
| `tests/architecture.test.ts` | 以 `path.relative` 產出路徑比對目錄名稱與規則。 | 移植上游 PR #79：將路徑轉換為 posix 斜線（`split(path.sep).join("/")`）。 | Windows 反斜線會導致模組所屬權與介面讀取判定全部誤報。 | 上游若合併 PR #79 則刪除此列；若修改架構規則保留正規化代碼。 |
| `tests/collection-tail.test.ts` | 未包含 `initialBackfillOnly` 之後續抓取行為測試。 | 移植上游 PR #85：新增 `initialBackfillOnly 時，下一次普通采集不再補進加入前的舊條目` 案例。 | 確保防歷史舊文灌入機制受測試覆蓋。 | 上游若合併 PR #85 則刪除此列。 |
