"""
Sample Plugin for Services AI
This demonstrates how to implement hooks for the Services AI plugin system.
"""
import json
import datetime
import sys
import os
import pluggy

# Make sure the parent directory is in the path
parent_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)
    print(f"Added parent directory to path: {parent_dir}")

# Import the hookimpl decorator directly from the hooks module
from plugins.hooks import hookimpl

# Create a plugin manager for testing
PM = pluggy.PluginManager("services_ai")

# Define hook specifications (normally this would be in the core application)
class ServiceAIHooks:
    @staticmethod
    @pluggy.HookspecMarker("services_ai")
    def lead_created(lead, context):
        """Called when a new lead is created"""

    @staticmethod
    @pluggy.HookspecMarker("services_ai")
    def plugin_installed(plugin_id, plugin_info):
        """Called when the plugin is installed"""

    @staticmethod
    @pluggy.HookspecMarker("services_ai")
    def plugin_uninstalled(plugin_id):
        """Called when the plugin is uninstalled"""

    @staticmethod
    @pluggy.HookspecMarker("services_ai")
    def plugin_enabled(plugin_id):
        """Called when the plugin is enabled"""

    @staticmethod
    @pluggy.HookspecMarker("services_ai")
    def plugin_disabled(plugin_id):
        """Called when the plugin is disabled"""

    @staticmethod
    @pluggy.HookspecMarker("services_ai")
    def booking_created(booking, context):
        """Called when a new booking is created"""

    @staticmethod
    @pluggy.HookspecMarker("services_ai")
    def booking_updated(booking, context):
        """Called when a booking is updated"""

    @staticmethod
    @pluggy.HookspecMarker("services_ai")
    def dashboard_widget(plugin_id, context):
        """Provides HTML content for dashboard widget"""

    @staticmethod
    @pluggy.HookspecMarker("services_ai")
    def settings_page(plugin_id, context):
        """Provides HTML content for plugin settings page"""

    @staticmethod
    @pluggy.HookspecMarker("services_ai")
    def data_export(export_type, start_date, end_date, context):
        """Provides data for export"""

# Register hook specifications
PM.add_hookspecs(ServiceAIHooks)


# Define the plugin class with hook implementations
# For pluggy to properly recognize class methods as hook implementations,
# we need to use the hookimpl decorator and register the class with the plugin manager

