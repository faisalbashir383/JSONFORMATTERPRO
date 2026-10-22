// Catch-all for /api/* paths that no more specific function handles.
// Serves mock endpoints at their public URL /api/<path>/<endpoint-id>/ (see server/mock.ts);
// everything else is a JSON 404.
import { assertConfigured, json, type Env } from '../../server/supabase';
import { MOCK_CORS, UUID_RE, serveMock } from '../../server/mock';

export const onRequest: PagesFunction<Env> = async ({ request, env, params, waitUntil }) => {
  const parts = ([] as string[]).concat(params.path ?? []).filter(Boolean);
  const last = parts[parts.length - 1];
  if (parts.length >= 2 && last && UUID_RE.test(last)) {
    if (request.method === 'OPTIONS') return new Response(null, { status: 204, headers: MOCK_CORS });
    const notConfigured = assertConfigured(env);
    if (notConfigured) return notConfigured;
    try {
      return await serveMock(request, env, last, waitUntil);
    } catch (e) {
      console.error(e);
      return json({ error: 'Internal Server Error', message: 'Could not load this mock endpoint', status: 500 }, 500);
    }
  }
  return json({ success: false, error: 'Not found' }, 404);
};
