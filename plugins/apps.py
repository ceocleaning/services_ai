from django.apps import AppConfig
import logging
import sys

class PluginsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'plugins'
    def ready(self):
        # Skip plugin loading when running migrations or certain management commands
        if 'migrate' in sys.argv or 'makemigrations' in sys.argv or 'collectstatic' in sys.argv:
            return
            
        # Import signal handlers
        import plugins.signals
        
        # Load enabled plugins
        from plugins.plugin_manager import plugin_manager
        try:
            # Discover plugins from the database
            plugin_manager.discover_plugins()
            
            # Load discovered plugins
            plugin_manager.discover_plugins()
            
            print(f"Successfully loaded {len(plugin_manager.loaded_plugins)} plugins")
        except Exception as e:
            # This might happen during migrations when the database table doesn't exist yet
            print(f"Error loading plugins: {str(e)}")
            
            # Don't crash the app if plugin loading fails
            # This allows the app to start even if there are issues with plugins