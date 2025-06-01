import os
import json
import zipfile
import tempfile
import shutil
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
from django.http import HttpResponse, JsonResponse
from django.urls import reverse
from django.forms import modelformset_factory

from .models import Plugin, PluginPermission, PluginSetting
from .plugin_manager import plugin_manager
from .forms import PluginUploadForm, PluginSettingForm
from .events import get_dashboard_widgets

@login_required
def plugin_list(request):
    """View to list all installed plugins"""
    plugins = Plugin.objects.all().order_by('name')
    return render(request, 'plugins/list.html', {'plugins': plugins})

@login_required
def plugin_detail(request, plugin_id):
    """View plugin details"""
    plugin = get_object_or_404(Plugin, id=plugin_id)
    
    # Get plugin permissions
    permissions = plugin.permissions.all()
    
    # Get plugin settings
    settings = plugin.settings.all()
    
    # Check if plugin has a custom settings page
    custom_settings_page = None
    if plugin.enabled:
        try:
            result = plugin_manager.call_hook('settings_page', plugin_id=plugin_id)
            if result and len(result) > 0:
                custom_settings_page = result[0]
        except Exception as e:
            messages.error(request, f"Error loading custom settings page: {str(e)}")
    
    return render(request, 'plugins/detail.html', {
        'plugin': plugin,
        'permissions': permissions,
        'settings': settings,
        'custom_settings_page': custom_settings_page
    })

@login_required
def upload_plugin(request):
    """View to upload a new plugin"""
    if request.method == 'POST':
        form = PluginUploadForm(request.POST, request.FILES)
        if form.is_valid():
            plugin_file = request.FILES['plugin_file']
            
            # Create a temporary directory
            with tempfile.TemporaryDirectory() as temp_dir:
                # Extract the plugin zip file
                zip_path = os.path.join(temp_dir, plugin_file.name)
                with open(zip_path, 'wb+') as destination:
                    for chunk in plugin_file.chunks():
                        destination.write(chunk)
                
                try:
                    # Extract the zip file
                    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                        zip_ref.extractall(temp_dir)
                    
                    # Look for manifest.json
                    manifest_path = None
                    for root, dirs, files in os.walk(temp_dir):
                        if 'manifest.json' in files:
                            manifest_path = os.path.join(root, 'manifest.json')
                            break
                    
                    if not manifest_path:
                        messages.error(request, 'Invalid plugin: manifest.json not found')
                        return redirect('plugin_list')
                    
                    # Load and validate manifest
                    with open(manifest_path, 'r') as f:
                        manifest = json.load(f)
                    
                    # Validate required fields
                    required_fields = ['name', 'version', 'description', 'author', 'email']
                    for field in required_fields:
                        if field not in manifest:
                            messages.error(request, f'Invalid manifest: {field} is required')
                            return redirect('plugin_list')
                    
                    # Create plugin directory if it doesn't exist
                    plugins_dir = os.path.join(settings.BASE_DIR, 'plugin_packages')
                    os.makedirs(plugins_dir, exist_ok=True)
                    
                    # Create directory for this plugin
                    plugin_dir = os.path.join(plugins_dir, manifest['name'])
                    if os.path.exists(plugin_dir):
                        shutil.rmtree(plugin_dir)
                    
                    # Copy plugin files
                    plugin_source_dir = os.path.dirname(manifest_path)
                    shutil.copytree(plugin_source_dir, plugin_dir)
                    
                    # Get entry point and plugin class
                    entry_point = manifest.get('entry_point', 'main.py')
                    plugin_class = manifest.get('plugin_class', None)
                    
                    # Create the plugin in the database
                    plugin = Plugin.objects.create(
                        name=manifest['name'],
                        description=manifest['description'],
                        version=manifest['version'],
                        author=manifest['author'],
                        email=manifest['email'],
                        package_path=plugin_dir,
                        entry_point=entry_point,
                        plugin_class=plugin_class,
                        manifest=manifest,
                        enabled=True
                    )
                    
                    # Create permissions
                    if 'permissions' in manifest:
                        for permission in manifest['permissions']:
                            PluginPermission.objects.create(
                                plugin=plugin,
                                permission_name=permission,
                                enabled=False  # Default to disabled for security
                            )
                    
                    # Create settings
                    if 'settings' in manifest:
                        for setting in manifest['settings']:
                            PluginSetting.objects.create(
                                plugin=plugin,
                                setting_name=setting['name'],
                                setting_type=setting['type'],
                                setting_value=setting.get('default', '')
                            )
                    
                    # Load the plugin
                    if plugin.enabled:
                        plugin_manager.load_plugin(plugin)
                        
                        # Call plugin_installed hook
                        try:
                            plugin_manager.call_hook('plugin_installed')
                        except Exception as e:
                            messages.warning(request, f"Error in plugin_installed hook: {str(e)}")
                    
                    messages.success(request, f'Plugin {plugin.name} installed successfully')
                    return redirect('plugins:plugin_detail', plugin_id=plugin.id)
                
                except Exception as e:
                    messages.error(request, f'Error installing plugin: {str(e)}')
                    return redirect('plugins:plugin_list')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = PluginUploadForm()
    
    return render(request, 'plugins/upload.html', {'form': form})

