// Helpers shared by the Pages Functions in functions/ that read and write Supabase.
//
// They use SUPABASE_SECRET_KEY (an encrypted Cloudflare variable), which bypasses Row Level
// Security, so the functions validate every input themselves. The key only exists on the
// server; it is never sent to the browser.

export interface Env {
  SUPABASE_URL: string;
  SUPABASE_SECRET_KEY: string;
}

export const json = (body: unknown, status = 200, headers: HeadersInit = {}) =>
  new Response(JSON.stringify(body), { status, headers: { 'Content-Type': 'application/json', ...headers } });

export function assertConfigured(env: Env): Response | null {
  if (env.SUPABASE_URL && env.SUPABASE_SECRET_KEY) return null;
  console.error('SUPABASE_URL / SUPABASE_SECRET_KEY are not set for this Pages project');
  return json({ success: false, error: 'This form is not available right now. Please try again later.' }, 503);
}

function headers(env: Env, extra: Record<string, string> = {}) {
  const h: Record<string, string> = { apikey: env.SUPABASE_SECRET_KEY, 'Content-Type': 'application/json', ...extra };
  // Legacy service_role keys are JWTs and also go in Authorization; sb_secret_ keys don't.
  if (env.SUPABASE_SECRET_KEY.startsWith('eyJ')) h.Authorization = `Bearer ${env.SUPABASE_SECRET_KEY}`;
  return h;
}

const rest = (env: Env, path: string) => `${env.SUPABASE_URL.replace(/\/$/, '')}/rest/v1/${path}`;

async function check(res: Response, what: string) {
  if (!res.ok) throw new Error(`${what}: ${res.status} ${await res.text()}`);
  return res;
}

/** GET rows. `query` is PostgREST syntax, e.g. "slug=eq.foo&select=id". */
export async function select<T = Record<string, any>>(env: Env, table: string, query: string): Promise<T[]> {
  const res = await check(await fetch(rest(env, `${table}?${query}`), { headers: headers(env) }), `select ${table}`);
  return res.json();
}

/** Number of rows matching `query`, without fetching them. */
export async function count(env: Env, table: string, query: string): Promise<number> {
  const res = await check(await fetch(rest(env, `${table}?select=id&${query}`), {
    method: 'HEAD',
    headers: headers(env, { Prefer: 'count=exact', Range: '0-0' }),
  }), `count ${table}`);
  return Number(res.headers.get('Content-Range')?.split('/')[1] ?? 0);
}

export async function insert<T = Record<string, any>>(env: Env, table: string, row: Record<string, unknown>): Promise<T> {
  const res = await check(await fetch(rest(env, table), {
    method: 'POST',
    headers: headers(env, { Prefer: 'return=representation' }),
    body: JSON.stringify(row),
  }), `insert ${table}`);
  return (await res.json())[0];
}

export async function update(env: Env, table: string, query: string, values: Record<string, unknown>) {
  await check(await fetch(rest(env, `${table}?${query}`), {
    method: 'PATCH',
    headers: headers(env, { Prefer: 'return=minimal' }),
    body: JSON.stringify(values),
  }), `update ${table}`);
}

export const clientIp = (request: Request) => request.headers.get('CF-Connecting-IP');

export const isEmail = (s: string) => /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(s);

/** Read a JSON body, or form fields if the page posted a regular form. */
export async function readBody(request: Request): Promise<Record<string, string>> {
  const type = request.headers.get('Content-Type') ?? '';
  try {
    if (type.includes('application/json')) return (await request.json()) as Record<string, string>;
    const form = await request.formData();
    return Object.fromEntries([...form.entries()].map(([k, v]) => [k, String(v)]));
  } catch {
    return {};
  }
}
