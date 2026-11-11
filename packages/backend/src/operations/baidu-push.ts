// Baidu's push interface (搜索资源平台 · 普通收录 · API提交) takes newly published links only: resubmitting
// known ones spends the daily quota, and Baidu lowers the quota or withdraws the interface for it. So the
// first run records the discovery inventory as it is (those pages reach Baidu through the sitemap) and later
// runs submit URLs that joined it since, each once. A request over the remaining quota is refused and voids
// the rest of the day, so a request never asks for more than Baidu's previous reply said is left; the first
// request of a Beijing day carries one URL to learn that number.
import { beijingDate } from "@aihot/contracts/time";
import { config } from "../config.ts";
import { sql } from "../db.ts";
import { siteUrl } from "../publication/links.ts";
import { loadDiscoveryEntries } from "../publication/sitemap.ts";
import { postUrls, runBudget, secureEndpoint, validRemain } from "./baidu-push-guard.ts";

const MAX_URLS = 2000;
const KEY = "baidu-push.state";
/** `known`: inventory paths that are not new to Baidu; `remain`: what Baidu's last reply on `day` left, if known. */
type State = { known: string[]; day: string; remain: number | null };
type Entry = Awaited<ReturnType<typeof loadDiscoveryEntries>>[number];

// A new site's quota is a handful of URLs a day: a report issue or a story stands for a whole day's or a
// whole event's coverage, so they go before single articles; within each, newer first. A new model-board
// page (a model, a board's prices) or topic answers searches for months and comes a few a week, so it goes
// right after the report instead of waiting behind each day's news for good. Stories carry no date in the
// full inventory, which lists them newest first; the sort is stable and keeps that order.
const RANK: [RegExp, number][] = [[/^\/(daily|weekly|monthly)\//, 0], [/^\/leaderboard\//, 1], [/^\/topics\//, 2], [/^\/story\//, 3], [/^\/items\//, 4]];
const rank = (loc: string) => RANK.find(([pattern]) => pattern.test(loc))?.[1] ?? 5;
const time = (e: Entry) => e.newsAt?.getTime() ?? e.lastmod?.getTime() ?? 0;

export async function submitBaiduPush(now = new Date()) {
  const [row] = await sql<{ value: State }[]>`SELECT value FROM settings WHERE key = ${KEY}`;
  const entries = await loadDiscoveryEntries(now);
  if (!row) {
    await save({ known: entries.map((e) => e.loc), day: "", remain: null });
    return { status: "baseline" as const, urls: 0, more: false };
  }
  const known = new Set(row.value.known);
  const fresh = entries.filter((e) => !known.has(e.loc))
    .sort((a, b) => rank(a.loc) - rank(b.loc) || time(b) - time(a));
  if (!fresh.length) return { status: "empty" as const, urls: 0, more: false };
  const token = config.baiduPushToken;
  if (!config.baiduPushEnabled || !token) return { status: "disabled" as const, urls: 0, more: true };
  const endpoint = secureEndpoint(config.baiduPushEndpoint); // never send the token over clear text

  const today = beijingDate(now);
  // A stored quota that is not a plausible count is forgotten: the first request relearns it with one URL.
  let remain = row.value.day === today && validRemain(row.value.remain) ? row.value.remain : null;
  // Paths that left the inventory are dropped, so the list stays as long as the inventory; one that comes
  // back later (a page withdrawn and restored) is new to Baidu again. Progress is saved after every reply,
  // so a failure further on cannot make a retry submit what Baidu already accepted.
  const current = new Set(entries.map((e) => e.loc));
  const kept = [...known].filter((loc) => current.has(loc));
  const accepted: string[] = [];
  const progress = () => save({ known: [...kept, ...accepted], day: today, remain });
  const spend = runBudget();
  while (accepted.length < fresh.length && remain !== 0) {
    spend();
    const batch = fresh.slice(accepted.length, accepted.length + (remain === null ? 1 : Math.min(remain, MAX_URLS)));
    if (!batch.length) throw new Error("Baidu push failed: empty batch");
    const reply = await postUrls(endpoint, config.siteUrl, token, batch.map((e) => siteUrl(e.loc)).join("\n"));
    if (reply.kind === "accepted") {
      accepted.push(...batch.map((e) => e.loc));
      remain = reply.remain;
    } else {
      remain = 0;
    }
    await progress();
  }
  return { status: accepted.length ? "sent" as const : "quota" as const, urls: accepted.length, more: fresh.length > accepted.length, sample: accepted.slice(0, 3) };
}

async function save(state: State) {
  await sql`INSERT INTO settings (key, value, updated_by) VALUES (${KEY}, ${sql.json(state)}, 'worker')
    ON CONFLICT (key) DO UPDATE SET value = EXCLUDED.value, updated_at = now()`;
}
