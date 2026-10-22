// POST /api/typing-test/submit/       save a score (one best score per username + level)
// GET  /api/typing-test/leaderboard/  ?level=&period=all|daily|weekly&duration=&limit=&page=
//
// Port of submit_typing_score and get_typing_leaderboard in formatter/views.py, with the same
// responses. Django used its session to find "your best score"; this uses a random id in the
// tt_sid cookie, stored in the session_key column.
import { assertConfigured, clientIp, count, insert, json, select, update, type Env } from '../../../server/supabase';

const TABLE = 'formatter_typingscore';
const COOKIE = 'tt_sid';

function sessionId(request: Request): { id: string; isNew: boolean } {
  const match = (request.headers.get('Cookie') ?? '').match(new RegExp(`(?:^|;\\s*)${COOKIE}=([\\w-]{20,64})`));
  return match ? { id: match[1], isNew: false } : { id: crypto.randomUUID(), isNew: true };
}

const sessionCookie = (id: string) =>
  `${COOKIE}=${id}; Path=/; Max-Age=31536000; HttpOnly; Secure; SameSite=Lax`;

/** Rank among verified scores: 1 + how many are strictly faster (TypingScore.get_rank). */
const rankOf = async (env: Env, wpm: number, level?: string) =>
  1 + await count(env, TABLE, `is_verified=eq.true&wpm=gt.${wpm}${level ? `&level=eq.${encodeURIComponent(level)}` : ''}`);

async function submit(request: Request, env: Env) {
  let body: Record<string, unknown>;
  try {
    body = (await request.json()) as Record<string, unknown>;
  } catch {
    return json({ success: false, error: 'Invalid request body' }, 400);
  }
  const int = (k: string, fallback: number) => {
    const n = parseInt(String(body[k] ?? fallback), 10);
    return Number.isNaN(n) ? NaN : n;
  };
  const username = String(body.username ?? 'Anonymous').trim().slice(0, 50) || 'Anonymous';
  const level = String(body.level ?? 'medium').trim().slice(0, 20) || 'medium';
  const wpm = int('wpm', 0);
  const accuracy = Number(body.accuracy ?? 0);
  const duration = int('duration', 60);
  const totals = {
    total_characters: int('total_characters', 0),
    correct_characters: int('correct_characters', 0),
    errors: int('errors', 0),
  };
  if ([wpm, duration, ...Object.values(totals)].some(Number.isNaN)) {
    return json({ success: false, error: 'Invalid number in request' }, 400);
  }
  if (wpm < 0 || wpm > 3000) return json({ success: false, error: 'Invalid WPM' }, 400);
  if (!(accuracy >= 0 && accuracy <= 100)) return json({ success: false, error: 'Invalid accuracy' }, 400);

  const session = sessionId(request);
  const now = new Date().toISOString();
  const [existing] = await select(env, TABLE,
    `username=eq.${encodeURIComponent(username)}&level=eq.${encodeURIComponent(level)}&select=id,wpm&limit=1`);

  let scoreId: number, bestWpm: number, message: string, isHighScore: boolean;
  if (existing && wpm <= existing.wpm) {
    scoreId = existing.id;
    bestWpm = existing.wpm;
    isHighScore = false;
    message = `Score recorded, but your personal best of ${existing.wpm} WPM remains!`;
  } else {
    const values = { wpm, accuracy, duration, ...totals, ip_address: clientIp(request), session_key: session.id, created_at: now };
    if (existing) {
      await update(env, TABLE, `id=eq.${existing.id}`, values);
      scoreId = existing.id;
    } else {
      scoreId = (await insert(env, TABLE, { ...values, username, level, is_verified: true })).id;
    }
    bestWpm = wpm;
    isHighScore = true;
    const rank = await rankOf(env, wpm, level);
    message = existing
      ? `New High Score! You ranked #${rank} in ${level} mode.`
      : `Score saved! You ranked #${rank} in ${level} mode.`;
  }

  const [rank, globalRank] = await Promise.all([rankOf(env, bestWpm, level), rankOf(env, bestWpm)]);
  return json(
    { success: true, score_id: scoreId, rank, global_rank: globalRank, message, is_high_score: isHighScore },
    200,
    session.isNew ? { 'Set-Cookie': sessionCookie(session.id) } : {},
  );
}

async function leaderboard(request: Request, env: Env) {
  const params = new URL(request.url).searchParams;
  const level = params.get('level') ?? 'all';
  const period = params.get('period') ?? 'all';
  const duration = params.get('duration');
  const limit = Math.min(parseInt(params.get('limit') ?? '20', 10) || 20, 100);
  const page = Math.max(parseInt(params.get('page') ?? '1', 10) || 1, 1);

  const filters = ['is_verified=eq.true'];
  if (level && level !== 'all') filters.push(`level=eq.${encodeURIComponent(level)}`);
  const now = new Date();
  if (period === 'daily' || period === 'weekly') {
    const start = new Date(Date.UTC(now.getUTCFullYear(), now.getUTCMonth(), now.getUTCDate()));
    if (period === 'weekly') start.setUTCDate(start.getUTCDate() - ((start.getUTCDay() + 6) % 7)); // back to Monday
    filters.push(`created_at=gte.${start.toISOString()}`);
  }
  const durationInt = duration ? parseInt(duration, 10) : NaN;
  if (!Number.isNaN(durationInt)) filters.push(`duration=eq.${durationInt}`);
  const where = filters.join('&');

  const offset = (page - 1) * limit;
  const [total, rows] = await Promise.all([
    count(env, TABLE, where),
    select(env, TABLE, `${where}&select=username,wpm,accuracy,level,duration,created_at&order=wpm.desc,accuracy.desc&limit=${limit}&offset=${offset}`),
  ]);

  let userBest = null, userRank = null;
  const session = sessionId(request);
  if (!session.isNew) {
    const own = ['is_verified=eq.true', `session_key=eq.${session.id}`, ...filters.filter((f) => f.startsWith('level=') || f.startsWith('duration='))];
    const [best] = await select(env, TABLE, `${own.join('&')}&select=wpm,accuracy,level,duration&order=wpm.desc&limit=1`);
    if (best) {
      userBest = { wpm: best.wpm, accuracy: Number(best.accuracy), level: best.level, duration: best.duration };
      userRank = 1 + await count(env, TABLE, `${where}&wpm=gt.${best.wpm}`);
    }
  }

  return json({
    success: true,
    leaderboard: rows.map((s, i) => ({
      rank: offset + i + 1, username: s.username, wpm: s.wpm, accuracy: Number(s.accuracy),
      level: s.level, duration: s.duration, date: String(s.created_at).slice(0, 10),
    })),
    user_best: userBest,
    user_rank: userRank,
    total_scores: total,
    page,
    total_pages: Math.max(1, Math.ceil(total / limit)),
    limit,
    filters: { level, period, duration },
  });
}

export const onRequest: PagesFunction<Env> = async ({ request, env, params }) => {
  const notConfigured = assertConfigured(env);
  if (notConfigured) return notConfigured;
  const action = ([] as string[]).concat(params.path ?? []).filter(Boolean)[0];
  try {
    if (action === 'submit' && request.method === 'POST') return await submit(request, env);
    if (action === 'leaderboard' && request.method === 'GET') return await leaderboard(request, env);
  } catch (e) {
    console.error(e);
    return json({ success: false, error: 'Something went wrong. Please try again.' }, 500);
  }
  return json({ success: false, error: 'Not found' }, 404);
};
