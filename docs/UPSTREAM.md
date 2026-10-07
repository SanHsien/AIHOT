# 上游審查紀錄

最後審查：2026-10-03

本檔只記可執行結論。機器水位與 open PR head SHA 放在 [`tools/upstream_baseline.json`](../tools/upstream_baseline.json)。相同 SHA、狀態與庫存不重審；任一項變動才重新評估。

## Main commits

已合併至本 fork：

| Commit | 對應 PR | 決定 |
|---|---:|---|
| `5794327` | [#89](https://github.com/KKKKhazix/AIHOT/pull/89) | 採納。正式站核心同步、公開介面 3.0.0、日週月報流程、主題編年史、模型榜 v17 與手機版重寫均屬上游主線；本 fork 尚無產品客製，整批跟進。 |
| `4ed5e76` | [#90](https://github.com/KKKKhazix/AIHOT/pull/90) | 採納。移除牆鐘時間造成的評測不穩定。 |
| `cc66cce` | [#91](https://github.com/KKKKhazix/AIHOT/pull/91) | 採納。移除已無用途的官方價格讀取日期欄位。 |

## Open pull requests

| PR | Head | 決定 | 重新審查條件 |
|---:|---|---|---|
| [#73](https://github.com/KKKKhazix/AIHOT/pull/73) | `bf5cfba` | 暫不移植。可重現的 story digest 評測工具方向合理，但與新版 digest 實作衝突；等待上游重整並合併，避免本 fork 獨自維護評測面。 | head SHA 或狀態改變。 |
| [#74](https://github.com/KKKKhazix/AIHOT/pull/74) | `befdf3d` | 暫不移植。只有側欄隱藏 scrollbar 的外觀修正，沒有測試，且不是功能阻斷。 | head SHA 或狀態改變。 |
| [#76](https://github.com/KKKKhazix/AIHOT/pull/76) | `01a0deb` | 暫不移植。後台 API 金鑰與模型連線設定影響祕密保存、路由與日誌；目前與新版 main 衝突，等待上游安全審查與合併。 | head SHA 或狀態改變。 |
| [#78](https://github.com/KKKKhazix/AIHOT/pull/78) | `d7c3d1a` | 暫不移植。Podcast 無頁面時以 media enclosure 作連結合理，且測試綠；等待上游處理衝突後採納。 | head SHA 或狀態改變。 |
| [#79](https://github.com/KKKKhazix/AIHOT/pull/79) | `79f0d4f` | 已採納。移植路徑正規化至 `tests/architecture.test.ts`，解決 Windows 反斜線導致模組所屬權比對全部失敗的缺陷。 | 上游若合併 PR #79 則刪除分岔登記。 |
| [#80](https://github.com/KKKKhazix/AIHOT/pull/80) | `b14c942` | 不需移植。上游 `5794327`（PR #89）已重構 `tests/media-performance.test.ts` 並移除 `deleteAllJobs` 調用，缺陷已不復存在。 | head SHA 或狀態改變。 |
| [#81](https://github.com/KKKKhazix/AIHOT/pull/81) | `9d6e617` | 暫不移植。補填後來才取得的日期／作者／語言方向合理，但更新路徑涉及 material 語意；目前與新版 main 衝突，等待上游整合。 | head SHA 或狀態改變。 |
| [#83](https://github.com/KKKKhazix/AIHOT/pull/83) | `65a0893` | 已採納。移植 `summaryIsBody` 判斷至 `packages/backend/src/sources/rss.ts` 並新增 `tests/rss-summary-body.test.ts`，允許短摘要信源免於非預期爬取。 | 上游若合併 PR #83 則刪除分岔登記。 |
| [#84](https://github.com/KKKKhazix/AIHOT/pull/84) | `0ade519` | 暫不移植。讓測試跟隨行業門檻是正確方向，但檔名與新版 main 已重整並衝突；等待上游重做。 | head SHA 或狀態改變。 |
| [#85](https://github.com/KKKKhazix/AIHOT/pull/85) | `cf216cf` | 已採納。移植 `_aihot.initialBackfillOnly` 至 `collect.ts`、`config-keys.ts`、`docs/sources.md` 與 `tests/collection-tail.test.ts`，解決長歷史 RSS 第二次抓取過量灌入舊文的成本風險。 | 上游若合併 PR #85 則刪除分岔登記。 |

## Closed, unmerged pull requests

- [#72](https://github.com/KKKKhazix/AIHOT/pull/72) `515f9de`：不移植。上游維護者已關閉，且 #89 大幅改寫 Markdown／publication 路徑；舊 branch 已從上游刪除，本 fork 同名遠端分支也於 2026-10-03 清掉。
- #24、#26、#32、#33–#36、#38–#62、#68：截至本輪均已關閉未合併；新版 main 已經歷正式站同步與架構重寫，不再逐筆移植舊 patch。只有上游重開或以新 PR 重提才重新評估。

## Open issues

| Issue | 決定 | 關聯／重新審查條件 |
|---:|---|---|
| [#67](https://github.com/KKKKhazix/AIHOT/issues/67) | 閱讀順序已由 #71 完成；綜述品質仍缺固定真實樣本對照。本 fork 不先改 prompt。 | #73 或 issue 有新證據／結論。 |
| [#77](https://github.com/KKKKhazix/AIHOT/issues/77) | 大型功能提案：將 `industry/` 改成後台 runtime override。影響設定來源、prompt 版本、祕密與升級語意；不在本 fork 先行。 | 上游提出分期實作 PR 或接受明確設計。 |
| [#86](https://github.com/KKKKhazix/AIHOT/issues/86) | 真實且具成本風險。本 fork 已移植 PR #85（opt-in `initialBackfillOnly`）徹底解決。 | 上游官方合併或提出其他替代實作時比對。 |
| [#88](https://github.com/KKKKhazix/AIHOT/issues/88) | 真實相容性問題；目前可用 `LLM_EXTRA_JSON={"max_tokens":10000}`。不採「從 reasoning_content 抽 JSON」；等待上游針對 reasoning 模型設計 token budget。 | 上游新 PR、模型路由變更或 workaround 失效。 |

## Branches, tags, releases

- 上游分支：只有 `main`。
- 本 fork 分支：只有 `main`；`codex/article-body-fidelity-20261002` 已於 2026-10-03 刪除。
- 上游與本 fork：目前均無 tag、無 GitHub Release，因此沒有舊版本可清。首次發布由本 fork 在完整閘門通過後建立，之後只保留最新 release 與對應 tag。
