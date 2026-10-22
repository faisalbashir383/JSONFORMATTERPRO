// Webhook Tester API, ported from apiutils/views.py with the same responses:
//   POST /api/webhook/create/          new endpoint (expires after 24 hours)
//   GET  /api/webhook/list/            this browser's endpoints
//   GET  /api/webhook/<id>/requests/   last 100 captured requests
//   POST /api/webhook/<id>/clear/      delete captured requests  (owner only)
//   POST /api/webhook/<id>/delete/     delete the endpoint       (owner only)
//   POST /api/webhook/send/            send a test request to any URL
// Django let anyone clear or delete an endpoint by id; here only the browser that created it can.
import { assertConfigured, count, insert, json, readBody, remove, select, type Env } from '../../../server/supabase';
import { ENDPOINTS, REQUESTS, UUID_RE, LIFETIME_MS, session, sessionCookie, hookUrl, isExpired } from '../../../server/webhook';

const view = (request: Request, e: Record<string, any>, requestCount: number) => ({
  id: e.id, name: e.name, url: hookUrl(request, e.id), created_at: e.created_at, expires_at: e.expires_at,
  is_expired: isExpired(e), request_count: requestCount,
});

async function send(request: Request) {
  const data = await readBody(request) as Record<string, any>;
  const url = String(data.url ?? '');
  if (!url) return json({ error: 'URL is required' }, 400);
  try {
    new URL(url);
  } catch {
    return json({ error: 'Invalid URL' }, 400);
  }
  const method = String(data.method ?? 'POST').toUpperCase();
  const headers = data.headers && typeof data.headers === 'object' ? data.headers : {};
  const started = Date.now();
  try {
    const res = await fetch(url, {
      method,
      headers,
      body: ['GET', 'HEAD'].includes(method) ? undefined : String(data.body ?? ''),
      redirect: 'follow',
      signal: AbortSignal.timeout(30_000),
    });
    const body = await res.text();
    return json({
      status: res.status, status_text: res.statusText, headers: Object.fromEntries(res.headers),
      body, time_ms: Math.round((Date.now() - started) * 100) / 100, url: res.url,
    });
  } catch (e) {
    const msg = String(e);
    if (/timeout|abort/i.test(msg)) return json({ error: 'Request timed out (30s limit)' }, 504);
    return json({ error: `Connection failed: ${msg}` }, 502);
  }
}

export const onRequest: PagesFunction<Env> = async ({ request, env, params }) => {
  const notConfigured = assertConfigured(env);
  if (notConfigured) return notConfigured;
  const [first, second] = ([] as string[]).concat(params.path ?? []).filter(Boolean);
  const method = request.method;
  const sid = session(request);
  const withCookie = (res: Response) => {
    if (sid.isNew) res.headers.append('Set-Cookie', sessionCookie(sid.id));
    return res;
  };

  try {
    if (first === 'create' && method === 'POST') {
      const data = await readBody(request);
      const now = new Date();
      const e = await insert(env, ENDPOINTS, {
        id: crypto.randomUUID(),
        name: String(data.name ?? '').slice(0, 100),
        created_at: now.toISOString(),
        expires_at: new Date(now.getTime() + LIFETIME_MS).toISOString(),
        session_key: sid.id,
      });
      return withCookie(json(view(request, e, 0)));
    }

    if (first === 'list' && method === 'GET') {
      if (sid.isNew) return json({ endpoints: [] });
      const rows = await select(env, ENDPOINTS, `session_key=eq.${sid.id}&order=created_at.desc&limit=50`);
      const counts = await Promise.all(rows.map((e) => count(env, REQUESTS, `endpoint_id=eq.${e.id}`)));
      return json({ endpoints: rows.map((e, i) => view(request, e, counts[i])) });
    }

    if (first === 'send' && method === 'POST') return await send(request);

    if (first && UUID_RE.test(first)) {
      const [e] = await select(env, ENDPOINTS, `id=eq.${first}&limit=1`);
      if (!e) return json({ error: 'Not found' }, 404);

      if (second === 'requests' && method === 'GET') {
        const rows = await select(env, REQUESTS, `endpoint_id=eq.${first}&order=received_at.desc&limit=100`);
        return json({
          endpoint_id: e.id, is_expired: isExpired(e), expires_at: e.expires_at,
          requests: rows.map((r) => ({
            id: r.id, method: r.method, headers: r.headers, body: r.body, content_type: r.content_type,
            query_params: r.query_params, ip_address: r.ip_address, received_at: r.received_at,
          })),
        });
      }
      if ((second === 'clear' || second === 'delete') && method === 'POST') {
        if (e.session_key !== sid.id) return json({ error: 'You can only change endpoints created in this browser' }, 403);
        const deleted = await remove(env, REQUESTS, `endpoint_id=eq.${first}`);
        if (second === 'clear') return json({ success: true, deleted });
        await remove(env, ENDPOINTS, `id=eq.${first}`);
        return json({ success: true });
      }
    }
  } catch (err) {
    console.error(err);
    return json({ error: 'Something went wrong. Please try again.' }, 500);
  }
  return json({ error: 'Not found' }, 404);
};
