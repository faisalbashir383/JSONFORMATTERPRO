// POST /api/dns-lookup/  { "domain": "example.com" }
//
// Port of dns_lookup_api in formatter/views.py, with the same response shape. Records come
// from Cloudflare's DNS-over-HTTPS JSON API; the first three A records get geolocation
// from ip-api.com, as before.

const DOH = 'https://cloudflare-dns.com/dns-query';
const TYPES = { A: 1, NS: 2, CNAME: 5, SOA: 6, PTR: 12, MX: 15, TXT: 16, AAAA: 28 } as const;
type RecordType = keyof typeof TYPES;

const json = (body: unknown, status = 200) =>
  new Response(JSON.stringify(body), { status, headers: { 'Content-Type': 'application/json' } });

const trimDot = (s: string) => s.replace(/\.$/, '');

/** Answers of one type only (an A query can also return the CNAME chain). */
async function resolve(name: string, type: RecordType): Promise<string[]> {
  try {
    const res = await fetch(`${DOH}?name=${encodeURIComponent(name)}&type=${type}`, {
      headers: { Accept: 'application/dns-json' },
    });
    if (!res.ok) return [];
    const body = (await res.json()) as { Answer?: { type: number; data: string }[] };
    return (body.Answer ?? []).filter((a) => a.type === TYPES[type]).map((a) => a.data);
  } catch {
    return [];
  }
}

async function geolocate(ip: string) {
  try {
    const res = await fetch(
      `http://ip-api.com/json/${ip}?fields=status,country,countryCode,region,regionName,city,zip,lat,lon,timezone,isp,org,as`,
    );
    const g = (await res.json()) as Record<string, any>;
    if (g.status !== 'success') return null;
    return {
      ip, country: g.country ?? '', countryCode: g.countryCode ?? '', region: g.regionName ?? '',
      city: g.city ?? '', zip: g.zip ?? '', lat: g.lat, lon: g.lon, timezone: g.timezone ?? '',
      isp: g.isp ?? '', org: g.org ?? '', as: g.as ?? '',
    };
  } catch {
    return { ip, error: 'Could not fetch location' };
  }
}

export const onRequestPost: PagesFunction = async ({ request }) => {
  let domain = '';
  try {
    domain = String(((await request.json()) as { domain?: string }).domain ?? '').trim();
  } catch {
    // fall through to the "required" error
  }
  if (!domain) return json({ error: 'Domain is required' }, 400);
  domain = domain.replace(/^https?:\/\//, '').split('/')[0];

  const [a, aaaa, mx, txt, ns, soa, cname] = await Promise.all(
    (['A', 'AAAA', 'MX', 'TXT', 'NS', 'SOA', 'CNAME'] as RecordType[]).map((t) => resolve(domain, t)),
  );

  const records: Record<string, unknown> = {
    A: a,
    AAAA: aaaa,
    MX: mx.map((d) => {
      const [priority, host] = d.split(/\s+/);
      return { priority: Number(priority), host: trimDot(host ?? '') };
    }),
    TXT: txt.map((d) => d.replace(/^"|"$/g, '')),
    NS: ns.map(trimDot),
    SOA: null,
    CNAME: cname.map(trimDot),
    PTR: [],
  };
  if (soa[0]) {
    const [mname, rname, serial, refresh, retry, expire, minimum] = soa[0].split(/\s+/);
    records.SOA = {
      mname: trimDot(mname), rname: trimDot(rname), serial: Number(serial), refresh: Number(refresh),
      retry: Number(retry), expire: Number(expire), minimum: Number(minimum),
    };
  }
  if (a[0]) {
    const reverse = a[0].split('.').reverse().join('.') + '.in-addr.arpa';
    records.PTR = (await resolve(reverse, 'PTR')).map(trimDot);
  }

  const ipDetails = (await Promise.all(a.slice(0, 3).map(geolocate))).filter(Boolean);
  return json({ domain, records, ipDetails });
};
