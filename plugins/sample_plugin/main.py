"""
Sample Plugin for Services AI
This demonstrates how to implement hooks for the Services AI plugin system.
"""
from plugins.hooks import hookimpl
import json
import datetime

class SamplePlugin:
    """Sample plugin implementation for Services AI"""
    
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
    def lead_created(self, lead, context):
        """Called when a new lead is created"""
        print(f"New lead created: {lead.name} (ID: {lead.id})")
        return {"status": "success", "message": f"Sample plugin processed new lead: {lead.name}"}
    
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
