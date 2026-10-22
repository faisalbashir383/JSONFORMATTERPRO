// POST /api/careers/apply/  { slug, full_name, email, resume_url, ... }
//
// Saves a job application to formatter_jobapplication, with the same validation as
// job_detail in formatter/views.py. `website` is a hidden honeypot field (see contact).
import { assertConfigured, clientIp, insert, isEmail, json, readBody, select, type Env } from '../../../../server/supabase';

const isUrl = (s: string) => /^https?:\/\/\S+$/i.test(s);

export const onRequestPost: PagesFunction<Env> = async ({ request, env }) => {
  const notConfigured = assertConfigured(env);
  if (notConfigured) return notConfigured;

  const body = await readBody(request);
  const field = (k: string, max = 200) => String(body[k] ?? '').trim().slice(0, max);
  const slug = field('slug', 250);
  const app = {
    full_name: field('full_name'),
    email: field('email', 254),
    phone: field('phone', 20),
    cover_letter: String(body.cover_letter ?? '').trim().slice(0, 10_000),
    resume_url: field('resume_url'),
    portfolio_url: field('portfolio_url'),
    linkedin_url: field('linkedin_url'),
    years_of_experience: Math.max(0, parseInt(field('years_of_experience'), 10) || 0),
    current_company: field('current_company'),
    current_role: field('current_role'),
  };

  const errors: string[] = [];
  if (!app.full_name) errors.push('Full name is required.');
  if (!app.email) errors.push('Email is required.');
  else if (!isEmail(app.email)) errors.push('Please enter a valid email address.');
  if (!app.resume_url) errors.push('Resume/CV link is required.');
  else if (!isUrl(app.resume_url)) errors.push('Resume/CV link must be a full URL starting with https://');
  for (const [key, label] of [['portfolio_url', 'Portfolio'], ['linkedin_url', 'LinkedIn']] as const) {
    if (app[key] && !isUrl(app[key])) errors.push(`${label} link must be a full URL starting with https://`);
  }
  if (errors.length) return json({ success: false, errors }, 400);

  const thanks = { success: true, message: "Thank you for applying! We've received your application and will get back to you soon." };
  if (field('website')) return json(thanks);

  try {
    const [job] = await select(env, 'formatter_jobposting', `slug=eq.${encodeURIComponent(slug)}&is_active=eq.true&select=id`);
    if (!job) return json({ success: false, errors: ['This job is no longer open.'] }, 404);
    const now = new Date().toISOString();
    await insert(env, 'formatter_jobapplication', {
      ...app,
      job_id: job.id,
      status: 'pending',
      ip_address: clientIp(request),
      user_agent: request.headers.get('User-Agent') ?? '',
      applied_at: now,
      updated_at: now,
      notes: '',
    });
  } catch (e) {
    console.error(e);
    return json({ success: false, errors: ['An error occurred while submitting your application. Please try again.'] }, 500);
  }
  return json(thanks);
};
