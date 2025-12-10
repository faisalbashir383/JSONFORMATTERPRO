"""
Visitor tracking middleware for JSON Formatter Pro
Captures IP address, geolocation, device info, and tracks page views
"""

import requests
from django.utils.deprecation import MiddlewareMixin
from django.contrib.sessions.middleware import SessionMiddleware
from django.http import HttpResponsePermanentRedirect, HttpResponseRedirect
from user_agents import parse
from formatter.models import VisitorLog, PageView


class WWWRedirectMiddleware(MiddlewareMixin):
    """
    Middleware to redirect www to non-www version
    Ensures canonical URL for SEO
    """
    
    def process_request(self, request):
        """Redirect www to non-www"""
        host = request.get_host()
        
        # Check if the host starts with www.
        if host.startswith('www.'):
            # Remove www. prefix
            new_host = host[4:]
            # Build new URL
            new_url = f"{request.scheme}://{new_host}{request.get_full_path()}"
            # Return permanent redirect (301)
            return HttpResponsePermanentRedirect(new_url)
        
        return None


class RedirectMiddleware(MiddlewareMixin):
    """
    Middleware to handle URL redirects from the Redirect model
    Supports 301 (permanent) and 302 (temporary) redirects
    """
    
    def process_request(self, request):
        """Check if the current path matches any active redirect"""
        from .models import Redirect
        
        path = request.path
        
        try:
            redirect = Redirect.objects.get(old_path=path, is_active=True)
            
            # Increment hit count for analytics
            redirect.increment_hit_count()
            
            # Return appropriate redirect response
            if redirect.redirect_type == 301:
                return HttpResponsePermanentRedirect(redirect.new_path)
            else:
                return HttpResponseRedirect(redirect.new_path)
                
        except Redirect.DoesNotExist:
            pass
        
        return None


class VisitorTrackingMiddleware(MiddlewareMixin):
    """
    Middleware to track visitors and page views
    Captures IP, geolocation, device info, and logs all page views
    """
    
    # Bot user agents to exclude
    BOT_USER_AGENTS = [
        'bot', 'crawler', 'spider', 'scraper', 'headless',
        'googlebot', 'bingbot', 'slurp', 'duckduckbot', 'baiduspider'
    ]
    
    def process_request(self, request):
        """Process incoming request to track visitor"""
        
        # Skip tracking for admin, static files, and media
        if request.path.startswith(('/admin/', '/static/', '/media/')):
            return None
        
        # Get IP address
        ip_address = self.get_client_ip(request)
        if not ip_address:
            return None
        
        # Get or create session
        if not request.session.session_key:
            request.session.create()
        session_key = request.session.session_key
        
        # Parse user agent
        user_agent_string = request.META.get('HTTP_USER_AGENT', '')
        user_agent = parse(user_agent_string)
        
        # Check if bot
        is_bot = self.is_bot(user_agent_string)
        
        # Get or create visitor log
        visitor_log, created = VisitorLog.objects.get_or_create(
            ip_address=ip_address,
            defaults={
                'session_key': session_key,
                'user_agent': user_agent_string,
                'browser': user_agent.browser.family,
                'browser_version': user_agent.browser.version_string,
                'device_type': self.get_device_type(user_agent),
                'os': user_agent.os.family,
                'os_version': user_agent.os.version_string,
                'is_bot': is_bot,
                'is_mobile': user_agent.is_mobile,
                'referrer': request.META.get('HTTP_REFERER'),
                'landing_page': request.path,
            }
        )
        
        # Fetch geolocation data if not already set
        if created and not visitor_log.country:
            self.update_geolocation(visitor_log, ip_address)
        
        # Update visitor log if not created
        if not created:
            visitor_log.increment_visit()
            visitor_log.last_visit = timezone.now()
            visitor_log.save(update_fields=['last_visit'])
        
        # Create page view record
        PageView.objects.create(
            visitor=visitor_log,
            url=request.path,
            page_title=self.get_page_title(request),
            method=request.method,
            ip_address=ip_address,
            user_agent=user_agent_string,
            referrer=request.META.get('HTTP_REFERER'),
            session_key=session_key,
            country_code=visitor_log.country_code,
            device_type=visitor_log.device_type,
        )
        
        # Increment total page views
        visitor_log.total_page_views += 1
        visitor_log.save(update_fields=['total_page_views'])
        
        # Attach visitor to request for later use
        request.visitor = visitor_log
        
        return None
    
    def get_client_ip(self, request):
        """
        Get client's real IP address
        Handles proxies and load balancers
        """
        # Try various headers used by proxies
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            # X-Forwarded-For can contain multiple IPs, take the first one
            ip = x_forwarded_for.split(',')[0].strip()
        else:
            # Try other common headers
            ip = (
                request.META.get('HTTP_X_REAL_IP') or
                request.META.get('HTTP_CF_CONNECTING_IP') or  # Cloudflare
                request.META.get('REMOTE_ADDR')
            )
        return ip
    
    def get_device_type(self, user_agent):
        """Determine device type from user agent"""
        if user_agent.is_mobile:
            return 'Mobile'
        elif user_agent.is_tablet:
            return 'Tablet'
        elif user_agent.is_pc:
            return 'Desktop'
        else:
            return 'Unknown'
    
    def is_bot(self, user_agent_string):
        """Check if user agent is a bot"""
        user_agent_lower = user_agent_string.lower()
        return any(bot in user_agent_lower for bot in self.BOT_USER_AGENTS)
    
    def get_page_title(self, request):
        """Extract page title from path"""
        path = request.path.strip('/')
        if not path:
            return 'Homepage'
        elif path.startswith('blog/'):
            return 'Blog'
        elif path.startswith('base64/'):
            return 'Base64 Encoder'
        else:
            return path.replace('/', ' - ').title()
    
    def update_geolocation(self, visitor_log, ip_address):
        """
        Get geolocation data from IP address using ip-api.com (free)
        Rate limit: 45 requests per minute
        """
        try:
            # Skip localhost/private IPs
            if ip_address in ['127.0.0.1', '::1'] or ip_address.startswith('192.168.'):
                return
            
            # Call free geolocation API
            response = requests.get(
                f'http://ip-api.com/json/{ip_address}',
                timeout=2
            )
            
            if response.status_code == 200:
                data = response.json()
                
                if data.get('status') == 'success':
                    visitor_log.country = data.get('country')
                    visitor_log.country_code = data.get('countryCode')
                    visitor_log.city = data.get('city')
                    visitor_log.region = data.get('regionName')
                    visitor_log.latitude = data.get('lat')
                    visitor_log.longitude = data.get('lon')
                    visitor_log.save()
        except Exception as e:
            # Silently fail - don't break the request
            print(f"Geolocation error for {ip_address}: {e}")


from django.utils import timezone
