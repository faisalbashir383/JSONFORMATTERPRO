// ANY /hook/<id>/  Captures an incoming webhook (capture_webhook in apiutils/views.py).
// Bodies over 256 KB are truncated so one large payload can't fill the database.
import { assertConfigured, clientIp, insert, json, select, type Env } from '../../server/supabase';
import { ENDPOINTS, REQUESTS, UUID_RE, MAX_BODY_BYTES, isExpired } from '../../server/webhook';

const CORS = { 'Access-Control-Allow-Origin': '*', 'Access-Control-Allow-Methods': '*', 'Access-Control-Allow-Headers': '*' };

export const onRequest: PagesFunction<Env> = async ({ request, env, params }) => {
  if (request.method === 'OPTIONS') return new Response(null, { status: 204, headers: CORS });
  const notConfigured = assertConfigured(env);
  if (notConfigured) return notConfigured;

  const id = ([] as string[]).concat(params.path ?? []).filter(Boolean)[0];
  if (!id || !UUID_RE.test(id)) return json({ error: 'Endpoint not found' }, 404, CORS);
  try {
    const [e] = await select(env, ENDPOINTS, `id=eq.${id}&limit=1`);
    if (!e) return json({ error: 'Endpoint not found' }, 404, CORS);
    if (isExpired(e)) return json({ error: 'Endpoint expired' }, 410, CORS);

    const raw = new Uint8Array(await request.arrayBuffer());
    let body = new TextDecoder('utf-8').decode(raw.slice(0, MAX_BODY_BYTES));
    if (raw.length > MAX_BODY_BYTES) body += `\n\n[truncated: ${raw.length} bytes received, first ${MAX_BODY_BYTES} kept]`;

    // Same shapes as Django: headers as a flat object, query params as { key: [values] }.
    const query: Record<string, string[]> = {};
    for (const [k, v] of new URL(request.url).searchParams) (query[k] ??= []).push(v);
    const headers = Object.fromEntries([...request.headers].filter(([k]) => !k.startsWith('cf-') && k !== 'x-real-ip'));

    await insert(env, REQUESTS, {
      endpoint_id: id,
      method: request.method,
      headers,
      body,
      content_type: (request.headers.get('Content-Type') ?? '').split(';')[0].slice(0, 100),
      query_params: query,
      ip_address: clientIp(request),
      received_at: new Date().toISOString(),
    });
    return json({ success: true, message: 'Webhook received' }, 200, CORS);
  } catch (err) {
    console.error(err);
    return json({ error: 'Could not store the request' }, 500, CORS);
  }
};
