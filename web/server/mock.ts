// Mock API engine, ported from formatter/views.py (process_template_variables, validate_auth,
// evaluate_conditional_rules, validate_request, serve_mock_endpoint). Used by
// functions/api/mock/[[path]].ts and the /api/<path>/<uuid>/ catch-all in functions/api/[[path]].ts.
import { clientIp, select, update, type Env } from './supabase';

export const TABLE = 'formatter_mockendpoint';
export const UUID_RE = /^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/;
export const MAX_ENDPOINTS_PER_IP = 5;
const MAX_LATENCY_MS = 10_000;

export const MOCK_CORS = {
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Methods': 'GET, POST, PUT, PATCH, DELETE, OPTIONS',
  'Access-Control-Allow-Headers': 'Content-Type, Authorization, X-API-Key',
};

const mockJson = (body: unknown, status = 200, extra: Record<string, string> = {}) =>
  // Same precedence as Django: custom headers can replace Content-Type, but the CORS headers win.
  new Response(JSON.stringify(body), { status, headers: { 'Content-Type': 'application/json', ...extra, ...MOCK_CORS } });

/** Public URL of a mock. Paths are served under /api/ (see the README). */
export function mockUrl(siteUrl: string, path: string, endpointId: string) {
  const p = (path || 'api/mock').replace(/^\/+|\/+$/g, '');
  return `${siteUrl}/${p.startsWith('api/') || p === 'api' ? p : `api/${p}`}/${endpointId}/`;
}

export const allowedIps = (s: string) => (s || '').split(',').map((ip) => ip.trim()).filter(Boolean);

const parseJson = <T>(s: unknown, fallback: T): T => {
  if (typeof s !== 'string' || !s) return (s as T) ?? fallback;
  try {
    return JSON.parse(s) as T;
  } catch {
    return fallback;
  }
};

// ---------------------------------------------------------------- template variables

