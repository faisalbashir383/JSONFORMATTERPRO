// POST /api/ai/generate-json/  { prompt, mode? }
//
// Port of ai_generate_json in formatter/views.py (OpenRouter). Default mode returns
// { success, json } with validated, pretty-printed JSON, as before. mode: "explain" returns
// { success, content } with plain text; the Log Analyzer uses it to explain error logs
// (the JSON-only endpoint rejected every explanation, so that feature never worked).
//
// Needs OPENROUTER_API_KEY (encrypted Cloudflare variable). OPENROUTER_MODEL overrides the models:
// a comma-separated list, tried in order by OpenRouter (free models get rate-limited or retired,
// so the default is a chain of free ones that returned clean JSON when tested).
import { json, readBody } from '../../../../server/supabase';

interface Env { OPENROUTER_API_KEY?: string; OPENROUTER_MODEL?: string }

const DEFAULT_MODELS = 'nvidia/nemotron-3.5-lightning:free,poolside/laguna-s-2.1:free,google/gemma-4-31b-it:free';
const MAX_PROMPT = 8_000;

const JSON_SYSTEM = `You are a JSON generator. Generate ONLY valid JSON based on the user's request.

Rules:
1. Return ONLY valid JSON - no markdown, no code blocks, no explanations
2. Generate realistic, varied data for each record
3. If user asks for multiple records, return an array
4. Include appropriate fields based on the entity type
5. For names, use realistic examples (not "Name 1", "Name 2")
6. For icd codes, use realistic format (like ICD-10 codes, product SKUs, etc.)

Examples:
- "5 biscuits" → array of 5 biscuit objects with name, brand, flavor, etc.
- "100 users" → array of 100 user objects with name, email, age, etc.
- "10 countries" → array of 10 countries with name, capital, population, etc.`;

const EXPLAIN_SYSTEM = 'You are a senior engineer helping a developer read their logs. Explain clearly and concisely ' +
  'what is going wrong, the likely causes and concrete steps to fix it. Use short paragraphs or a short list. Plain text only, no markdown headings.';

export const onRequestPost: PagesFunction<Env> = async ({ request, env }) => {
  const body = await readBody(request);
  const prompt = String(body.prompt ?? '').trim();
  const explain = body.mode === 'explain';
  if (!prompt) return json({ success: false, error: 'No prompt provided. Please describe what JSON you need.' }, 400);
  if (prompt.length > MAX_PROMPT) return json({ success: false, error: `Prompt is too long (${MAX_PROMPT} characters max).` }, 400);
  if (!env.OPENROUTER_API_KEY) return json({ success: false, error: 'OpenRouter API key not configured.' }, 500);

  let res: Response;
  try {
    res = await fetch('https://openrouter.ai/api/v1/chat/completions', {
      method: 'POST',
      headers: {
        Authorization: `Bearer ${env.OPENROUTER_API_KEY}`,
        'Content-Type': 'application/json',
        'HTTP-Referer': 'https://jsonformatterspro.com',
        'X-Title': 'JSON Formatter Pro',
      },
      body: JSON.stringify({
        models: (env.OPENROUTER_MODEL || DEFAULT_MODELS).split(',').map((m) => m.trim()).filter(Boolean),
        messages: [
          { role: 'system', content: explain ? EXPLAIN_SYSTEM : JSON_SYSTEM },
          { role: 'user', content: prompt },
        ],
        temperature: explain ? 0.3 : 0.7,
        max_tokens: explain ? 1500 : 8192,
      }),
      signal: AbortSignal.timeout(60_000),
    });
  } catch (e) {
    return /timeout|abort/i.test(String(e))
      ? json({ success: false, error: 'AI request timed out. Please try again.' }, 504)
      : json({ success: false, error: `An error occurred: ${e}` }, 500);
  }
  if (!res.ok) {
    console.error('OpenRouter', res.status, await res.text());
    return json({ success: false, error: `AI API error: ${res.status}` }, 500);
  }

  const data = (await res.json()) as { choices?: { message?: { content?: string } }[] };
  let text = (data.choices?.[0]?.message?.content ?? '').trim();
  if (!text) return json({ success: false, error: 'The AI did not return an answer. Please try again.' }, 502);
  if (explain) return json({ success: true, content: text });

  // Same cleanup as the Django view: strip ``` fences, then insist on valid JSON.
  text = text.replace(/^```(?:json)?/, '').replace(/```$/, '').trim();
  try {
    return json({ success: true, json: JSON.stringify(JSON.parse(text), null, 2) });
  } catch (e) {
    return json({ success: false, error: `AI returned invalid JSON: ${(e as Error).message}`, raw: text.slice(0, 500) }, 500);
  }
};
