// Fork 修補的回歸測試（docs/DIVERGENCE.md 對應列）：外部標題不能在給 AI 的 Markdown 裡造出連結、
// 轉址路徑裡的 `$` 是資料不是替換樣板、偽造來源位址灌滿限流表不能重置全站密碼嘗試上限。
import "./setup.ts";
import assert from "node:assert/strict";
import { test } from "node:test";
import Fastify from "fastify";
import { config } from "@aihot/backend/config";
import { latestAnswer } from "@aihot/backend/publication/agent";
import { resolveRedirect } from "@aihot/contracts/http-policy";
import { registerAdminAuth } from "../apps/api/src/routes/admin-auth.ts";

test("an item title cannot close its link text and open a link of its own", () => {
  const query = { mode: "all", window: "24h", category: null, limit: 10 } as const;
  const item = {
    title: "Model x\\](https://evil.example/phish) y",
    links: { aihot: "https://aihot.example/items/1" },
    source: { name: "Source" },
    publishedAt: "2026-10-27T01:00:00Z",
    discoveredAt: "2026-10-27T01:00:00Z",
    category: null,
    summary: null,
    reason: null,
  };
  const res = { schemaVersion: 1, query: { ...query, by: "timeline", q: null, ordering: "timelineDesc" }, items: [item], page: { count: 1, hasMore: false, nextCursor: null } };
  const text = latestAnswer(res as never, query);
  const line = text.split("\n").find((l) => l.startsWith("1. "))!;
  // Markdown: a backslash escapes the next punctuation, so the text must end only at the link's own "](".
  let depth = 0;
  let closed = -1;
  for (let i = 3; i < line.length; i++) {
    if (line[i] === "\\") { i++; continue; }
    if (line[i] === "[") depth++;
    if (line[i] === "]" && --depth === 0) { closed = i; break; }
  }
  assert.equal(line.slice(closed), "](https://aihot.example/items/1)", line);
});

test("a redirected path keeps `$` sequences literally", () => {
  for (const tail of ["/a$`b", "/a$&b", "/a$'b", "/a$$b"]) {
    const decision = resolveRedirect(`/sources${tail}`, "");
    assert.equal(decision?.location, `/admin/sources${tail}`, tail);
  }
});

test("forged client addresses cannot reset the overall password attempt cap", async () => {
  const saved = config.adminPassword;
  (config as { adminPassword: string | null }).adminPassword = "correct-horse-battery-staple";
  const app = Fastify({ trustProxy: true });
  registerAdminAuth(app);
  await app.ready();
  try {
    let n = 0;
    const attempt = async () => {
      n++;
      const ip = `10.${(n >> 16) & 255}.${(n >> 8) & 255}.${n & 255}`;
      const r = await app.inject({ method: "POST", url: "/api/auth/password", headers: { "content-type": "application/x-www-form-urlencoded", "x-forwarded-for": ip }, payload: "password=wrong-guess&return=/admin" });
      return String(r.headers.location);
    };
    for (let i = 0; i < 50; i++) assert.match(await attempt(), /error=wrong/);
    // 5000 more forged addresses: every one is refused, and the table grows past its size bound.
    for (let i = 0; i < 5000; i++) assert.match(await attempt(), /error=too-many/);
    assert.match(await attempt(), /error=too-many/, "the overall cap still holds after the table is trimmed");
  } finally {
    (config as { adminPassword: string | null }).adminPassword = saved;
    await app.close();
  }
});