const FIRST = ['James', 'Emma', 'Liam', 'Olivia', 'Noah', 'Ava', 'Ethan', 'Sophia', 'Mason', 'Isabella'];
const LAST = ['Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia', 'Miller', 'Davis', 'Rodriguez', 'Martinez'];
const COMPANIES = ['TechCorp', 'Innovate Inc', 'Digital Dynamics', 'CloudFirst', 'DataDriven', 'NetSolutions'];
const JOBS = ['Software Engineer', 'Product Manager', 'UX Designer', 'Data Scientist', 'DevOps Engineer'];
const CITIES = ['New York', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix', 'San Francisco', 'Seattle'];
const COUNTRIES = ['United States', 'Canada', 'United Kingdom', 'Germany', 'France', 'Australia', 'Japan'];
const STREETS = ['Main St', 'Oak Ave', 'Park Blvd', 'Maple Dr', 'Cedar Ln', 'Elm St', 'Pine Rd'];
const WORDS = ['lorem', 'ipsum', 'dolor', 'sit', 'amet', 'consectetur', 'adipiscing', 'elit', 'sed', 'do', 'eiusmod',
  'tempor', 'incididunt', 'ut', 'labore', 'et', 'dolore', 'magna', 'aliqua'];

const pick = <T>(list: T[]) => list[Math.floor(Math.random() * list.length)];
const rint = (a: number, b: number) => a + Math.floor(Math.random() * (b - a + 1));
const hex = (bytes: number) => [...crypto.getRandomValues(new Uint8Array(bytes))].map((b) => b.toString(16).padStart(2, '0')).join('');
const pad = (n: number) => String(n).padStart(2, '0');
const pastDate = () => new Date(Date.now() - rint(0, 365) * 86_400_000);
const sentence = () => {
  const s = Array.from({ length: rint(8, 15) }, () => pick(WORDS)).join(' ');
  return s[0].toUpperCase() + s.slice(1) + '.';
};

const VARIABLES: [RegExp, (...groups: string[]) => string][] = [
  [/\{\{uuid\}\}/g, () => crypto.randomUUID()],
  [/\{\{id\}\}/g, () => String(rint(1, 99999))],
  [/\{\{firstName\}\}/g, () => pick(FIRST)],
  [/\{\{lastName\}\}/g, () => pick(LAST)],
  [/\{\{fullName\}\}/g, () => `${pick(FIRST)} ${pick(LAST)}`],
  [/\{\{username\}\}/g, () => `${pick(FIRST).toLowerCase()}${rint(10, 999)}`],
  [/\{\{email\}\}/g, () => `${pick(FIRST).toLowerCase()}.${pick(LAST).toLowerCase()}@${pick(['gmail.com', 'yahoo.com', 'outlook.com', 'example.com'])}`],
  [/\{\{phone\}\}/g, () => `+1 ${rint(200, 999)}-${rint(200, 999)}-${rint(1000, 9999)}`],
  [/\{\{company\}\}/g, () => pick(COMPANIES)],
  [/\{\{jobTitle\}\}/g, () => pick(JOBS)],
  [/\{\{street\}\}/g, () => `${rint(100, 9999)} ${pick(STREETS)}`],
  [/\{\{city\}\}/g, () => pick(CITIES)],
  [/\{\{country\}\}/g, () => pick(COUNTRIES)],
  [/\{\{isoDate\}\}/g, () => pastDate().toISOString().replace('Z', '')],
  [/\{\{date\}\}/g, () => pastDate().toISOString().slice(0, 10)],
  [/\{\{datetime\}\}/g, () => pastDate().toISOString().slice(0, 19).replace('T', ' ')],
  [/\{\{time\}\}/g, () => `${pad(rint(0, 23))}:${pad(rint(0, 59))}:${pad(rint(0, 59))}`],
  [/\{\{boolean\}\}/g, () => String(Math.random() < 0.5)],
  [/\{\{number:(\d+),(\d+)\}\}/g, (a, b) => String(rint(Number(a), Number(b)))],
  [/\{\{number:(\d+)\}\}/g, (a) => String(rint(0, Number(a)))],
  [/\{\{float:(\d+),(\d+)\}\}/g, (a, b) => (Number(a) + Math.random() * (Number(b) - Number(a))).toFixed(2)],
  [/\{\{percentage\}\}/g, () => String(rint(0, 100))],
  [/\{\{oneOf:([^}]+)\}\}/g, (list) => pick(list.split(','))],
  [/\{\{avatar\}\}/g, () => `https://i.pravatar.cc/150?img=${rint(1, 70)}`],
  [/\{\{imageUrl\}\}/g, () => `https://picsum.photos/seed/${rint(1, 1000)}/400/300`],
  [/\{\{zipCode\}\}/g, () => String(rint(10000, 99999))],
  [/\{\{url\}\}/g, () => `https://example.com/${pick(['products', 'users', 'posts', 'articles', 'pages', 'items'])}/${rint(1, 9999)}`],
  [/\{\{slug\}\}/g, () => Array.from({ length: rint(2, 4) }, () => pick(WORDS)).join('-')],
  [/\{\{paragraph\}\}/g, () => Array.from({ length: rint(3, 6) }, sentence).join(' ')],
  [/\{\{sentence\}\}/g, () => sentence()],
  [/\{\{color\}\}/g, () => `#${hex(3)}`],
  [/\{\{hexColor\}\}/g, () => `#${hex(3)}`],
  [/\{\{creditCard\}\}/g, () => `4${rint(100, 999)} ${rint(1000, 9999)} ${rint(1000, 9999)} ${rint(1000, 9999)}`],
  [/\{\{price\}\}/g, () => `${rint(1, 999)}.${pad(rint(0, 99))}`],
  [/\{\{ipAddress\}\}/g, () => `${rint(1, 255)}.${rint(0, 255)}.${rint(0, 255)}.${rint(1, 255)}`],
  [/\{\{macAddress\}\}/g, () => Array.from({ length: 6 }, () => hex(1)).join(':')],
  [/\{\{lorem:(\d+)\}\}/g, (n) => Array.from({ length: Number(n) }, () => pick(WORDS)).join(' ')],
];

export function processTemplate(template: string) {
  let out = template;
  for (const [re, gen] of VARIABLES) out = out.replace(re, (_m, ...g) => gen(...(g.slice(0, -2) as string[])));
  return out;
}

/** Repeat the first object of the template's "data" array record_count times (fresh values each). */
function renderBody(template: string, recordCount: number): unknown {
  const count = Math.max(1, recordCount);
  const dataAt = template.indexOf('"data"');
  const bracket = dataAt === -1 ? -1 : template.indexOf('[', dataAt);
  const objStart = bracket === -1 ? -1 : template.indexOf('{', bracket);
  let processed: string;
  if (objStart !== -1) {
    let depth = 1, pos = objStart + 1;
    while (pos < template.length && depth > 0) {
      if (template[pos] === '{') depth++;
      else if (template[pos] === '}') depth--;
      pos++;
    }
    const item = template.slice(objStart, pos);
    const arrayEnd = template.indexOf(']', pos);
    const items = Array.from({ length: count }, () => processTemplate(item)).join(',\n');
    processed = processTemplate(template.slice(0, bracket + 1) + items + template.slice(arrayEnd));
  } else {
    processed = processTemplate(template);
  }
  try {
    return JSON.parse(processed);
  } catch {
    try {
      return JSON.parse(processTemplate(template));
    } catch {
      return { raw_response: processTemplate(template) };
    }
  }
}

