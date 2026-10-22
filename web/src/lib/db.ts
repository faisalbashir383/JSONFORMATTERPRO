// Build-time data access. Pages are generated once per build, so tables are read in full
// (they are small) and cached for the rest of the build.
//
// Sources, in order:
//   SUPABASE_URL + SUPABASE_ANON_KEY  Supabase REST API; Row Level Security limits what is visible
//   DATA_FIXTURE                      path to a JSON file { table: rows[] } for offline builds/tests
// With neither set, the data-driven pages are skipped and the rest of the site still builds.
import { readFileSync } from 'node:fs';

export type Row = Record<string, any>;

const SUPABASE_URL = process.env.SUPABASE_URL?.replace(/\/$/, '');
const SUPABASE_ANON_KEY = process.env.SUPABASE_ANON_KEY;
const DATA_FIXTURE = process.env.DATA_FIXTURE;

export const hasData = Boolean((SUPABASE_URL && SUPABASE_ANON_KEY) || DATA_FIXTURE);

if (!hasData) {
  console.warn('[db] SUPABASE_URL/SUPABASE_ANON_KEY not set: blog, tutorials and careers pages are skipped.');
}

let fixture: Record<string, Row[]> | undefined;
const cache = new Map<string, Promise<Row[]>>();

async function fetchAll(table: string, query: string): Promise<Row[]> {
  const rows: Row[] = [];
  const pageSize = 1000;
  for (let offset = 0; ; offset += pageSize) {
    const res = await fetch(`${SUPABASE_URL}/rest/v1/${table}?select=*&${query}`, {
      headers: {
        apikey: SUPABASE_ANON_KEY!,
        Authorization: `Bearer ${SUPABASE_ANON_KEY}`,
        Range: `${offset}-${offset + pageSize - 1}`,
      },
    });
    if (!res.ok) throw new Error(`[db] ${table}: ${res.status} ${await res.text()}`);
    const page: Row[] = await res.json();
    rows.push(...page);
    if (page.length < pageSize) return rows;
  }
}

/**
 * All visible rows of a table, ordered like the Django model's Meta.ordering.
 * `order` uses PostgREST syntax, e.g. "published_at.desc" or "order.asc,name.asc".
 */
export function table(name: string, order: string): Promise<Row[]> {
  if (!cache.has(name)) {
    cache.set(name, (async () => {
      if (SUPABASE_URL && SUPABASE_ANON_KEY) return fetchAll(name, `order=${order}`);
      if (DATA_FIXTURE) {
        fixture ??= JSON.parse(readFileSync(DATA_FIXTURE, 'utf8'));
        return sortRows(fixture![name] ?? [], order);
      }
      return [];
    })());
  }
  return cache.get(name)!;
}

/** Same ordering rules as PostgREST/Postgres for the fixture source (NULLs first on desc). */
function sortRows(rows: Row[], order: string) {
  const keys = order.split(',').map((k) => {
    const [col, dir = 'asc'] = k.split('.');
    return { col, desc: dir === 'desc' };
  });
  return [...rows].sort((a, b) => {
    for (const { col, desc } of keys) {
      const x = a[col], y = b[col];
      if (x === y) continue;
      if (x === null || x === undefined) return desc ? -1 : 1;
      if (y === null || y === undefined) return desc ? 1 : -1;
      const cmp = x < y ? -1 : 1;
      return desc ? -cmp : cmp;
    }
    return 0;
  });
}
