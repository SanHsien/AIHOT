// Fork 修補的回歸測試（docs/DIVERGENCE.md 對應列）：外部標題不能在給 AI 的 Markdown 裡造出連結、
// 轉址路徑裡的 `$` 是資料不是替換樣板、偽造來源位址灌滿限流表不能重置全站密碼嘗試上限。
import "./setup.ts";
import assert from "node:assert/strict";
import { test } from "node:test";
import Fastify from "fastify";
import type { ModuleDeclaration } from "@aihot/contracts/modules";
import { MODULES } from "@aihot/site/modules";
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

test("publishedAt earlier than timelineAt by hours outputs site timeline and original published time", () => {
  const query = { mode: "all", window: "24h", category: null, limit: 10 } as const;
  const itemWithSkew = {
    title: "Article with earlier publication",
    links: { aihot: "https://aihot.example/items/1", original: "https://source.example/1" },
    source: { name: "Source" },
    publishedAt: "2026-10-27T01:00:00Z",
    timelineAt: "2026-10-27T05:00:00Z",
    discoveredAt: "2026-10-27T05:00:00Z",
    category: null,
    summary: null,
    reason: null,
  };
  const itemWithoutTimeline = {
    title: "Legacy item without timelineAt",
    links: { aihot: "https://aihot.example/items/2", original: "https://source.example/2" },
    source: { name: "Source" },
    publishedAt: "2026-10-27T02:00:00Z",
    discoveredAt: "2026-10-27T02:00:00Z",
    category: null,
    summary: null,
    reason: null,
  };
  const itemCloseTimes = {
    title: "Item with same published and timeline time",
    links: { aihot: "https://aihot.example/items/3", original: "https://source.example/3" },
    source: { name: "Source" },
    publishedAt: "2026-10-27T03:00:00Z",
    timelineAt: "2026-10-27T03:00:30Z",
    discoveredAt: "2026-10-27T03:00:30Z",
    category: null,
    summary: null,
    reason: null,
  };
  const res = {
    schemaVersion: 1,
    query: { ...query, by: "timeline", q: null, ordering: "timelineDesc" },
    items: [itemWithSkew, itemWithoutTimeline, itemCloseTimes],
    page: { count: 3, hasMore: false, nextCursor: null },
  };
  const text = latestAnswer(res as never, query);

  // 1. Skew >= 1 min: outputs 站内时间 and 原文发布于
  assert.match(text, /站内时间 \S+ 13:00 · 原文发布于 \S+ 09:00/);

  // 2. Missing timelineAt: falls back to legacy 发布于
  assert.match(text, /发布于 \S+ 10:00/);

  // 3. Skew < 1 min (30s): only outputs 站内时间, does not repeat 原文发布于
  assert.match(text, /站内时间 \S+ 11:00(?!\s*·\s*原文发布于)/);

  // 4. BRIEF_HINTS includes timeline filtering hint
  assert.match(text, /按每条的「站内时间」过滤/);
});

test("a redirected path keeps `$` sequences literally", () => {
  const modules = MODULES as ModuleDeclaration[];
  modules.push({ name: "fork-redirect-test", redirects: [{ match: "prefix", path: "/test-prefix", status: 302, location: "/test-target*" }] });
  try {
    for (const tail of ["/a$`b", "/a$&b", "/a$'b", "/a$$b"]) {
      const decision = resolveRedirect(`/test-prefix${tail}`, "");
      assert.equal(decision?.location, `/test-target${tail}`, tail);
    }
  } finally {
    modules.pop();
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

test("sign-out cookies follow the request protocol even when the canonical site is HTTPS", async () => {
  const saved = config.siteUrl;
  (config as { siteUrl: string }).siteUrl = "https://aihot.example";
  const app = Fastify({ trustProxy: true });
  registerAdminAuth(app);
  await app.ready();
  try {
    for (const protocol of ["http", "https"]) {
      const response = await app.inject({
        method: "POST", url: "/api/auth/logout",
        headers: { "content-type": "application/x-www-form-urlencoded", "x-forwarded-proto": protocol },
        payload: "",
      });
      assert.equal(response.statusCode, 303);
      assert.equal(/; Secure(?:;|$)/.test(String(response.headers["set-cookie"])), protocol === "https");
    }
  } finally {
    (config as { siteUrl: string }).siteUrl = saved;
    await app.close();
  }
});