@login_required
def toggle_plugin(request, plugin_id):
    """Enable or disable a plugin"""
    plugin = get_object_or_404(Plugin, id=plugin_id)
    plugin.enabled = not plugin.enabled
    plugin.save()
    
    if plugin.enabled:
        # Load the plugin
        plugin_manager.load_plugin(plugin)
        messages.success(request, f'Plugin {plugin.name} enabled')
    else:
        # Unload the plugin
        plugin_manager.unload_plugin(plugin.id)
        messages.success(request, f'Plugin {plugin.name} disabled')
    
    return redirect('plugins:plugin_detail', plugin_id=plugin.id)

@login_required
def toggle_permission(request, plugin_id, permission_id):
    """Enable or disable a plugin permission"""
    permission = get_object_or_404(PluginPermission, id=permission_id, plugin_id=plugin_id)
    permission.enabled = not permission.enabled
    permission.save()
    
    messages.success(request, f'Permission {permission.permission_name} {"enabled" if permission.enabled else "disabled"}')
    return redirect('plugins:plugin_detail', plugin_id=plugin_id)

@login_required
def update_settings(request, plugin_id):
    """Update plugin settings"""
    plugin = get_object_or_404(Plugin, id=plugin_id)
    
    if request.method == 'POST':
        # Process each setting
        for setting in plugin.settings.all():
            setting_name = setting.setting_name
            if setting_name in request.POST:
                setting_value = request.POST[setting_name]
                
                # Handle checkbox fields
                if setting.setting_type == 'checkbox':
                    setting_value = 'true' if setting_value == 'true' else 'false'
                
                setting.setting_value = setting_value
                setting.save()
        
        messages.success(request, 'Settings updated successfully')
        return redirect('plugins:plugin_detail', plugin_id=plugin.id)
    
    return redirect('plugins:plugin_detail', plugin_id=plugin.id)

@login_required
def uninstall_plugin(request, plugin_id):
    """Uninstall a plugin"""
    plugin = get_object_or_404(Plugin, id=plugin_id)
    
    if request.method == 'POST':
        # Call plugin_uninstalled hook if plugin is enabled
        if plugin.enabled:
            try:
                plugin_manager.call_hook('plugin_uninstalled')
            except Exception as e:
                messages.warning(request, f"Error in plugin_uninstalled hook: {str(e)}")
        
        # Unload the plugin
        plugin_manager.unload_plugin(plugin.id)
        
        # Remove plugin directory
        if os.path.exists(plugin.package_path):
            try:
                shutil.rmtree(plugin.package_path)
            except Exception as e:
                messages.warning(request, f"Error removing plugin files: {str(e)}")
        
        # Delete plugin from database
        plugin_name = plugin.name
        plugin.delete()
        
        messages.success(request, f'Plugin {plugin_name} uninstalled successfully')
        return redirect('plugins:plugin_list')
    
    return render(request, 'plugins/confirm_uninstall.html', {'plugin': plugin})

@login_required
def get_dashboard_widgets(request):
    """Get dashboard widgets from all plugins as JSON"""
    widgets_html = []
    widget_errors = []
    context = {'user': request.user, 'request': request}
    
    # Get all enabled plugins
    plugins = Plugin.objects.filter(enabled=True)
    
    # For each plugin, call the dashboard_widget hook
    for plugin in plugins:
        try:
            # Check if dashboard_widget permission is enabled
            has_permission = plugin.permissions.filter(permission_name='dashboard_widget', enabled=True).exists()
            if not has_permission:
                continue
                
            # Call the dashboard_widget hook for this plugin
            results = plugin_manager.call_hook('dashboard_widget',
                plugin_id=plugin.id,
                context={
                    'request': request,
                    'user': request.user,
                    'plugin': plugin
                }
            )
            
            # Process the returned widgets
            if results and len(results) > 0:
                for widget in results:
                    if widget:
                        widgets_html.append(widget)
                        
        except Exception as e:
            # Log the error but continue with other plugins
            import traceback
            error_msg = f"Error rendering dashboard widget for {plugin.name}: {str(e)}"
            error_traceback = traceback.format_exc()
            print(error_msg)
            print(error_traceback)
            
            # Add error to widget_errors to display in the dashboard
            widget_errors.append({
                'plugin_name': plugin.name,
                'error_msg': error_msg,
                'traceback': error_traceback
            })
    
    return JsonResponse({
        'widgets': widgets_html, 
        'errors': widget_errors
    })
