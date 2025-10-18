"""
Dynamic URL routing for plugins

This module handles dynamic registration of plugin URLs at runtime.
"""

from django.urls import path, include
from django.http import HttpResponse
from .plugin_manager import plugin_manager
from .models import Plugin


def get_plugin_urls():
    """
    Dynamically generate URL patterns from all active plugins
    
    Returns:
        List of URL patterns
    """
    urlpatterns = []
    
    try:
        # Get all enabled and approved plugins
        plugins = Plugin.objects.filter(enabled=True, status='approved')
        
        for plugin in plugins:
            try:
                # Call the register_routes hook
                routes = plugin_manager.call_hook('register_routes', plugin_id=plugin.id)
                
                if routes:
                    for route_list in routes:
                        if route_list:
                            for route in route_list:
                                # Route should be (pattern, view, name)
                                if len(route) >= 2:
                                    pattern = route[0]
                                    view = route[1]
                                    name = route[2] if len(route) > 2 else None
                                    
                                    # Prefix plugin routes with plugin name
                                    plugin_pattern = f'plugin/{plugin.name.lower().replace(" ", "-")}/{pattern}'
                                    
                                    print(f"[PLUGIN ROUTES] Registering: {plugin_pattern}")
                                    
                                    if name:
                                        urlpatterns.append(
                                            path(plugin_pattern, view, name=f'plugin_{plugin.id}_{name}')
                                        )
                                    else:
                                        urlpatterns.append(
                                            path(plugin_pattern, view)
                                        )
            except Exception as e:
                print(f"Error loading routes for plugin {plugin.name}: {str(e)}")
                import traceback
                traceback.print_exc()
    except Exception as e:
        # Database might not be ready yet
        print(f"Error accessing plugins for URL routing: {str(e)}")
    
    return urlpatterns


# Create a simple view that returns plugin URLs
def plugin_router(request, plugin_name, path_info):
    """
    Route requests to plugin views
    
    This is a fallback router that can handle plugin requests
    """
    return HttpResponse(f"Plugin router: {plugin_name}/{path_info}")
