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
    path('robots.txt', views.robots_txt, name='robots_txt'),
    
    # Blog URLs
    path('blog/', views.blog_list, name='blog_list'),
    path('blog/<slug:slug>/', views.blog_detail, name='blog_detail'),
    path('blog/category/<slug:slug>/', views.blog_category, name='blog_category'),
]

