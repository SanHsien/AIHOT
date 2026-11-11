// The parts of Baidu's push that must not trust what comes back or where it goes (fork-owned file, see
// docs/DIVERGENCE.md): the token rides in the query string, so the endpoint must be https and must not
// redirect; the reply's `remain` drives how many URLs the next request carries, so a negative, fractional
// or non-numeric one must fail the run instead of producing empty batches that loop forever.

export const MAX_REQUESTS_PER_RUN = 50;
export const RUN_DEADLINE_MS = 5 * 60_000;

export type PushReply = { kind: "accepted"; remain: number } | { kind: "over-quota" };

/** A quota Baidu could really have left: a non-negative safe integer. */
export const validRemain = (value: unknown): value is number => Number.isSafeInteger(value) && (value as number) >= 0;

/** Refuses an endpoint that would send the token in clear text; the message names the setting, never the token. */
export function secureEndpoint(endpoint: string): string {
  let url: URL;
  try { url = new URL(endpoint); } catch { throw new Error("Baidu push refused: BAIDU_PUSH_ENDPOINT is not a valid URL"); }
  if (url.protocol !== "https:") {
    throw new Error("Baidu push refused: the endpoint is not https, so the token would travel in clear text (set BAIDU_PUSH_ENDPOINT to an https address Baidu documents)");
  }
  return endpoint;
}

/** One POST of newline-separated URLs. Anything but an accepted reply with a valid `remain` or "over quota" throws. */
export async function postUrls(endpoint: string, site: string, token: string, body: string): Promise<PushReply> {
  // The address as the platform shows it: site is the verified origin, unencoded.
  const res = await fetch(`${secureEndpoint(endpoint)}?site=${site}&token=${encodeURIComponent(token)}`, {
    method: "POST",
    headers: { "content-type": "text/plain" },
    body,
    redirect: "error", // a redirect would replay the token to wherever it points
    signal: AbortSignal.timeout(30_000),
  });
  const reply = await res.json().catch(() => null) as { remain?: unknown; message?: string } | null;
  if (res.ok && validRemain(reply?.remain)) return { kind: "accepted", remain: reply.remain };
  if (res.status === 400 && reply?.message === "over quota") return { kind: "over-quota" };
  // A revoked token, a site that lost its verification or Baidu being down fails the run, and a day of
  // failures becomes a follow-up (operations/alerts.ts); nothing of this request is counted as sent.
  const detail = res.ok ? `invalid remain ${JSON.stringify(reply?.remain) ?? "(none)"}` : reply?.message ?? "";
  throw new Error(`Baidu push failed: ${res.status} ${detail}`);
}

/** Caps how many requests and how long one run may spend, so a misbehaving reply cannot keep it looping. */
export function runBudget(now: () => number = Date.now) {
  const start = now();
  let requests = 0;
  return () => {
    if (++requests > MAX_REQUESTS_PER_RUN) throw new Error(`Baidu push failed: more than ${MAX_REQUESTS_PER_RUN} requests in one run`);
    if (now() - start > RUN_DEADLINE_MS) throw new Error("Baidu push failed: run exceeded its deadline");
  };
}
