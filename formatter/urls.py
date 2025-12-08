"""
URL Configuration for the formatter app
"""

from django.urls import path
from . import views

urlpatterns = [
    # API endpoints
    path('api/format/', views.format_json, name='format_json'),
    path('api/minify/', views.minify_json, name='minify_json'),
    path('api/validate/', views.validate_json, name='validate_json'),
    path('api/convert/xml/', views.convert_to_xml, name='convert_to_xml'),
    path('api/convert/csv/', views.convert_to_csv, name='convert_to_csv'),
    path('api/base64/encode/', views.base64_encode, name='base64_encode'),
    path('api/base64/decode/', views.base64_decode, name='base64_decode'),
    
    # Page views
    path('base64/', views.base64_page, name='base64_page'),
    path('about/', views.about_page, name='about_page'),
    path('contact/', views.contact_page, name='contact_page'),
    path('privacy/', views.privacy_page, name='privacy_page'),
    
    # JSON Tool Pages
    path('json-to-yaml/', views.json_to_yaml_page, name='json_to_yaml_page'),
    path('json-diff/', views.json_diff_page, name='json_diff_page'),
    path('json-schema/', views.json_schema_page, name='json_schema_page'),
    path('json-tree/', views.json_tree_page, name='json_tree_page'),
    path('dummy-json/', views.dummy_json_page, name='dummy_json_page'),
    
    # API & Network Tool Pages
    path('http-headers/', views.http_headers_page, name='http_headers_page'),
    path('ip-info/', views.ip_info_page, name='ip_info_page'),
    path('dns-lookup/', views.dns_lookup_page, name='dns_lookup_page'),
    path('ssl-checker/', views.ssl_checker_page, name='ssl_checker_page'),
    path('cors-checker/', views.cors_checker_page, name='cors_checker_page'),
    
    # API & Network Tool API Endpoints
    path('api/dns-lookup/', views.dns_lookup_api, name='dns_lookup_api'),
    path('api/ssl-checker/', views.ssl_checker_api, name='ssl_checker_api'),
    path('api/cors-checker/', views.cors_checker_api, name='cors_checker_api'),
    
    # Code Tool Pages
    path('cron-builder/', views.cron_builder_page, name='cron_builder_page'),
    path('markdown-preview/', views.markdown_preview_page, name='markdown_preview_page'),
    path('sql-formatter/', views.sql_formatter_page, name='sql_formatter_page'),
    path('qr-generator/', views.qr_generator_page, name='qr_generator_page'),
    path('meta-tag-generator/', views.meta_tag_generator_page, name='meta_tag_generator_page'),
    path('swagger-viewer/', views.swagger_viewer_page, name='swagger_viewer_page'),
    path('mock-api/', views.mock_api_generator_page, name='mock_api_generator_page'),
    path('push-notification-tester/', views.push_notification_tester_page, name='push_notification_tester_page'),
    path('api-response-tester/', views.api_response_tester_page, name='api_response_tester_page'),
    path('image-to-base64/', views.image_to_base64_page, name='image_to_base64_page'),
    path('json-editor/', views.json_editor_page, name='json_editor_page'),
    path('regex-tester/', views.regex_tester_page, name='regex_tester_page'),
    
    # Code Tool API Endpoints
    path('api/qr-generator/', views.generate_qr_code, name='generate_qr_code'),
    
    path('robots.txt', views.robots_txt, name='robots_txt'),
    
    # Blog URLs
    path('blog/', views.blog_list, name='blog_list'),
    path('blog/<slug:slug>/', views.blog_detail, name='blog_detail'),
    path('blog/category/<slug:slug>/', views.blog_category, name='blog_category'),
]