# This is a class-based plugin implementation
# IMPORTANT: For class methods to be recognized as hook implementations,
# the decorator must be applied to the function BEFORE it becomes a method
# This is why we're using a different approach with the DirectPlugin class below
class SamplePlugin:
    """Sample plugin implementation for Services AI"""
    
    def __init__(self):
        print("SamplePlugin instance created")
    
    # Use the hookimpl decorator to mark this method as a hook implementation
    @hookimpl
    def lead_created(self, lead, context):
        """Called when a new lead is created"""
      
        print(f"New lead created: {lead.first_name} {lead.last_name} (ID: {lead.id})")

        # Create an animated toast notification with CSS animations
        html_alert = f"""
        <div id="lead-toast-notification" class="lead-toast-notification animate-in">
            <div class="lead-toast-header">
                <div class="lead-toast-icon">
                    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                        <circle cx="12" cy="12" r="12" fill="#4CAF50" opacity="0.2"/>
                        <path d="M8 12L10.5 14.5L16 9" stroke="#4CAF50" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                    </svg>
                </div>
                <div class="lead-toast-title">New Lead Created!</div>
                <button class="lead-toast-close" onclick="document.getElementById('lead-toast-notification').classList.add('animate-out');setTimeout(() => document.getElementById('lead-toast-notification').remove(), 500);">
                    &times;
                </button>
            </div>
            <div class="lead-toast-body">
                <div class="lead-info">
                    <div class="lead-name">{lead.first_name} {lead.last_name}</div>
                    <div class="lead-id">ID: {lead.id}</div>
                </div>
                <div class="lead-actions">
                    <button class="lead-action-btn" onclick="window.location.href='/leads/{lead.id}/'">View Details</button>
                </div>
            </div>
        </div>
        
        <style>
        .lead-toast-notification {{
            position: fixed;
            top: 20px;
            right: 20px;
            width: 320px;
            background: white;
            border-radius: 8px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
            overflow: hidden;
            z-index: 9999;
            border-left: 4px solid #4CAF50;
        }}
        
        .lead-toast-header {{
            display: flex;
            align-items: center;
            padding: 12px 16px;
            background: #f9f9f9;
            border-bottom: 1px solid #eee;
        }}
        
        .lead-toast-icon {{
            margin-right: 12px;
        }}
        
        .lead-toast-title {{
            font-weight: 600;
            font-size: 16px;
            flex-grow: 1;
            color: #333;
        }}
        
        .lead-toast-close {{
            background: none;
            border: none;
            font-size: 20px;
            cursor: pointer;
            color: #999;
        }}
        
        .lead-toast-body {{
            padding: 16px;
        }}
        
        .lead-info {{
            margin-bottom: 12px;
        }}
        
        .lead-name {{
            font-size: 15px;
            font-weight: 500;
            margin-bottom: 4px;
            color: #333;
        }}
        
        .lead-id {{
            font-size: 13px;
            color: #666;
        }}
        
        .lead-actions {{
            display: flex;
            justify-content: flex-end;
        }}
        
        .lead-action-btn {{
            background: #4CAF50;
            color: white;
            border: none;
            padding: 6px 12px;
            border-radius: 4px;
            cursor: pointer;
            font-size: 14px;
            transition: background 0.2s;
        }}
        
        .lead-action-btn:hover {{
            background: #3d8b40;
        }}
        
        /* Animation classes */
        .animate-in {{
            animation: slideIn 0.5s forwards;
        }}
        
        .animate-out {{
            animation: slideOut 0.5s forwards;
        }}
        
        @keyframes slideIn {{
            from {{
                transform: translateX(100%);
                opacity: 0;
            }}
            to {{
                transform: translateX(0);
                opacity: 1;
            }}
        }}
        
        @keyframes slideOut {{
            from {{
                transform: translateX(0);
                opacity: 1;
            }}
            to {{
                transform: translateX(100%);
                opacity: 0;
            }}
        }}
        
        /* Auto-dismiss after 10 seconds */
        .lead-toast-notification {{
            animation: slideIn 0.5s forwards, dismissAfterDelay 10s forwards;
        }}
        
        @keyframes dismissAfterDelay {{
            0%, 90% {{
                transform: translateX(0);
                opacity: 1;
            }}
            100% {{
                transform: translateX(100%);
                opacity: 0;
            }}
        }}
        </style>
        
        <script>
        // Auto-remove the element after animation completes
        setTimeout(() => {{
            const notification = document.getElementById('lead-toast-notification');
            if (notification) {{
                notification.remove();
            }}
        }}, 10500);
        </script>
        """
        
        return {"status": "success", "message": f"Sample plugin processed new lead: {lead.first_name} {lead.last_name}", "html": html_alert}
    
    # Mark other methods as hook implementations
    @hookimpl
    def plugin_installed(self, plugin_id, plugin_info):
        """Called when the plugin is installed"""
        print(f"Sample plugin installed with ID: {plugin_id}")
        return {"status": "success", "message": "Sample plugin installed successfully"}
    
    @hookimpl
    def plugin_uninstalled(self, plugin_id):
        """Called when the plugin is uninstalled"""
        print(f"Sample plugin uninstalled with ID: {plugin_id}")
        return {"status": "success", "message": "Sample plugin uninstalled successfully"}
    
    @hookimpl
    def plugin_enabled(self, plugin_id):
        """Called when the plugin is enabled"""
        print(f"Sample plugin enabled with ID: {plugin_id}")
        return {"status": "success", "message": "Sample plugin enabled successfully"}
    
    @hookimpl
    def plugin_disabled(self, plugin_id):
        """Called when the plugin is disabled"""
        print(f"Sample plugin disabled with ID: {plugin_id}")
        return {"status": "success", "message": "Sample plugin disabled successfully"}
    
    @hookimpl
    def booking_created(self, booking, context):
        """Called when a new booking is created"""
        print(f"New booking created: {booking.id} for lead {booking.lead.name}")
        return {"status": "success", "message": f"Sample plugin processed new booking for: {booking.lead.name}"}
    
    @hookimpl
    def booking_updated(self, booking, context):
        """Called when a booking is updated"""
        print(f"Booking updated: {booking.id}")
        return {"status": "success", "message": f"Sample plugin processed booking update for ID: {booking.id}"}
    
    @hookimpl
    def dashboard_widget(self, plugin_id, context):
        """Provides HTML content for dashboard widget"""
        user = context.get('user')
        username = user.username if user else "Guest"
        
        widget_html = f"""
        <div class="plugin-widget">
            <div class="plugin-widget-header">
                <h5>Sample Plugin</h5>
            </div>
            <div class="plugin-widget-body">
                <p>Hello {username}! This is a sample dashboard widget from the Sample Plugin.</p>
                <p>Current time: <span id="sample-plugin-time"></span></p>
                <button class="btn btn-sm btn-primary" id="sample-plugin-btn">Click Me</button>
                
                <script>
                    // Update the time every second
                    setInterval(function() {{
                        document.getElementById('sample-plugin-time').textContent = new Date().toLocaleTimeString();
                    }}, 1000);
                    
                    // Add button click event
                    document.getElementById('sample-plugin-btn').addEventListener('click', function() {{
                        alert('Hello from Sample Plugin!');
                    }});
                </script>
            </div>
        </div>
        """
        
        return widget_html
    
    @hookimpl
    def settings_page(self, plugin_id, context):
        """Provides HTML content for plugin settings page"""
        settings_html = """
        <div class="card">
            <div class="card-header">
                <h5>Custom Settings</h5>
            </div>
            <div class="card-body">
                <p>This is a sample custom settings page for the Sample Plugin.</p>
                <form method="post" action="#">
                    <div class="mb-3">
                        <label for="sample_api_key" class="form-label">API Key</label>
                        <input type="password" class="form-control" id="sample_api_key" name="sample_api_key">
                        <div class="form-text">Enter your API key for external integrations.</div>
                    </div>
                    <div class="mb-3">
                        <label for="sample_endpoint" class="form-label">API Endpoint</label>
                        <input type="text" class="form-control" id="sample_endpoint" name="sample_endpoint">
                    </div>
                    <button type="submit" class="btn btn-primary">Save Settings</button>
                </form>
            </div>
        </div>
        """
        
        return settings_html
    
    @hookimpl
    def data_export(self, export_type, start_date, end_date, context):
        """Provides data for export
        
        Args:
            export_type: Type of data to export (leads, bookings, etc.)
            start_date: Start date for data range
            end_date: End date for data range
            context: Dictionary containing context information including request and user
            
        Returns:
            List of dictionaries containing exported data
        """
        # Get user from context for permissions check
        user = context.get('user')
        
        # Check if user has permission to export data
        if user and user.is_authenticated:
            if export_type == 'leads':
                # Normally, we would query the database here based on date range
                # For demonstration, we're returning sample data
                return [{
                    'name': 'Sample Lead 1',
                    'email': 'sample1@example.com',
                    'phone': '123-456-7890',
                    'created_at': start_date.strftime('%Y-%m-%d'),
                    'exported_by': user.username
                }, {
                    'name': 'Sample Lead 2',
                    'email': 'sample2@example.com',
                    'phone': '987-654-3210',
                    'created_at': end_date.strftime('%Y-%m-%d'),
                    'exported_by': user.username
                }]
            elif export_type == 'bookings':
                # Example for another export type
                return [{
                    'id': 'BOOK-001',
                    'lead_name': 'Sample Lead 1',
                    'date': datetime.datetime.now().strftime('%Y-%m-%d %H:%M'),
                    'status': 'Confirmed',
                    'exported_by': user.username
                }]
        
        # Return empty list if user is not authenticated or for unsupported export types
        return []


