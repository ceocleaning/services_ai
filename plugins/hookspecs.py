from plugins.hooks import hookspec

class PluginHooks:
    """Hook specifications for the Services AI plugin system"""
    
    @hookspec
    def lead_created(self, lead, context):
        """Hook called when a new lead is created
        
        Args:
            lead: The lead instance that was created
            context: Dictionary containing context information including request and user
        """
    
    @hookspec
    def booking_created(self, booking, context):
        """Hook called when a new booking is created
        
        Args:
            booking: The booking instance that was created
            context: Dictionary containing context information including request and user
        """
    
    @hookspec
    def booking_updated(self, booking, previous_state, context):
        """Hook called when a booking is updated
        
        Args:
            booking: The booking instance that was updated
            previous_state: Dictionary containing the previous state of the booking
            context: Dictionary containing context information including request and user
        """
    
    @hookspec
    def dashboard_widget(self, plugin_id, context):
        """Hook called when dashboard widgets are rendered
        
        Args:
            plugin_id: ID of the plugin
            context: Dictionary containing context information including request and user
        """
        
    @hookspec
    def plugin_installed(self, plugin_id, plugin_info):
        """Hook called when the plugin is installed
        
        Args:
            plugin_id: ID of the installed plugin
            plugin_info: Dictionary containing plugin information
        """
    
    @hookspec
    def plugin_uninstalled(self, plugin_id):
        """Hook called when the plugin is uninstalled
        
        Args:
            plugin_id: ID of the uninstalled plugin
        """
        
    @hookspec
    def data_export(self, export_type, start_date, end_date, context):
        """Hook called when data is exported
        
        Args:
            export_type: Type of data to export (leads, bookings, etc.)
            start_date: Start date for data range
            end_date: End date for data range
            context: Dictionary containing context information including request and user
            
        Returns:
            List of dictionaries containing exported data
        """
    
    @hookspec
    def settings_page(self, plugin_id, context):
        """Hook to render custom settings page
        
        Args:
            plugin_id: ID of the plugin
            context: Dictionary containing context information including request and user
            
        Returns:
            HTML string for the settings page
        """
