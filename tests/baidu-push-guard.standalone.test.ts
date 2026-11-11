// Baidu push guard (fork-owned), failure modes it must stop:
// - a reply with remain -1, 1.5 or "3" is taken as a quota, then the next batch is empty and the run loops
//   forever POSTing nothing (Codex review F2);
// - the token is sent in clear text over http, or replayed to wherever a redirect points (F1);
// - a run that keeps getting "valid but useless" replies has no ceiling on requests or time.
import './setup.ts';
import assert from 'node:assert/strict';
import { afterEach, test } from 'node:test';
import { MAX_REQUESTS_PER_RUN, RUN_DEADLINE_MS, postUrls, runBudget, secureEndpoint, validRemain } from '@aihot/backend/operations/baidu-push-guard';

const originalFetch = globalThis.fetch;
afterEach(() => { globalThis.fetch = originalFetch; });
const HTTPS = 'https://data.zz.baidu.com/urls';
const SITE = 'https://example.test';
const reply = (remain: unknown) => { globalThis.fetch = async () => Response.json({ success: 1, remain }); };

test('only a non-negative safe integer counts as a remaining quota', () => {
  for (const ok of [0, 1, 2000, Number.MAX_SAFE_INTEGER]) assert.equal(validRemain(ok), true, String(ok));
  for (const bad of [-1, 1.5, '3', null, undefined, NaN, Infinity, Number.MAX_SAFE_INTEGER + 1]) assert.equal(validRemain(bad), false, String(bad));
});

test('a reply with a negative, fractional or non-numeric remain fails the run instead of being accepted', async () => {
  for (const bad of [-1, 1.5, '3', null]) {
    reply(bad);
    await assert.rejects(postUrls(HTTPS, SITE, 'tok', 'https://example.test/a'), /invalid remain/, String(bad));
  }
  reply(7);
  assert.deepEqual(await postUrls(HTTPS, SITE, 'tok', 'https://example.test/a'), { kind: 'accepted', remain: 7 });
});

test('over quota is told apart from failure, and other rejections still throw', async () => {
  globalThis.fetch = async () => Response.json({ error: 400, message: 'over quota' }, { status: 400 });
  assert.deepEqual(await postUrls(HTTPS, SITE, 'tok', 'x'), { kind: 'over-quota' });
  globalThis.fetch = async () => Response.json({ error: 401, message: 'token is not valid' }, { status: 401 });
  await assert.rejects(postUrls(HTTPS, SITE, 'tok', 'x'), /401 token is not valid/);
});

test('a clear-text endpoint is refused before any request, and the token never appears in the message', async () => {
  globalThis.fetch = async () => { throw new Error('made a network request'); };
  for (const endpoint of ['http://data.zz.baidu.com/urls', 'ftp://data.zz.baidu.com/urls', 'not a url', '']) {
    assert.throws(() => secureEndpoint(endpoint), /refused/, endpoint);
    await assert.rejects(postUrls(endpoint, SITE, 'secret-token-xyz', 'x'), (e: Error) => /refused/.test(e.message) && !e.message.includes('secret-token-xyz'));
  }
  assert.equal(secureEndpoint(HTTPS), HTTPS);
});

test('requests do not follow redirects, so the token is not replayed elsewhere', async () => {
  let redirectOption: RequestRedirect | undefined;
  globalThis.fetch = async (_url, init) => { redirectOption = init?.redirect; return Response.json({ remain: 1 }); };
  await postUrls(HTTPS, SITE, 'tok', 'x');
  assert.equal(redirectOption, 'error');
});

test('one run is capped in requests and in time', () => {
  const spend = runBudget();
  for (let n = 0; n < MAX_REQUESTS_PER_RUN; n++) spend();
  assert.throws(spend, /more than \d+ requests/);
  let t = 0;
  const timed = runBudget(() => t);
  timed();
  t = RUN_DEADLINE_MS + 1;
  assert.throws(timed, /deadline/);
});
