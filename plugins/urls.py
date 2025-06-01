from django.urls import path
from . import views

app_name = 'plugins'

urlpatterns = [
    # Plugin Management
    path('', views.plugin_list, name='plugin_list'),
    path('upload/', views.upload_plugin, name='upload_plugin'),
    path('<int:plugin_id>/', views.plugin_detail, name='plugin_detail'),
    path('<int:plugin_id>/toggle/', views.toggle_plugin, name='toggle_plugin'),
    path('<int:plugin_id>/permission/<int:permission_id>/toggle/', views.toggle_permission, name='toggle_permission'),
    path('<int:plugin_id>/settings/', views.update_settings, name='update_settings'),
    path('<int:plugin_id>/uninstall/', views.uninstall_plugin, name='uninstall_plugin'),
    path('dashboard/widgets/', views.get_dashboard_widgets, name='get_dashboard_widgets'),
]