// ---------------------------------------------------------------- request checks

interface Incoming { method: string; headers: Headers; query: URLSearchParams; body: Record<string, any> }

function checkAuth(req: Incoming, raw: unknown): string | null {
  const cfg = parseJson<Record<string, string>>(raw, {});
  const type = (cfg.type || '').toLowerCase();
  if (type === 'api_key') {
    const header = cfg.header_name || 'X-API-Key';
    const provided = req.headers.get(header) || req.query.get('api_key');
    if (!provided) return `Missing API key. Provide via '${header}' header or 'api_key' query param`;
    return provided === cfg.api_key ? null : 'Invalid API key';
  }
  if (type === 'bearer' || type === 'basic') {
    const auth = req.headers.get('Authorization') || '';
    if (!auth) return 'Missing Authorization header';
    if (type === 'bearer') {
      if (!auth.startsWith('Bearer ')) return 'Invalid Authorization header format. Expected: Bearer <token>';
      return auth.slice(7) === cfg.token ? null : 'Invalid bearer token';
    }
    if (!auth.startsWith('Basic ')) return 'Invalid Authorization header format. Expected: Basic <base64>';
    try {
      const decoded = new TextDecoder().decode(Uint8Array.from(atob(auth.slice(6)), (c) => c.charCodeAt(0)));
      const i = decoded.indexOf(':');
      if (i < 0) return 'Invalid Basic auth encoding';
      return decoded.slice(0, i) === cfg.username && decoded.slice(i + 1) === cfg.password ? null : 'Invalid credentials';
    } catch {
      return 'Invalid Basic auth encoding';
    }
  }
  return null;
}

function validationErrors(req: Incoming, raw: unknown, bodyIsJson: boolean): string[] {
  const schema = parseJson<Record<string, any>>(raw, {});
  const errors: string[] = [];
  for (const h of schema.required_headers ?? []) if (!req.headers.get(h)) errors.push(`Missing required header: ${h}`);
  for (const p of schema.required_params ?? []) if (!req.query.has(p)) errors.push(`Missing required query parameter: ${p}`);
  const bodySchema = schema.body_schema ?? {};
  if (Object.keys(bodySchema).length) {
    if (!bodyIsJson && bodySchema.required?.length) errors.push('Invalid or missing request body (expected JSON)');
    for (const f of bodySchema.required ?? []) if (!(f in req.body)) errors.push(`Missing required body field: ${f}`);
    for (const [f, t] of Object.entries<string>(bodySchema.types ?? {})) {
      if (!(f in req.body)) continue;
      const v = req.body[f];
      const ok = t === 'string' ? typeof v === 'string'
        : t === 'number' ? typeof v === 'number'
        : t === 'boolean' ? typeof v === 'boolean'
        : t === 'array' ? Array.isArray(v)
        : t === 'object' ? v !== null && typeof v === 'object' && !Array.isArray(v)
        : true;
      if (!ok) errors.push(`Field '${f}' must be ${t === 'array' || t === 'object' ? 'an' : 'a'} ${t}`);
    }
  }
  return errors;
}

function matchRule(req: Incoming, raw: unknown): { status_code?: number; body?: unknown } | null {
  const rules = parseJson<any[]>(raw, []);
  for (const rule of Array.isArray(rules) ? rules : []) {
    const conditions: any[] = rule.conditions ?? [];
    if (!conditions.length) continue;
    const all = conditions.every((c) => {
      const op = c.operator || 'equals';
      const value = String(c.value ?? '');
      const actual = c.type === 'header' ? req.headers.get(c.key)
        : c.type === 'query' ? req.query.get(c.key)
        : c.type === 'body' ? (req.body[c.key] === undefined ? null : req.body[c.key])
        : undefined;
      if (actual === undefined) return true; // unknown condition type: ignored, as in Django
      const missing = actual === null || (c.type === 'header' && actual === '');
      if (op === 'missing') return missing;
      if (op === 'present') return !missing;
      if (op === 'equals') return !missing && String(actual) === value;
      if (op === 'contains') return !missing && String(actual).includes(value);
      return true;
    });
    if (all) return rule.response ?? {};
  }
  return null;
}

