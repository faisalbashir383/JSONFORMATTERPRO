// GET /api/top-domains/?limit=N  Most visited domain-age pages (top_domains_api in
// formatter/views.py), read from formatter_domainpagevisit. Returns an empty list until
// domain-age result pages are tracked again.
import { json, select, type Env } from '../../../server/supabase';

export const onRequestGet: PagesFunction<Env> = async ({ request, env }) => {
  const limit = Math.min(parseInt(new URL(request.url).searchParams.get('limit') ?? '10', 10) || 10, 50);
  if (!env.SUPABASE_URL || !env.SUPABASE_SECRET_KEY) return json({ success: true, domains: [], total: 0 });
  try {
    const rows = await select(env, 'formatter_domainpagevisit',
      `select=domain,visit_count,unique_visitors,last_cached_data&order=visit_count.desc&limit=${limit}`);
    const domains = rows.map((v) => {
      const item: Record<string, unknown> = { domain: v.domain, visitCount: v.visit_count, uniqueVisitors: v.unique_visitors };
      try {
        const cached = JSON.parse(v.last_cached_data || '{}');
        if (cached.age) item.age = cached.age;
        if (cached.registrar) item.registrar = cached.registrar;
      } catch { /* ignore bad cache */ }
      return item;
    });
    return json({ success: true, domains, total: domains.length });
  } catch (e) {
    return json({ success: false, error: String(e) }, 500);
  }
};
