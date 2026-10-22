// Mock API management, ported from formatter/views.py with the same responses:
//   POST /api/mock/create/              create (max 5 per IP)
//   GET  /api/mock/my-endpoints/        endpoints created from this IP
//   GET  /api/mock/share/<token>/       config for sharing
//   POST /api/mock/clone/<token>/       copy a shared endpoint
//   GET  /api/mock/<id>/info/           details
//   POST /api/mock/<id>/update/         edit (creator IP only)
//   POST /api/mock/<id>/delete/         delete (creator IP only)
//   ANY  /api/mock/<id>/                serve the mock
// Ownership is by IP address, as on the Django site.
import { assertConfigured, clientIp, count, insert, json, remove, select, update, type Env } from '../../../server/supabase';
import { TABLE, UUID_RE, MAX_ENDPOINTS_PER_IP, MOCK_CORS, allowedIps, mockUrl, serveMock } from '../../../server/mock';

const shareToken = () => btoa(String.fromCharCode(...crypto.getRandomValues(new Uint8Array(32))))
  .replace(/\+/g, '-').replace(/\//g, '_').replace(/=+$/, '');
const site = (request: Request) => new URL(request.url).origin;
const asText = (v: unknown, fallback: string) => (v === undefined ? fallback : typeof v === 'string' ? v : JSON.stringify(v));
const int = (v: unknown, fallback: number, min = 0, max = Number.MAX_SAFE_INTEGER) => {
  const n = parseInt(String(v ?? fallback), 10);
  return Math.min(Math.max(Number.isNaN(n) ? fallback : n, min), max);
};

async function readJson(request: Request) {
  try {
    return (await request.json()) as Record<string, any>;
  } catch {
    return null;
  }
}

async function create(request: Request, env: Env, cloneOf?: Record<string, any>) {
  const ip = clientIp(request);
  let row: Record<string, unknown>;
  if (cloneOf) {
    row = {
      name: cloneOf.name ? `${cloneOf.name} (Clone)` : 'Cloned Endpoint',
      ...Object.fromEntries(['path', 'method', 'status_code', 'response_body', 'latency_ms', 'error_rate', 'record_count',
        'conditional_rules', 'validation_schema', 'auth_config', 'custom_headers'].map((k) => [k, cloneOf[k]])),
      ip_restriction_enabled: false,
      allowed_ips: '',
    };
  } else {
    const data = await readJson(request);
    if (!data) return json({ success: false, error: 'Invalid JSON in request body' }, 400);
    if (!data.response_body) return json({ success: false, error: 'response_body is required' }, 400);
    if (String(data.response_body).length > 100_000) return json({ success: false, error: 'response_body is too large (100 KB max)' }, 400);
    row = {
      name: String(data.name ?? '').slice(0, 100),
      path: String(data.path ?? '/api/users').trim().replace(/^\/+|\/+$/g, '').slice(0, 200),
      method: String(data.method ?? 'GET').toUpperCase().slice(0, 10),
      status_code: int(data.status_code, 200, 100, 599),
      response_body: String(data.response_body),
      latency_ms: int(data.latency_ms, 0, 0, 10_000),
      error_rate: int(data.error_rate, 0, 0, 100),
      record_count: int(data.record_count, 1, 1, 1000),
      ip_restriction_enabled: Boolean(data.ip_restriction_enabled),
      allowed_ips: String(data.allowed_ips ?? ''),
      custom_headers: asText(data.custom_headers, '{}'),
      conditional_rules: asText(data.conditional_rules, '[]'),
      validation_schema: asText(data.validation_schema, '{}'),
      auth_config: asText(data.auth_config, '{}'),
    };
  }

  const existing = await count(env, TABLE, `creator_ip=eq.${encodeURIComponent(ip ?? '')}`);
  if (existing >= MAX_ENDPOINTS_PER_IP) {
    return json({ success: false, error: `You have reached the maximum limit of ${MAX_ENDPOINTS_PER_IP} endpoints. Please delete an existing endpoint to create a new one.`,
      limit: MAX_ENDPOINTS_PER_IP, current_count: existing }, 400);
  }

  const now = new Date().toISOString();
  const ep = await insert(env, TABLE, {
    ...row,
    endpoint_id: crypto.randomUUID(),
    content_type: 'application/json',
    is_public: true,
    share_token: shareToken(),
    creator_ip: ip,
    created_at: now,
    updated_at: now,
    request_count: 0,
  });
  const auth = JSON.parse(asText(ep.auth_config, '{}') || '{}');
  return json({
    success: true,
    endpoint_id: ep.endpoint_id,
    endpoint_url: mockUrl(site(request), ep.path, ep.endpoint_id),
    share_url: `${site(request)}/mock-api/?share=${ep.share_token}`,
    share_token: ep.share_token,
    method: ep.method,
    path: `/${ep.path}`,
    ...(cloneOf ? { message: 'Endpoint cloned successfully' } : {
      ip_restriction_enabled: ep.ip_restriction_enabled,
      allowed_ips: allowedIps(ep.allowed_ips),
      has_conditional_rules: ep.conditional_rules !== '[]' && Boolean(ep.conditional_rules),
      has_validation: ep.validation_schema !== '{}' && Boolean(ep.validation_schema),
      has_auth: Boolean(auth?.type),
      created_at: ep.created_at,
      message: 'Mock endpoint created successfully',
    }),
  }, 201);
}

async function listMine(request: Request, env: Env) {
  const ip = clientIp(request) ?? '';
  const rows = await select(env, TABLE, `creator_ip=eq.${encodeURIComponent(ip)}&order=created_at.desc&limit=20`);
  const endpoints = rows.map((ep) => ({
    endpoint_id: ep.endpoint_id,
    endpoint_url: mockUrl(site(request), ep.path, ep.endpoint_id),
    name: ep.name,
    path: `/${(ep.path || 'api/mock').replace(/^\/+|\/+$/g, '')}`,
    method: ep.method,
    status_code: ep.status_code,
    record_count: ep.record_count,
    response_body: ep.response_body,
    ip_restriction_enabled: ep.ip_restriction_enabled,
    allowed_ips: allowedIps(ep.allowed_ips),
    request_count: ep.request_count,
    created_at: ep.created_at,
    is_expired: Boolean(ep.expires_at && Date.parse(ep.expires_at) < Date.now()),
  }));
  return json({ success: true, count: endpoints.length, limit: MAX_ENDPOINTS_PER_IP,
    remaining: Math.max(0, MAX_ENDPOINTS_PER_IP - endpoints.length), endpoints, your_ip: ip });
}

async function byShareToken(env: Env, token: string) {
  const [ep] = await select(env, TABLE, `share_token=eq.${encodeURIComponent(token)}&limit=1`);
  return ep;
}

async function owned(request: Request, env: Env, endpointId: string, verb: string) {
  const [ep] = await select(env, TABLE, `endpoint_id=eq.${endpointId}&limit=1`);
  if (!ep) return { error: json({ success: false, error: 'Endpoint not found' }, 404) };
  if (ep.creator_ip && ep.creator_ip !== clientIp(request)) {
    return { error: json({ success: false, error: `You can only ${verb} endpoints you created` }, 403) };
  }
  return { ep };
}

export const onRequest: PagesFunction<Env> = async ({ request, env, params, waitUntil }) => {
  const parts = ([] as string[]).concat(params.path ?? []).filter(Boolean);
  const [first, second] = parts;
  const method = request.method;

  if (method === 'OPTIONS' && first && UUID_RE.test(first)) return new Response(null, { status: 204, headers: MOCK_CORS });
  const notConfigured = assertConfigured(env);
  if (notConfigured) return notConfigured;

  try {
    if (first === 'create' && method === 'POST') return await create(request, env);
    if (first === 'my-endpoints' && method === 'GET') return await listMine(request, env);

    if (first === 'share' && second) {
      const ep = await byShareToken(env, second);
      if (!ep) return json({ error: 'Endpoint not found', message: 'Invalid or expired share token' }, 404);
      return json({ success: true, config: Object.fromEntries(['name', 'path', 'method', 'status_code', 'response_body',
        'latency_ms', 'error_rate', 'record_count', 'conditional_rules', 'validation_schema', 'auth_config', 'custom_headers']
        .map((k) => [k, ep[k]])) });
    }
    if (first === 'clone' && second) {
      if (method !== 'POST') return json({ error: 'Method not allowed' }, 405);
      const ep = await byShareToken(env, second);
      if (!ep) return json({ error: 'Endpoint not found', message: 'Invalid or expired share token' }, 404);
      return await create(request, env, ep);
    }

    if (first && UUID_RE.test(first)) {
      if (second === 'info' && method === 'GET') {
        const [ep] = await select(env, TABLE, `endpoint_id=eq.${first}&limit=1`);
        if (!ep) return json({ success: false, error: 'Endpoint not found' }, 404);
        return json({ success: true, endpoint_id: ep.endpoint_id, endpoint_url: `${site(request)}/api/mock/${ep.endpoint_id}/`,
          name: ep.name, path: ep.path, method: ep.method, status_code: ep.status_code, latency_ms: ep.latency_ms,
          error_rate: ep.error_rate, ip_restriction_enabled: ep.ip_restriction_enabled, request_count: ep.request_count,
          created_at: ep.created_at, last_accessed: ep.last_accessed,
          is_expired: Boolean(ep.expires_at && Date.parse(ep.expires_at) < Date.now()) });
      }
      if (second === 'delete' && (method === 'POST' || method === 'DELETE')) {
        const { ep, error } = await owned(request, env, first, 'delete');
        if (error) return error;
        await remove(env, TABLE, `id=eq.${ep.id}`);
        return json({ success: true, message: 'Endpoint deleted successfully' });
      }
      if (second === 'update' && ['POST', 'PUT', 'PATCH'].includes(method)) {
        const { ep, error } = await owned(request, env, first, 'edit');
        if (error) return error;
        const data = await readJson(request);
        if (!data) return json({ success: false, error: 'Invalid JSON in request body' }, 400);
        const changes: Record<string, unknown> = { updated_at: new Date().toISOString() };
        if ('name' in data) changes.name = String(data.name).slice(0, 100);
        if ('allowed_ips' in data) changes.allowed_ips = String(data.allowed_ips);
        if ('ip_restriction_enabled' in data) changes.ip_restriction_enabled = Boolean(data.ip_restriction_enabled);
        if ('record_count' in data) changes.record_count = int(data.record_count, ep.record_count, 1, 1000);
        if (typeof data.response_body === 'string' && data.response_body.trim()) changes.response_body = data.response_body;
        await update(env, TABLE, `id=eq.${ep.id}`, changes);
        const merged = { ...ep, ...changes };
        return json({ success: true, endpoint_id: ep.endpoint_id, endpoint_url: `${site(request)}/api/mock/${ep.endpoint_id}/`,
          name: merged.name, ip_restriction_enabled: merged.ip_restriction_enabled, allowed_ips: allowedIps(String(merged.allowed_ips)),
          record_count: merged.record_count, message: 'Endpoint updated successfully' });
      }
      if (!second) return await serveMock(request, env, first, waitUntil);
    }
  } catch (e) {
    console.error(e);
    return json({ success: false, error: 'Something went wrong. Please try again.' }, 500);
  }
  return json({ success: false, error: 'Not found' }, 404);
};
