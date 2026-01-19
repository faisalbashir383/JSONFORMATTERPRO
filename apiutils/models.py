from django.db import models
import uuid
from django.utils import timezone
from datetime import timedelta


class WebhookEndpoint(models.Model):
    """Represents a unique webhook URL that captures incoming requests."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    session_key = models.CharField(max_length=64, db_index=True)

    
    class Meta:
        ordering = ['-created_at']
    
    def save(self, *args, **kwargs):
        if not self.expires_at:
            self.expires_at = timezone.now() + timedelta(hours=24)
        super().save(*args, **kwargs)
    
    @property
    def is_expired(self):
        return timezone.now() > self.expires_at
    
    def __str__(self):
        return f"Webhook {self.id}"


class CapturedRequest(models.Model):
    """Stores an individual HTTP request captured by a webhook endpoint."""
    endpoint = models.ForeignKey(
        WebhookEndpoint, 
        on_delete=models.CASCADE, 
        related_name='requests'
    )
    method = models.CharField(max_length=10)
    headers = models.JSONField(default=dict)
    body = models.TextField(blank=True)
    content_type = models.CharField(max_length=100, blank=True)
    query_params = models.JSONField(default=dict)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    received_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-received_at']
    
    def __str__(self):
        return f"{self.method} @ {self.received_at}"
