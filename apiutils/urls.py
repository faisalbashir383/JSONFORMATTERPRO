from django.urls import path
from . import views

app_name = 'apiutils'

urlpatterns = [
    # Page view
    path('webhook-tester/', views.webhook_tester_page, name='webhook_tester'),
    
    # API endpoints
    path('api/webhook/create/', views.create_endpoint, name='create_endpoint'),
    path('api/webhook/list/', views.list_endpoints, name='list_endpoints'),
    path('api/webhook/<uuid:endpoint_id>/requests/', views.get_requests, name='get_requests'),
    path('api/webhook/<uuid:endpoint_id>/clear/', views.clear_requests, name='clear_requests'),
    path('api/webhook/<uuid:endpoint_id>/delete/', views.delete_endpoint, name='delete_endpoint'),
    path('api/webhook/send/', views.send_request, name='send_request'),
    
    # Webhook capture endpoint (accepts all HTTP methods)
    path('hook/<uuid:endpoint_id>/', views.capture_webhook, name='capture_webhook'),
]

