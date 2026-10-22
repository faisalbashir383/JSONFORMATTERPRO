// POST /api/cors-checker/  { url, origin? }
//
// Port of cors_checker_api in formatter/views.py, same response shape: sends an OPTIONS and a
// GET with the test Origin and reports the Access-Control-* headers from the GET response.
import { json, readBody } from '../../../server/supabase';

const CORS_HEADERS = [
  'Access-Control-Allow-Origin', 'Access-Control-Allow-Methods', 'Access-Control-Allow-Headers',
  'Access-Control-Allow-Credentials', 'Access-Control-Expose-Headers', 'Access-Control-Max-Age',
];

export const onRequestPost: PagesFunction = async ({ request }) => {
  const body = await readBody(request);
  let url = String(body.url ?? '').trim();
  const testOrigin = String(body.origin ?? '').trim() || 'https://example.com';
  if (!url) return json({ error: 'URL is required' }, 400);
  if (!url.startsWith('http')) url = 'https://' + url;
  try {
    new URL(url);
  } catch {
    return json({ error: 'Could not connect to the URL' }, 400);
  }

  const headers = { Origin: testOrigin, 'User-Agent': 'Mozilla/5.0 CORS Checker' };
  const timeout = () => AbortSignal.timeout(10_000);
  try {
    await fetch(url, { method: 'OPTIONS', headers, signal: timeout() }).catch(() => null);
    const res = await fetch(url, { method: 'GET', headers, signal: timeout() });
    res.body?.cancel();

    const found = Object.fromEntries(CORS_HEADERS.map((h) => [h, res.headers.get(h) ?? '']));
    const allowOrigin = found['Access-Control-Allow-Origin'];
    return json({
      url,
      testOrigin,
      corsEnabled: Boolean(allowOrigin),
      allowsAnyOrigin: allowOrigin === '*',
      allowsTestOrigin: allowOrigin === testOrigin || allowOrigin === '*',
      headers: found,
      statusCode: res.status,
    });
  } catch (e) {
    const message = String(e);
    if (/timeout|abort/i.test(message)) return json({ error: 'Request timed out' }, 400);
    if (/certificate|ssl|tls/i.test(message)) return json({ error: 'SSL certificate verification failed' }, 400);
    return json({ error: 'Could not connect to the URL' }, 400);
  }
};
