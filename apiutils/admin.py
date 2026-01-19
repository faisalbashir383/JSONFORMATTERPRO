from django.contrib import admin
from .models import WebhookEndpoint, CapturedRequest


@admin.register(WebhookEndpoint)
class WebhookEndpointAdmin(admin.ModelAdmin):
    list_display = ['id', 'created_at', 'expires_at', 'is_expired', 'request_count']
    list_filter = ['created_at']
    search_fields = ['id', 'session_key']
    readonly_fields = ['id', 'created_at']
    
    def request_count(self, obj):
        return obj.requests.count()
    request_count.short_description = 'Requests'


@admin.register(CapturedRequest)
class CapturedRequestAdmin(admin.ModelAdmin):
    list_display = ['id', 'endpoint', 'method', 'content_type', 'ip_address', 'received_at']
    list_filter = ['method', 'received_at']
    search_fields = ['endpoint__id', 'ip_address']
    readonly_fields = ['received_at']
