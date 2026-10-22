// /api/dummy/quota-status/ and /api/dummy/renew/, used by the Dummy JSON API playground.
//
// The Django site limited each IP to 30 requests per endpoint and stored the count in the
// database. The Cloudflare version has no per-request quota, so these always report that
// the caller is within the limit. Use a Cloudflare rate-limiting rule if abuse shows up.

const json = (body: unknown, status = 200) =>
  new Response(JSON.stringify(body), { status, headers: { 'Content-Type': 'application/json' } });

const ENDPOINTS = ['users', 'products', 'posts', 'comments', 'todos', 'companies'];

export const onRequest: PagesFunction = async ({ request, params }) => {
  const action = ([] as string[]).concat(params.path ?? []).filter(Boolean)[0];

  if (action === 'quota-status' && request.method === 'GET') {
    const endpoint = new URL(request.url).searchParams.get('endpoint');
    if (!endpoint) return json({ success: false, error: 'Endpoint is required' }, 400);
    return json({ success: true, endpoint, request_count: 0, limit: 30, is_blocked: false });
  }

  if (action === 'renew' && request.method === 'POST') {
    let endpoint = '';
    try {
      endpoint = String(((await request.json()) as { endpoint?: string }).endpoint ?? '');
    } catch {
      // handled below
    }
    if (!endpoint) return json({ success: false, error: 'Endpoint is required' }, 400);
    if (!ENDPOINTS.includes(endpoint)) return json({ success: false, error: 'Invalid endpoint' }, 400);
    return json({ success: true, message: `Quota reset for ${endpoint}`, endpoint });
  }

  return json({ success: false, error: 'Not found' }, 404);
};
