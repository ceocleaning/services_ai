from django import template
from django.template.defaultfilters import stringfilter
from django.urls import reverse
import os
import importlib.util
import json
from django.http import HttpResponse
from django.shortcuts import render
from ..models import Plugin, PluginSetting, PluginPermission
from ..plugin_manager import plugin_manager

register = template.Library()

@register.filter
def get_item(dictionary, key):
    """
    Get an item from a dictionary using a key.
    Usage: {{ dictionary|get_item:key }}
    """
    if not dictionary:
        return None
    
    if isinstance(dictionary, dict):
        return dictionary.get(key)
    elif isinstance(dictionary, (list, tuple)) and isinstance(key, int):
        if 0 <= key < len(dictionary):
            return dictionary[key]
    
    return None

@register.inclusion_tag('plugins/widgets/dashboard_widgets.html', takes_context=True)
def render_plugin_widgets(context):
    """
    Render all dashboard widgets from active plugins for the current user.
    Usage: {% render_plugin_widgets %}
    """
    request = context['request']
    user = request.user
    widgets_html = []
    widget_errors = []
    
    # Get all enabled plugins
    plugins = Plugin.objects.filter(enabled=True)
    
    # For each plugin, call the dashboard_widget hook
    for plugin in plugins:
        try:
            # Call the dashboard_widget hook for this plugin
            widgets = plugin_manager.call_hook('dashboard_widget',
                plugin_id=plugin.id, 
                context={
                    'request': request,
                    'user': user,
                    'plugin': plugin
                }
            )
            
            # Process the returned widgets
            if widgets:
                for widget in widgets:
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
    
    return {'widgets_html': widgets_html, 'widget_errors': widget_errors}
