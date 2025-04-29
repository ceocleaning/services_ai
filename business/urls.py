from django.urls import path
from . import views

app_name = 'business'

urlpatterns = [
    # Business registration
    path('register/', views.business_registration, name='register'),
    
    # Business profile and settings
    path('profile/', views.business_profile, name='profile'),
    path('profile/update/', views.update_profile, name='update_profile'),
    path('pricing/', views.business_pricing, name='pricing'),
    path('booking-settings/', views.booking_settings, name='booking_settings'),
    path('notifications/', views.notification_preferences, name='notifications'),
    path('upgrade/', views.upgrade_plan, name='upgrade'),
    
    # Service management
    path('service/add/', views.add_service, name='add_service'),
    path('service/update/', views.update_service, name='update_service'),
    path('service/delete/', views.delete_service, name='delete_service'),
    path('package/add/', views.add_package, name='add_package'),
    
    # API endpoints
    path('api/industries/', views.get_industries, name='api_industries'),
    path('api/register/', views.register_business, name='api_register_business'),
]
