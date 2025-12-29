"""
URL Configuration for the formatter app
"""
from django.contrib.staticfiles.storage import staticfiles_storage
from django.urls import path, re_path
from django.views.generic.base import RedirectView
from . import views

urlpatterns = [
    path('favicon.ico', RedirectView.as_view(
        url=staticfiles_storage.url('favicon.ico'),
        permanent=True
    )),
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
    path('csv-to-json/', views.csv_to_json_page, name='csv_to_json_page'),
    path('xsd-to-json-schema/', views.xsd_to_json_schema_page, name='xsd_to_json_schema_page'),
    path('json-to-jsonl/', views.json_to_jsonl_page, name='json_to_jsonl_page'),
    path('json-diff/', views.json_diff_page, name='json_diff_page'),
    path('json-schema-validator/', views.json_schema_page, name='json_schema_page'),
    path('json-tree/', views.json_tree_page, name='json_tree_page'),
    path('json-visualizer/', views.json_visualizer_page, name='json_visualizer_page'),
    path('json-to-code/', views.json_to_code_page, name='json_to_code_page'),
    path('dummy-json/', views.dummy_json_page, name='dummy_json_page'),
    path('json-generator/', views.json_generator_page, name='json_generator_page'),
    path('json-formatter-online/', views.json_formatter_online_page, name='json_formatter_online_page'),
    
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
    path('lorem-ipsum/', views.lorem_ipsum_page, name='lorem_ipsum_page'),
    path('image-resizer/', views.image_resizer_page, name='image_resizer_page'),
    path('toon-converter/', views.toon_converter_page, name='toon_converter_page'),
    path('domain-age/', views.domain_age_page, name='domain_age_page'),
    path('resume-builder/', views.resume_builder, name='resume_builder'),
    
    # Calculator Pages
    path('calculator/', views.calculator_page, name='calculator_page'),
    path('percentage-calculator/', views.percentage_calculator_page, name='percentage_calculator_page'),
    path('age-calculator/', views.age_calculator_page, name='age_calculator_page'),
    path('date-calculator/', views.date_calculator_page, name='date_calculator_page'),
    path('loan-calculator/', views.loan_calculator_page, name='loan_calculator_page'),
    path('mortgage-calculator/', views.mortgage_calculator_page, name='mortgage_calculator_page'),
    path('car-payment-calculator/', views.car_payment_calculator_page, name='car_payment_calculator_page'),
    path('sip-calculator/', views.sip_calculator_page, name='sip_calculator_page'),
    path('compound-interest-calculator/', views.compound_interest_calculator_page, name='compound_interest_calculator_page'),
    path('salary-calculator/', views.salary_calculator_page, name='salary_calculator_page'),
    path('bmi-calculator/', views.bmi_calculator_page, name='bmi_calculator_page'),
    path('calorie-calculator/', views.calorie_calculator_page, name='calorie_calculator_page'),
    path('time-calculator/', views.time_calculator_page, name='time_calculator_page'),
    path('gpa-calculator/', views.gpa_calculator_page, name='gpa_calculator_page'),
    path('unit-converter/', views.unit_converter_page, name='unit_converter_page'),
    path('discount-calculator/', views.discount_calculator_page, name='discount_calculator_page'),
    path('tip-calculator/', views.tip_calculator_page, name='tip_calculator_page'),
    path('currency-calculator/', views.currency_calculator_page, name='currency_calculator_page'),
    path('concrete-calculator/', views.concrete_calculator_page, name='concrete_calculator_page'),
    path('graphing-calculator/', views.graphing_calculator_page, name='graphing_calculator_page'),
    
    # Legal Pages
    path('terms/', views.terms_page, name='terms_page'),
    path('code-of-conduct/', views.code_of_conduct_page, name='code_of_conduct_page'),
    
    # Security Tools
    path('password-generator/', views.password_generator_page, name='password_generator_page'),
    path('url-encoder/', views.url_encoder_page, name='url_encoder_page'),
    path('typing-test/', views.typing_test_page, name='typing_test_page'),
    
    # Code Tool API Endpoints

    path('api/qr-generator/', views.generate_qr_code, name='generate_qr_code'),
    path('api/domain-age/', views.domain_age_api, name='domain_age_api'),
    path('api/typing-test/submit/', views.submit_typing_score, name='submit_typing_score'),
    path('api/typing-test/leaderboard/', views.get_typing_leaderboard, name='get_typing_leaderboard'),
    
    # Mock API Management Endpoints
    path('api/my-ip/', views.get_client_ip_api, name='get_client_ip_api'),
    path('api/mock/create/', views.create_mock_endpoint, name='create_mock_endpoint'),
    path('api/mock/my-endpoints/', views.list_my_endpoints, name='list_my_endpoints'),
    path('api/mock/<str:endpoint_id>/info/', views.get_mock_endpoint_info, name='get_mock_endpoint_info'),
    path('api/mock/<str:endpoint_id>/update/', views.update_mock_endpoint, name='update_mock_endpoint'),
    path('api/mock/<str:endpoint_id>/delete/', views.delete_mock_endpoint, name='delete_mock_endpoint'),
    
    # Backward compatible - old style /api/mock/{uuid}/
    path('api/mock/<str:endpoint_id>/', views.serve_mock_endpoint, name='serve_mock_endpoint'),
    
    # Dynamic path-based mock endpoints: /{user_path}/{uuid}/
    # Examples: /api/users/550e8400-e29b-41d4-a716-446655440000/
    re_path(r'^(?P<user_path>[\w/-]+)/(?P<endpoint_id>[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})/$', views.serve_path_mock_endpoint, name='serve_path_mock_endpoint'),

    # Careers Pages
    path('careers/', views.careers_page, name='careers_page'),
    path('careers/<slug:slug>/', views.job_detail, name='job_detail'),
    
    path('robots.txt', views.robots_txt, name='robots_txt'),
    path('llms.txt', views.llms_txt, name='llms_txt'),
    
    # Blog URLs
    path('blog/', views.blog_list, name='blog_list'),
    path('blog/<slug:slug>/', views.blog_detail, name='blog_detail'),
    path('blog/category/<slug:slug>/', views.blog_category, name='blog_category'),
    path('api/blogs/', views.blog_api, name='blog_api'),
    
    # Tutorial URLs
    path('tutorials/', views.tutorials_list, name='tutorials_list'),
    path('tutorials/<slug:slug>/', views.tutorial_detail, name='tutorial_detail'),

    # redirect urls
    path(
        "json-schema/",
        RedirectView.as_view(
            url="/json-schema-validator/",
            permanent=True
        ),
    ),

]

