// GET /api/ip-lookup/[?ip=1.2.3.4]
//
// Port of ip_lookup_api in formatter/views.py, same response shape. The visitor's own IP is
// answered from Cloudflare's request.cf data (no third party). Any other IP is looked up on
// ip-api.com like before; its free tier is licensed for non-commercial use only.
import { json } from '../../../server/supabase';

type Cf = Record<string, any> | undefined;

const countryName = (code?: string) => {
  if (!code) return '';
  try {
    return new Intl.DisplayNames(['en'], { type: 'region' }).of(code) ?? code;
  } catch {
    return code;
  }
};

function fromCloudflare(ip: string, cf: Cf) {
  const org = cf?.asOrganization ?? '';
  return {
    success: true,
    ip,
    country: countryName(cf?.country),
    countryCode: cf?.country ?? '',
    region: cf?.regionCode ?? '',
    regionName: cf?.region ?? '',
    city: cf?.city ?? '',
    zip: cf?.postalCode ?? '',
    lat: cf?.latitude ? Number(cf.latitude) : null,
    lon: cf?.longitude ? Number(cf.longitude) : null,
    timezone: cf?.timezone ?? '',
    isp: org,
    org,
    as: cf?.asn ? `AS${cf.asn} ${org}`.trim() : '',
  };
}

async function fromIpApi(ip: string) {
  const fields = 'status,message,country,countryCode,region,regionName,city,zip,lat,lon,timezone,isp,org,as,query';
  const res = await fetch(`http://ip-api.com/json/${encodeURIComponent(ip)}?fields=${fields}`);
  if (!res.ok) return json({ success: false, error: 'External API unavailable' }, 502);
  const d = (await res.json()) as Record<string, any>;
  if (d.status !== 'success') return json({ success: false, error: d.message ?? 'Lookup failed' }, 400);
  return json({
    success: true, ip: d.query, country: d.country, countryCode: d.countryCode, region: d.region,
    regionName: d.regionName, city: d.city, zip: d.zip, lat: d.lat, lon: d.lon, timezone: d.timezone,
    isp: d.isp, org: d.org, as: d.as,
  });
}

export const onRequestGet: PagesFunction = async ({ request }) => {
  const own = request.headers.get('CF-Connecting-IP') ?? '';
  const asked = (new URL(request.url).searchParams.get('ip') ?? '').trim();
  const ip = asked || own;
  if (!ip) return json({ success: false, error: 'No IP address provided' }, 400);
  if (ip === own) return json(fromCloudflare(ip, (request as any).cf));
  try {
    return await fromIpApi(ip);
  } catch (e) {
    return json({ success: false, error: String(e) }, 500);
  }
};
