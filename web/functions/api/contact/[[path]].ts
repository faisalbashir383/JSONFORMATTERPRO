// POST /api/contact/  { name, email, subject, message }
//
// Saves a contact form message to formatter_contactmessage, with the same validation as
// contact_page in formatter/views.py. `website` is a hidden honeypot field: people never
// fill it in, simple bots do, so those requests are accepted but not stored.
import { assertConfigured, clientIp, insert, isEmail, json, readBody, type Env } from '../../../server/supabase';

const SUBJECTS = ['general', 'support', 'feedback', 'bug', 'feature', 'other'];

export const onRequestPost: PagesFunction<Env> = async ({ request, env }) => {
  const notConfigured = assertConfigured(env);
  if (notConfigured) return notConfigured;

  const body = await readBody(request);
  const field = (k: string) => String(body[k] ?? '').trim();
  const name = field('name'), email = field('email'), subject = field('subject'), message = field('message');

  const errors: string[] = [];
  if (!name) errors.push('Name is required.');
  else if (name.length > 200) errors.push('Name is too long.');
  if (!email) errors.push('Email is required.');
  else if (!isEmail(email) || email.length > 254) errors.push('Please enter a valid email address.');
  if (!SUBJECTS.includes(subject)) errors.push('Subject is required.');
  if (!message) errors.push('Message is required.');
  else if (message.length > 10_000) errors.push('Message is too long (10,000 characters max).');
  if (errors.length) return json({ success: false, errors }, 400);

  const thanks = { success: true, message: "Thank you for your message! We'll get back to you soon." };
  if (field('website')) return json(thanks);

  try {
    await insert(env, 'formatter_contactmessage', {
      name, email, subject, message,
      ip_address: clientIp(request),
      user_agent: request.headers.get('User-Agent') ?? '',
      created_at: new Date().toISOString(),
      is_read: false,
      is_replied: false,
      notes: '',
    });
  } catch (e) {
    console.error(e);
    return json({ success: false, errors: ['An error occurred. Please try again.'] }, 500);
  }
  return json(thanks);
};
