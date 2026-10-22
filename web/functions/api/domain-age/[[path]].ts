// POST /api/domain-age/  { domain }
//
// Port of domain_age_api in formatter/views.py, same response shape. Classic WHOIS needs a raw
// TCP connection to port 43, which Pages Functions don't allow, so this uses RDAP: the JSON
// over HTTPS successor run by every gTLD registry and most ccTLDs. The registry for each TLD
// comes from IANA's bootstrap file. Results are cached for 24 hours, as before.
import { json, readBody } from '../../../server/supabase';

const CACHE_SECONDS = 86_400;
const HEADERS = { Accept: 'application/rdap+json', 'User-Agent': 'JSONFormattersPro-DomainAge/1.0 (+https://jsonformatterspro.com)' };

/** TLD -> RDAP base URL, from https://data.iana.org/rdap/dns.json (cached for a day). */
async function rdapBase(tld: string): Promise<string | undefined> {
  const key = new Request('https://cache.internal/iana-rdap-dns.json');
  let res = await caches.default.match(key);
  if (!res) {
    const fresh = await fetch('https://data.iana.org/rdap/dns.json', { headers: HEADERS, signal: AbortSignal.timeout(10_000) });
    if (!fresh.ok) return undefined;
    res = new Response(await fresh.text(), { headers: { 'Cache-Control': `max-age=${CACHE_SECONDS}` } });
    await caches.default.put(key, res.clone());
  }
  const { services } = (await res.json()) as { services: [string[], string[]][] };
  const urls = services.find(([tlds]) => tlds.includes(tld))?.[1] ?? [];
  return urls.find((u) => u.startsWith('https://')) ?? urls[0];
}

interface RdapEntity { roles?: string[]; vcardArray?: [string, [string, object, string, string][]]; publicIds?: { identifier: string }[] }
interface Rdap {
  ldhName?: string;
  events?: { eventAction: string; eventDate: string }[];
  entities?: RdapEntity[];
  nameservers?: { ldhName?: string }[];
  status?: string[];
  secureDNS?: { delegationSigned?: boolean };
}

const vcardName = (e: RdapEntity) => e.vcardArray?.[1]?.find((p) => p[0] === 'fn')?.[3];

/** Same arithmetic as the Django view: 365-day years, 30-day months. */
function ageFrom(created: Date) {
  const total = Math.floor((Date.now() - created.getTime()) / 86_400_000);
  return { years: Math.floor(total / 365), months: Math.floor((total % 365) / 30), days: (total % 365) % 30 };
}

const iso = (s?: string) => (s ? new Date(s).toISOString().replace(/\.000Z$/, '').replace(/Z$/, '') : null);

async function lookup(domain: string) {
  const base = await rdapBase(domain.split('.').pop()!);
  if (!base) return json({ error: `Unable to fetch WHOIS data: no RDAP service for .${domain.split('.').pop()} domains` }, 400);
  const res = await fetch(`${base.replace(/\/?$/, '/')}domain/${encodeURIComponent(domain)}`, {
    headers: HEADERS,
    signal: AbortSignal.timeout(15_000),
  });
  if (res.status === 404) return json({ error: 'Domain not found or WHOIS data unavailable' }, 404);
  if (!res.ok) return json({ error: `Unable to fetch WHOIS data: registry returned ${res.status}` }, 400);
  const r = (await res.json()) as Rdap;

  const event = (action: string) => r.events?.find((e) => e.eventAction === action)?.eventDate;
  const created = event('registration');
  const updated = event('last changed') ?? event('last update of RDAP database');
  const expiry = event('expiration');
  const registrar = r.entities?.find((e) => e.roles?.includes('registrar'));

  return json({
    domain,
    createdDate: iso(created),
    updatedDate: iso(updated),
    expiryDate: iso(expiry),
    age: created ? ageFrom(new Date(created)) : { years: 0, months: 0, days: 0 },
    daysUntilExpiry: expiry ? Math.floor((Date.parse(expiry) - Date.now()) / 86_400_000) : null,
    registrar: (registrar && vcardName(registrar)) ?? null,
    nameServers: [...new Set((r.nameservers ?? []).map((n) => n.ldhName?.toLowerCase().replace(/\.$/, '')).filter(Boolean))],
    status: r.status ?? [],
    dnssec: r.secureDNS?.delegationSigned ? 'signedDelegation' : 'Unsigned',
  }, 200, { 'Cache-Control': `max-age=${CACHE_SECONDS}` });
}

export const onRequestPost: PagesFunction = async ({ request, waitUntil }) => {
  const body = await readBody(request);
  const domain = String(body.domain ?? '').trim().replace(/^https?:\/\//, '').replace(/^www\./, '')
    .split('/')[0].split('?')[0].toLowerCase();
  if (!domain) return json({ error: 'Domain is required' }, 400);
  if (!/^[a-z0-9.-]+\.[a-z0-9-]{2,}$/.test(domain)) return json({ error: 'Domain not found or WHOIS data unavailable' }, 404);

  const cacheKey = new Request(`https://cache.internal/domain-age/${domain}`);
  const cached = await caches.default.match(cacheKey);
  if (cached) return cached;

  try {
    const response = await lookup(domain);
    if (response.ok) waitUntil(caches.default.put(cacheKey, response.clone()));
    return response;
  } catch (e) {
    const msg = String(e);
    return json({ error: /timeout|abort/i.test(msg) ? 'Unable to fetch WHOIS data: the registry timed out' : msg }, 500);
  }
};
