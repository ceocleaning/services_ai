from django.urls import path
from . import views, views_chat

app_name = 'ai_website'

urlpatterns = [
    # Chat-Style Builder (New Default)
    path('', views_chat.chat_builder, name='builder'),
    path('chat/', views_chat.chat_builder, name='chat_builder'),
    
    # AJAX Endpoints for Chat Interface
    path('api/generate/', views_chat.generate_website_chat, name='api_generate'),
    path('api/process/<int:session_id>/', views_chat.process_generation, name='api_process'),
    path('api/status/<int:session_id>/', views_chat.get_session_status, name='api_status'),
    path('api/history/', views_chat.get_conversation_history, name='api_history'),
    
    # Legacy Builder (Keep for backward compatibility)
    path('legacy/', views.website_builder, name='legacy_builder'),
    path('generate/', views.generate_website, name='generate'),
    
    # Preview Website
    path('preview/', views.preview_website, name='preview'),
    
    # Toggle Publish Status
    path('toggle-publish/<int:website_id>/', views.toggle_publish, name='toggle_publish'),
    
    # Delete Website
    path('delete/<int:website_id>/', views.delete_website, name='delete'),
]
