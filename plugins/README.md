# Services AI Plugin System

A modular, extensible plugin system for the Services AI platform based on the Pluggy framework.

## Overview

The Services AI Plugin System allows developers to extend the platform's functionality through custom plugins. Plugins can:

- Respond to system events (lead creation, booking changes, etc.)
- Add widgets to the dashboard
- Provide custom settings interfaces
- Export and analyze data
- Integrate with third-party services

## Plugin Structure

A valid plugin must be a Python package with the following structure:

```
plugin_name/
  ├── __init__.py        # Package initialization
  ├── main.py            # Plugin implementation with hook implementations
  └── manifest.json      # Plugin metadata and configuration
```

### manifest.json

The manifest file defines the plugin's metadata, required permissions, settings, and implemented hooks:

```json
{
    "name": "Plugin Name",
    "version": "1.0.0",
    "description": "Plugin description",
    "author": "Author Name",
    "email": "author@example.com",
    "entry_point": "main",
    "plugin_class": "PluginClassName",
    "requires_python": ">=3.8.0",
    "permissions": [
        {
            "name": "permission_name",
            "description": "Permission description"
        }
    ],
    "settings": [
        {
            "name": "setting_name",
            "type": "text|number|checkbox|select|textarea",
            "required": true|false,
            "default": "default value",
            "description": "Setting description",
            "options": [  // Only for type="select"
                {"value": "option1", "label": "Option 1"},
                {"value": "option2", "label": "Option 2"}
            ]
        }
    ],
    "hooks": [
        "plugin_installed",
        "plugin_uninstalled",
        "plugin_enabled",
        "plugin_disabled",
        "lead_created",
        "booking_created",
        "booking_updated",
        "dashboard_widget",
        "settings_page",
        "data_export"
    ]
}
```

### Plugin Implementation

Create a class in your main.py file that implements the hooks specified in the manifest. Use the `@hookimpl` decorator to mark methods as hook implementations:

```python
from plugins.hooks import hookimpl

class YourPluginClass:
    @hookimpl
    def lead_created(self, lead, context):
        """Called when a new lead is created"""
        # Process the lead
        return {"status": "success", "message": "Lead processed"}
    
    @hookimpl
    def dashboard_widget(self, plugin_id, context):
        """Provides HTML content for dashboard widget"""
        # Return HTML for dashboard widget
        return "<div class='card'>Your widget content</div>"
```

## Available Hooks

### System Events

- `plugin_installed(plugin_id, plugin_info)`: Called when the plugin is installed
- `plugin_uninstalled(plugin_id)`: Called when the plugin is uninstalled
- `plugin_enabled(plugin_id)`: Called when the plugin is enabled
- `plugin_disabled(plugin_id)`: Called when the plugin is disabled

### Business Events

- `lead_created(lead, context)`: Called when a new lead is created
- `booking_created(booking, context)`: Called when a new booking is created
- `booking_updated(booking, context)`: Called when a booking is updated

### UI Extensions

- `dashboard_widget(plugin_id, context)`: Provides HTML content for dashboard widget
- `settings_page(plugin_id, context)`: Provides HTML content for plugin settings page

### Data Operations

- `data_export(export_type, start_date, end_date, context)`: Provides data for export

## Hook Context

Each hook receives a context dictionary with relevant information:

```python
context = {
    'request': request,           # The current HTTP request (if applicable)
    'user': user,                 # The current user (if applicable)
    'plugin': plugin              # The Plugin model instance
}
```

## Permissions

Plugins must declare permissions they require in the manifest. Permissions are disabled by default when a plugin is installed and must be explicitly enabled by an administrator.

### Standard Permissions

- `lead_access`: Access to lead data
- `booking_access`: Access to booking data
- `dashboard_widget`: Display widget on dashboard
- `data_export`: Export data from the system

## Settings

Plugins can define settings in their manifest file. Settings are stored in the database and can be accessed within hook implementations.

### Setting Types

- `text`: Single-line text input
- `textarea`: Multi-line text input
- `number`: Numeric input
- `checkbox`: Boolean checkbox
- `select`: Dropdown selection with options

## Best Practices

### Security

- Never store sensitive information (API keys, passwords) in plain text
- Validate all user input
- Use proper error handling
- Follow the principle of least privilege when requesting permissions

### Performance

- Keep hook implementations lightweight
- For long-running tasks, use asynchronous processing
- Cache results when appropriate to avoid redundant processing

### UI Integration

- Use Bootstrap 5 classes for consistent styling
- Make widgets responsive
- Keep dashboard widgets focused and compact
- Follow accessibility guidelines

## Submission and Review

Plugins must be reviewed before being published to the Services AI plugin directory. During review, plugins are checked for:

- Code quality and security
- Adherence to platform guidelines
- Documentation quality
- Performance impact

## Plugin Lifecycle

1. **Development**: Create plugin following the structure above
2. **Packaging**: Package as a ZIP file with all required files
3. **Installation**: Upload through the plugin management interface
4. **Configuration**: Configure permissions and settings
5. **Usage**: Enable and use the plugin
6. **Updates**: Upload new versions as needed
7. **Uninstallation**: Remove when no longer needed

## Example

See the `sample_plugin` directory for a complete example plugin implementation.
