// GET /api/my-ip/  The visitor's public IP (get_client_ip_api in formatter/views.py).
import { json } from '../../../server/supabase';

export const onRequestGet: PagesFunction = async ({ request }) =>
  json({ success: true, ip: request.headers.get('CF-Connecting-IP'), message: 'Your public IP address' });
