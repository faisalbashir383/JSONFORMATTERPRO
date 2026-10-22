// Shared bits for the Webhook Tester functions (port of apiutils/views.py).
export const ENDPOINTS = 'apiutils_webhookendpoint';
export const REQUESTS = 'apiutils_capturedrequest';
export const UUID_RE = /^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/;
export const LIFETIME_MS = 24 * 3600 * 1000;
export const MAX_BODY_BYTES = 256 * 1024;

const COOKIE = 'wh_sid';

/** Browser session id (Django used its session); endpoints belong to the session that made them. */
export function session(request: Request): { id: string; isNew: boolean } {
  const m = (request.headers.get('Cookie') ?? '').match(new RegExp(`(?:^|;\\s*)${COOKIE}=([\\w-]{20,64})`));
  return m ? { id: m[1], isNew: false } : { id: crypto.randomUUID(), isNew: true };
}

export const sessionCookie = (id: string) => `${COOKIE}=${id}; Path=/; Max-Age=2592000; HttpOnly; Secure; SameSite=Lax`;

export const hookUrl = (request: Request, id: string) => `${new URL(request.url).origin}/hook/${id}/`;

export const isExpired = (ep: { expires_at: string }) => Date.parse(ep.expires_at) < Date.now();