function filterByQuery(data: any, query: URLSearchParams) {
  if (!data || typeof data !== 'object' || !Array.isArray(data.data) || ![...query.keys()].length) return data;
  const id = query.get('id');
  if (id) {
    const match = data.data.find((it: any) => it && typeof it === 'object' && String(it.id ?? it._id ?? it.uuid ?? it.ID) === id);
    if (match) return { success: true, data: match };
    if (data.data.length && typeof data.data[0] === 'object') return { success: true, data: { ...data.data[0], id } };
    return { success: false, error: 'Record not found', id };
  }
  for (const [key, value] of query) {
    if (['format', 'callback', '_', 'api_key'].includes(key)) continue;
    const filtered = data.data.filter((it: any) => it && typeof it === 'object' && String(it[key] ?? '').toLowerCase() === value.toLowerCase());
    if (filtered.length) return { ...data, data: filtered, filtered_by: { [key]: value } };
  }
  return data;
}

// ---------------------------------------------------------------- serve

export async function serveMock(request: Request, env: Env, endpointId: string, waitUntil: (p: Promise<unknown>) => void) {
  if (request.method === 'OPTIONS') return new Response(null, { status: 204, headers: MOCK_CORS });

  const [ep] = await select(env, TABLE, `endpoint_id=eq.${endpointId}&limit=1`);
  if (!ep) return mockJson({ error: 'Not Found', message: 'Mock endpoint does not exist or has been deleted', status: 404 }, 404);
  if (ep.expires_at && Date.parse(ep.expires_at) < Date.now()) {
    return mockJson({ error: 'Gone', message: 'This mock endpoint has expired', status: 410 }, 410);
  }

  const ip = clientIp(request) ?? '';
  if (ep.ip_restriction_enabled && !allowedIps(ep.allowed_ips).includes(ip)) {
    return mockJson({ error: 'Forbidden', message: 'Your IP address is not authorized to access this endpoint',
      your_ip: ip, allowed_ips: allowedIps(ep.allowed_ips), status: 403 }, 403);
  }
  if (request.method !== ep.method) {
    return mockJson({ error: 'Method Not Allowed', message: `This endpoint only accepts ${ep.method} requests`, status: 405 }, 405);
  }

  const text = request.method === 'GET' || request.method === 'HEAD' ? '' : await request.text();
  let body: Record<string, any> = {};
  let bodyIsJson = false;
  if (text) {
    try {
      const parsed = JSON.parse(text);
      if (parsed && typeof parsed === 'object' && !Array.isArray(parsed)) { body = parsed; bodyIsJson = true; }
    } catch { /* not JSON */ }
  }
  const incoming: Incoming = { method: request.method, headers: request.headers, query: new URL(request.url).searchParams, body };

  const authError = checkAuth(incoming, ep.auth_config);
  if (authError) return mockJson({ error: 'Unauthorized', message: authError, status: 401 }, 401);
  const errors = validationErrors(incoming, ep.validation_schema, bodyIsJson);
  if (errors.length) return mockJson({ error: 'Bad Request', message: 'Request validation failed', validation_errors: errors, status: 400 }, 400);

  const sleep = () => new Promise((r) => setTimeout(r, Math.min(ep.latency_ms || 0, MAX_LATENCY_MS)));
  const touch = () => waitUntil(update(env, TABLE, `id=eq.${ep.id}`, {
    request_count: (ep.request_count || 0) + 1, last_accessed: new Date().toISOString(),
  }).catch(() => undefined));

  const rule = matchRule(incoming, ep.conditional_rules);
  if (rule) {
    if (ep.latency_ms > 0) await sleep();
    touch();
    return mockJson(rule.body ?? {}, rule.status_code ?? 200, { 'X-Mock-Rule-Matched': 'true' });
  }

  if (ep.latency_ms > 0) await sleep();
  if (ep.error_rate > 0 && rint(1, 100) <= ep.error_rate) {
    return mockJson({ error: 'Internal Server Error', message: 'Simulated server error (based on configured error rate)', status: 500 }, 500);
  }
  touch();

  const data = filterByQuery(renderBody(ep.response_body, ep.record_count), incoming.query);
  const custom = parseJson<Record<string, string>>(ep.custom_headers, {});
  const extra: Record<string, string> = {};
  for (const [k, v] of Object.entries(custom ?? {})) if (typeof v === 'string' && /^[\w-]+$/.test(k)) extra[k] = v;
  return mockJson(data, ep.status_code || 200, extra);
}
