// Nunjucks set up to render the translated Django templates (src/templates/*.njk) with
// the same output Django produced: Django's HTML escaping, Python-style True/False/None,
// and Django's filters (date, truncatewords, escapejs, default, ...).
import nunjucks from 'nunjucks';

const { SafeString } = nunjucks.runtime;
type Value = unknown;

// Django's django.utils.html.escape (nunjucks uses &#39; for ', Django uses &#x27;).
const ESCAPES: Record<string, string> = { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#x27;' };
(nunjucks.lib as unknown as { escape: (s: string) => string }).escape = (s: string) =>
  s.replace(/[&<>"']/g, (c) => ESCAPES[c]);

const isSafe = (v: Value) => v instanceof SafeString;
const str = (v: Value) => (v === null || v === undefined ? '' : String(v));
const keepSafe = (input: Value, output: string) => (isSafe(input) ? new SafeString(output) : output);

const pyTruthy = (v: Value) => {
  if (Array.isArray(v)) return v.length > 0;
  if (isSafe(v)) return String(v).length > 0;
  return Boolean(v);
};

// ---------------------------------------------------------------- date

const MONTHS = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August',
  'September', 'October', 'November', 'December'];
const pad = (n: number, width = 2) => String(n).padStart(width, '0');

/** Parse a Postgres/ISO timestamp, keeping microseconds, and convert it to UTC (TIME_ZONE = 'UTC'). */
function parseTimestamp(value: string) {
  const m = value.match(/^(\d{4})-(\d\d)-(\d\d)[T ](\d\d):(\d\d):(\d\d)(?:\.(\d{1,6}))?(Z|[+-]\d\d(?::?\d\d)?)?$/);
  if (!m) return null;
  const [, y, mo, d, h, mi, s, frac = '', tz = 'Z'] = m;
  let offsetMin = 0;
  if (tz !== 'Z') {
    const sign = tz[0] === '-' ? -1 : 1;
    const digits = tz.slice(1).replace(':', '');
    offsetMin = sign * (Number(digits.slice(0, 2)) * 60 + Number(digits.slice(2, 4) || 0));
  }
  const utc = new Date(Date.UTC(+y, +mo - 1, +d, +h, +mi, +s) - offsetMin * 60_000);
  return { date: utc, micro: Number(frac.padEnd(6, '0')) };
}

function djangoDate(value: Value, format = 'N j, Y') {
  if (!value) return '';
  const t = parseTimestamp(String(value));
  if (!t) return '';
  const { date: dt, micro } = t;
  const parts: Record<string, () => string> = {
    Y: () => String(dt.getUTCFullYear()),
    m: () => pad(dt.getUTCMonth() + 1),
    n: () => String(dt.getUTCMonth() + 1),
    F: () => MONTHS[dt.getUTCMonth()],
    N: () => MONTHS[dt.getUTCMonth()].slice(0, 3) + '.',
    d: () => pad(dt.getUTCDate()),
    j: () => String(dt.getUTCDate()),
    H: () => pad(dt.getUTCHours()),
    i: () => pad(dt.getUTCMinutes()),
    s: () => pad(dt.getUTCSeconds()),
    c: () => {
      const base = `${dt.getUTCFullYear()}-${pad(dt.getUTCMonth() + 1)}-${pad(dt.getUTCDate())}T` +
        `${pad(dt.getUTCHours())}:${pad(dt.getUTCMinutes())}:${pad(dt.getUTCSeconds())}`;
      return `${base}${micro ? '.' + pad(micro, 6) : ''}+00:00`;
    },
  };
  return [...format].map((ch) => (parts[ch] ? parts[ch]() : ch)).join('');
}

// ---------------------------------------------------------------- text filters

const JS_ESCAPES: Record<string, string> = {
  '\\': '\\u005C', "'": '\\u0027', '"': '\\u0022', '>': '\\u003E', '<': '\\u003C', '&': '\\u0026',
  '=': '\\u003D', '-': '\\u002D', ';': '\\u003B', '`': '\\u0060', '\u2028': '\\u2028', '\u2029': '\\u2029',
};

function escapejs(value: Value) {
  const out = str(value).replace(/[\\'"<>&=\-;`\u2028\u2029\x00-\x1f]/g, (c) =>
    JS_ESCAPES[c] ?? '\\u' + c.charCodeAt(0).toString(16).toUpperCase().padStart(4, '0'));
  return new SafeString(out);
}

const words = (s: string) => s.split(/\s+/).filter(Boolean);

function truncatewords(value: Value, length: number) {
  const n = Number(length);
  if (n <= 0) return '';
  const w = words(str(value));
  const text = w.length > n ? w.slice(0, n).join(' ') + ' …' : w.join(' ');
  return keepSafe(value, text);
}

function striptags(value: Value) {
  let s = str(value);
  while (s.includes('<') && s.includes('>')) {
    const next = s.replace(/<!--[\s\S]*?-->/g, '').replace(/<\/?[A-Za-z!][^>]*>/g, '');
    if ((next.match(/</g) ?? []).length === (s.match(/</g) ?? []).length) break;
    s = next;
  }
  return s;
}

function urlencode(value: Value) {
  return encodeURIComponent(str(value))
    .replace(/[!'()*]/g, (c) => '%' + c.charCodeAt(0).toString(16).toUpperCase())
    .replace(/%2F/g, '/');
}

/** Python slice syntax, e.g. ":5" or "2:". */
function slice<T>(value: T[] | string, spec: string) {
  const [start, end] = String(spec).split(':').map((x) => (x === '' ? undefined : Number(x)));
  return value.slice(start ?? 0, end);
}

/** Final output step: print values the way Python's str() does. */
function py(value: Value) {
  if (value === true) return 'True';
  if (value === false) return 'False';
  if (value === null) return 'None';
  return value;
}

export function createEnvironment() {
  const env = new nunjucks.Environment(null, { autoescape: true });
  env.addFilter('py', py);
  env.addFilter('pytruth', pyTruthy);
  env.addFilter('date', djangoDate);
  env.addFilter('escapejs', escapejs);
  env.addFilter('truncatewords', truncatewords);
  env.addFilter('striptags', striptags);
  env.addFilter('urlencode', urlencode);
  env.addFilter('slice', slice);
  env.addFilter('wordcount', (v: Value) => words(str(v)).length);
  env.addFilter('default', (v: Value, fallback: Value) => (pyTruthy(v) ? v : fallback));
  env.addFilter('pluralize', (v: Value, suffix = 's') =>
    (Array.isArray(v) ? v.length : Number(v)) === 1 ? '' : suffix);
  return env;
}