# Verify hook implementations when this module is loaded
def verify_hook_implementations():
    """Verify that hook implementations are properly decorated"""
    print("\n=== VERIFYING HOOK IMPLEMENTATIONS ====")
    plugin_instance = SamplePlugin()
    hook_count = 0
    
    # Register the plugin instance with our global plugin manager
    # that already has the hook specifications registered
    PM.register(plugin_instance)
    
    # Check all methods in the plugin instance
    print("Checking plugin instance methods:")
    for attr_name in dir(plugin_instance):
        if attr_name.startswith('_'):
            continue
            
        try:
            attr = getattr(plugin_instance, attr_name)
            print(f"  Checking attribute: {attr_name}, type: {type(attr)}")
            
            # Check if the attribute is callable
            if callable(attr):
                # Debug information
                is_hookimpl = hasattr(attr, '__hookimpl__')
                has_func = hasattr(attr, '__func__')
                func_is_hookimpl = has_func and hasattr(attr.__func__, '__hookimpl__')
                
                print(f"    Is callable: Yes")
                print(f"    Has __hookimpl__: {is_hookimpl}")
                print(f"    Has __func__: {has_func}")
                print(f"    __func__ has __hookimpl__: {func_is_hookimpl}")
                
                # Check for hookimpl directly
                if is_hookimpl:
                    hook_count += 1
                    print(f"    + Verified hook implementation: {attr_name}")
                    print(f"      Hookimpl attributes: {attr.__hookimpl__}")
                # For bound methods, check __func__
                elif func_is_hookimpl:
                    hook_count += 1
                    print(f"    + Verified hook implementation via __func__: {attr_name}")
                    print(f"      Hookimpl attributes: {attr.__func__.__hookimpl__}")
        except Exception as e:
            print(f"  Error inspecting {attr_name}: {str(e)}")
    
    # Check the registered hook implementations in the plugin manager
    print("\nChecking registered hook implementations in plugin manager:")
    for hook_name in PM.hook.__dict__.keys():
        if hook_name.startswith('_'):
            continue
            
        hook_caller = getattr(PM.hook, hook_name)
        impls = hook_caller.get_hookimpls()
        
        if impls:
            print(f"  Hook '{hook_name}' has {len(impls)} implementation(s)")
            for impl in impls:
                hook_count += 1
                print(f"    + Implementation from: {impl.plugin_name}")
                print(f"      Function: {impl.function.__name__}")
    
    # Print summary
    if hook_count > 0:
        print(f"\nSuccess! Found {hook_count} hook implementations in total")
    else:
        print(f"\nWarning! No hook implementations found")
        print("This may indicate that the hookimpl decorator is not properly applied or recognized")
        print("Make sure the decorator is imported correctly and applied to methods")
        
        # Additional debugging - check if the plugin is properly registered
        print("\nDebugging plugin registration:")
        print(f"Registered plugins: {PM.list_name_plugin()}")
        print(f"Plugin manager hook callers: {PM.hook.__dict__.keys()}")
    
    print("=== HOOK VERIFICATION COMPLETE ====")
    return hook_count


