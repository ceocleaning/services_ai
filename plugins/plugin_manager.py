import os
import sys
import importlib.util
import json
import pluggy

from django.conf import settings
from plugins.hookspecs import PluginHooks
from plugins.models import Plugin

class ServicesAIPluginManager:
    """Plugin manager for the Services AI platform"""
    
    def __init__(self):
        self.manager = pluggy.PluginManager("services_ai")
        self.manager.add_hookspecs(PluginHooks)
        self.loaded_plugins = {}
        
    def get_plugin_dir(self):
        """Get the directory where plugins are stored"""
        # First check if the plugin_packages directory exists in the project root
        project_root = settings.BASE_DIR
        plugin_packages_dir = os.path.join(project_root, 'plugin_packages')
        
        # If not, use the plugins directory within the app
        if not os.path.exists(plugin_packages_dir):
            plugin_packages_dir = os.path.join(project_root, 'plugins')
            
        return plugin_packages_dir
    
    def discover_plugins(self):
        """Discover and load all enabled plugins"""
        plugins = Plugin.objects.filter(enabled=True)
        
        for plugin in plugins:
            self.load_plugin(plugin)
    
    def load_plugin(self, plugin):
        """Load a specific plugin"""
        if plugin.id in self.loaded_plugins:
            return self.loaded_plugins[plugin.id]
        
        try:
            # If plugin path doesn't exist, try to find it in standard locations
            if not os.path.exists(plugin.package_path):
                # Try in plugin_packages directory
                plugin_packages_dir = self.get_plugin_dir()
                plugin_dir = os.path.join(plugin_packages_dir, plugin.name)
                if os.path.exists(plugin_dir):
                    plugin.package_path = plugin_dir
                    plugin.save()
                else:
                    # Try sample_plugin directory as fallback for the Sample Plugin
                    if plugin.name == "Sample Plugin":
                        sample_plugin_dir = os.path.join(plugin_packages_dir, 'sample_plugin')
                        if os.path.exists(sample_plugin_dir):
                            plugin.package_path = sample_plugin_dir
                            plugin.save()
            
            # Add plugin directory to path
            plugin_dir = plugin.package_path
            if not os.path.exists(plugin_dir):
                raise FileNotFoundError(f"Plugin directory not found: {plugin_dir}")
                
            if plugin_dir not in sys.path:
                sys.path.insert(0, plugin_dir)
            
            # Load the entry point module
            # If entry_point doesn't have .py extension, add it
            entry_point = plugin.entry_point
            if not entry_point.endswith('.py'):
                entry_point = f"{entry_point}.py"
                
            module_path = os.path.join(plugin_dir, entry_point)
            module_name = f"plugin_{plugin.id}"
            
            spec = importlib.util.spec_from_file_location(module_name, module_path)
            if spec is None:
                print(f"Error loading plugin {plugin.name}: Could not find module at {module_path}")
                return None
                
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            
            # Get the plugin class instance if specified in manifest
            if plugin.plugin_class:
                try:
                    # Try to find the plugin class in the module
                    plugin_class = getattr(module, plugin.plugin_class, None)
                    
                    if plugin_class:
                        # Create an instance of the plugin class
                        plugin_instance = plugin_class()
                        # Register the plugin instance with Pluggy
                        self.manager.register(plugin_instance)
                        print(f"Registered plugin class {plugin.plugin_class} from {plugin.name}")
                    else:
                        # If plugin class not found, register the module itself
                        self.manager.register(module)
                        print(f"Plugin class {plugin.plugin_class} not found in {plugin.name}, registering module instead")
                except Exception as e:
                    # If there's an error instantiating the plugin class, register the module itself
                    self.manager.register(module)
                    print(f"Error instantiating plugin class {plugin.plugin_class} from {plugin.name}: {str(e)}. Registering module instead.")
            else:
                # Register the module directly if no plugin class specified
                self.manager.register(module)
                print(f"Registered module for plugin {plugin.name}")
            
            # Store the loaded plugin
            self.loaded_plugins[plugin.id] = module
            
            return module
        except Exception as e:
            print(f"Error loading plugin {plugin.name}: {str(e)}")
            return None
    
    def unload_plugin(self, plugin_id):
        """Unload a specific plugin"""
        if plugin_id in self.loaded_plugins:
            plugin_module = self.loaded_plugins[plugin_id]
            self.manager.unregister(plugin_module)
            del self.loaded_plugins[plugin_id]
    
    def call_hook(self, hook_name, **kwargs):
        """Call a specific hook with the given arguments"""
        try:
            # Access hook through manager.hook, this is the Pluggy way
            if not hasattr(self.manager, 'hook'):
                print(f"Error: Plugin manager has no 'hook' attribute. Manager type: {type(self.manager)}")
                # Try to see if hookspecs are properly registered
                print(f"Registered hookspecs: {self.manager.get_hookspecs()}")
                return []
                
            # Check if the hook exists
            if not hasattr(self.manager.hook, hook_name):
                # This is not an error, just means no plugins have implemented this hook
                return []
                
            # Get the hook implementation and call it
            hook = getattr(self.manager.hook, hook_name)
            return hook(**kwargs)
        except Exception as e:
            print(f"Error calling hook {hook_name}: {str(e)}")
            # Return empty list on error for safety
            return []
    
    def reload_all_plugins(self):
        """Reload all plugins"""
        # Store currently loaded plugin IDs
        loaded_ids = list(self.loaded_plugins.keys())
        
        # Unload all plugins
        for plugin_id in loaded_ids:
            self.unload_plugin(plugin_id)
        
        # Rediscover and load plugins
        self.discover_plugins()

# Create a singleton instance
plugin_manager = ServicesAIPluginManager()
