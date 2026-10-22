// POST /api/ssl-checker/  { domain }
//
// Port of ssl_checker_api in formatter/views.py, same response shape. Pages Functions can't
// read the certificate from a TLS handshake, so:
//   - validity: an HTTPS request to the domain (it fails if the certificate isn't trusted)
//   - details: the newest unexpired, unrevoked certificate for the domain in Certificate
//     Transparency logs (Cert Spotter API). Every publicly trusted certificate must be logged.
// The serial number isn't available this way and is returned as ''. Results are cached for
// 6 hours per domain; set CERTSPOTTER_API_KEY to raise Cert Spotter's 100 lookups/hour limit.
import { json, readBody } from '../../../server/supabase';

interface Env { CERTSPOTTER_API_KEY?: string }
interface Issuance {
  dns_names: string[];
  issuer: { name: string; friendly_name?: string };
  not_before: string;
  not_after: string;
  revoked: boolean;
}

const CACHE_SECONDS = 6 * 3600;

/** "C=GB, O=Sectigo Limited, CN=Sectigo ..." -> { O: 'Sectigo Limited', CN: 'Sectigo ...' } */
function parseDn(dn: string) {
  const out: Record<string, string> = {};
  for (const part of dn.split(/,\s*(?=[A-Za-z.]+=)/)) {
    const i = part.indexOf('=');
    if (i > 0) out[part.slice(0, i).trim()] = part.slice(i + 1).trim();
  }
  return out;
}

const covers = (name: string, domain: string) =>
  name === domain || (name.startsWith('*.') && domain.endsWith(name.slice(1)) && domain.split('.').length === name.split('.').length);

async function lookup(domain: string, env: Env) {
  try {
    const res = await fetch(`https://${domain}/`, { method: 'HEAD', redirect: 'manual', signal: AbortSignal.timeout(10_000) });
    res.body?.cancel();
  } catch (e) {
    const msg = String(e);
    if (/timeout|abort/i.test(msg)) return { domain, valid: false, error: 'Connection timed out' };
    if (/dns|resolve|not found/i.test(msg)) return { domain, valid: false, error: 'Could not resolve domain' };
    // Cloudflare reports untrusted certificates only as an opaque "internal error".
    return { domain, valid: false, error: 'SSL Error: the certificate is not trusted (expired, self-signed, revoked or issued for a different domain), or the site does not support HTTPS.' };
  }

  const headers: Record<string, string> = {};
  if (env.CERTSPOTTER_API_KEY) headers.Authorization = `Bearer ${env.CERTSPOTTER_API_KEY}`;
  const ct = await fetch(
    `https://api.certspotter.com/v1/issuances?domain=${encodeURIComponent(domain)}&match_wildcards=true&expand=dns_names&expand=issuer`,
    { headers, signal: AbortSignal.timeout(15_000) },
  );
  if (!ct.ok) {
    return { domain, valid: true, error: ct.status === 429
      ? 'The certificate is trusted, but the certificate log service is busy. Try again in a few minutes.'
      : 'The certificate is trusted, but its details could not be loaded.' };
  }
  const now = Date.now();
  const current = ((await ct.json()) as Issuance[])
    .filter((c) => !c.revoked && Date.parse(c.not_after) > now && Date.parse(c.not_before) <= now)
    .filter((c) => c.dns_names.some((n) => covers(n, domain)))
    .sort((a, b) => Date.parse(b.not_before) - Date.parse(a.not_before))[0];
  if (!current) return { domain, valid: true, error: 'The certificate is trusted, but it was not found in public certificate logs.' };

  const issuer = parseDn(current.issuer.name);
  const daysRemaining = Math.floor((Date.parse(current.not_after) - now) / 86_400_000);
  return {
    domain,
    valid: true,
    subject: { commonName: current.dns_names.find((n) => covers(n, domain)) ?? domain, organization: '' },
    issuer: { commonName: issuer.CN ?? '', organization: issuer.O ?? current.issuer.friendly_name ?? '' },
    validFrom: current.not_before.replace(/Z$/, ''),
    validTo: current.not_after.replace(/Z$/, ''),
    daysRemaining,
    expired: daysRemaining < 0,
    serialNumber: '',
    version: 3,
    subjectAltNames: current.dns_names,
  };
}

export const onRequestPost: PagesFunction<Env> = async ({ request, env, waitUntil }) => {
  const body = await readBody(request);
  const domain = String(body.domain ?? '').trim().replace(/^https?:\/\//, '').split('/')[0].toLowerCase();
  if (!domain) return json({ error: 'Domain is required' }, 400);
  if (!/^[a-z0-9.-]+\.[a-z]{2,}$/.test(domain)) return json({ domain, valid: false, error: 'Could not resolve domain' });

  const cacheKey = new Request(`https://cache.internal/ssl-checker/${domain}`);
  const cached = await caches.default.match(cacheKey);
  if (cached) return cached;

  try {
    const response = json(await lookup(domain, env), 200, { 'Cache-Control': `max-age=${CACHE_SECONDS}` });
    waitUntil(caches.default.put(cacheKey, response.clone()));
    return response;
  } catch (e) {
    return json({ error: String(e) }, 500);
  }
};
