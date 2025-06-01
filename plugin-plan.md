# Services AI Plugin System Architecture Plan

## Introduction

This document outlines the architecture and implementation plan for a Pluggy-based plugin system in the Services AI platform. The system will allow developers to create, upload, and manage plugins that can extend the functionality of the platform through dynamic function execution and HTML widget display.

## Core Components

### 1. Plugin System Architecture

We will implement a Pluggy-based plugin system with the following core components:

- **Plugin Manager**: Central component that discovers, loads, and manages plugins
- **Hook Specifications**: Defines the interfaces that plugins can implement
- **Hook Implementations**: Plugin-provided implementations of the hook specifications
- **Plugin Registry**: Stores metadata about installed plugins
- **Event System**: Notifies plugins about system events

### 2. Plugin Structure

Each plugin will be structured as a Python package with the following components:

```
plugin_name/
├── __init__.py           # Package initialization
├── main.py               # Hook implementations and main plugin code
├── manifest.json         # Plugin metadata and configuration
├── static/               # Static assets (CSS, JS, images)
│   └── ...
└── templates/            # HTML templates for widgets and UI components
    └── ...
```

#### 2.1 Manifest File

The `manifest.json` file will contain metadata about the plugin:

```json
{
  "name": "example-plugin",
  "version": "1.0.0",
  "description": "Example plugin for Services AI",
  "author": "Developer Name",
  "email": "dev@example.com",
  "is_pluggy_plugin": true,
  "entry_point": "main.py",
  "hook_specs": [
    "lead_created",
    "booking_created",
    "dashboard_widget"
  ],
  "permissions": [
    "read_leads",
    "read_bookings",
    "create_bookings"
  ],
  "settings": [
    {
      "name": "api_key",
      "type": "text",
      "label": "API Key",
      "required": true,
      "description": "Your API key for the service"
    },
    {
      "name": "auto_sync",
      "type": "checkbox",
      "label": "Auto Sync",
      "default": true,
      "description": "Automatically sync data"
    }
  ]
}
```

#### 2.2 Main Plugin File

The `main.py` file will contain the hook implementations:

```python
from services_ai.plugins import hookimpl

@hookimpl
def lead_created(lead):
    """Hook called when a new lead is created"""
    # Process the lead
    return {"status": "processed"}

@hookimpl
def booking_created(booking):
    """Hook called when a new booking is created"""
    # Process the booking
    return {"status": "processed"}

@hookimpl
def dashboard_widget(context):
    """Hook called when dashboard widgets are rendered"""
    # Return HTML content for the widget
    return {
        "html": "<div class='widget'>Widget Content</div>",
        "title": "Example Widget",
        "refresh_interval": 60  # seconds
    }
```

### 3. Hook Specifications

The system will define the following hook specifications:

```python
from services_ai.plugins import hookspec

@hookspec
def lead_created(lead):
    """Hook called when a new lead is created"""

@hookspec
def booking_created(booking):
    """Hook called when a new booking is created"""

@hookspec
def booking_updated(booking, previous_state):
    """Hook called when a booking is updated"""

@hookspec
def dashboard_widget(context):
    """Hook called when dashboard widgets are rendered"""

@hookspec
def plugin_installed():
    """Hook called when the plugin is installed"""

@hookspec
def plugin_uninstalled():
    """Hook called when the plugin is uninstalled"""

@hookspec
def data_export(data_type, filters):
    """Hook called when data is exported"""

@hookspec
def settings_page(plugin_id):
    """Hook to render custom settings page"""
```

## Implementation Plan

The implementation will follow these steps to create a complete Pluggy-based plugin system:

### 1. Core Plugin Framework

#### 1.1 Django App Structure

Create a dedicated Django app called `plugins` with the following structure:

```
plugins/
├── __init__.py
├── admin.py          # Admin interface for plugins
├── apps.py           # App configuration
├── events.py         # Event notification system
├── forms.py          # Forms for plugin upload and configuration
├── hookspecs.py      # Hook specifications
├── hooks.py          # Hook initialization and utilities
├── migrations/       # Database migrations
├── models.py         # Plugin and settings models
├── plugin_manager.py # Pluggy integration and plugin management
├── signals.py        # Django signals for event handling
├── templates/        # UI templates
├── tests.py          # Test suite
├── urls.py           # URL configurations
├── utils.py          # Utility functions
└── views.py          # View functions
```

#### 1.2 Plugin Models

Create database models to store plugin information:

```python
# plugins/models.py
from django.db import models
from django.contrib.auth.models import User

class Plugin(models.Model):
    """Model to store plugin information"""
    name = models.CharField(max_length=100)
    description = models.TextField()
    version = models.CharField(max_length=20)
    author = models.CharField(max_length=100)
    email = models.EmailField()
    enabled = models.BooleanField(default=True)
    installed_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    package_path = models.CharField(max_length=255)
    entry_point = models.CharField(max_length=100)
    manifest = models.JSONField()
    
    def __str__(self):
        return f"{self.name} ({self.version})"

class PluginPermission(models.Model):
    """Model to store plugin permissions"""
    plugin = models.ForeignKey(Plugin, on_delete=models.CASCADE, related_name='permissions')
    permission_name = models.CharField(max_length=100)
    enabled = models.BooleanField(default=False)
    
    class Meta:
        unique_together = ('plugin', 'permission_name')
    
    def __str__(self):
        return f"{self.plugin.name} - {self.permission_name}"

class PluginSetting(models.Model):
    """Model to store plugin settings"""
    plugin = models.ForeignKey(Plugin, on_delete=models.CASCADE, related_name='settings')
    setting_name = models.CharField(max_length=100)
    setting_value = models.TextField(blank=True, null=True)
    setting_type = models.CharField(max_length=20)  # text, number, checkbox, select
    
    class Meta:
        unique_together = ('plugin', 'setting_name')
    
    def __str__(self):
        return f"{self.plugin.name} - {self.setting_name}"
```

#### 1.3 Pluggy Integration

Integrate Pluggy for plugin management:

```python
# plugins/hooks.py
import pluggy

# Create hook specification and implementation markers
hookspec = pluggy.HookspecMarker("services_ai")
hookimpl = pluggy.HookimplMarker("services_ai")

# Export for use in other modules
__all__ = ['hookspec', 'hookimpl']
```

```python
# plugins/hookspecs.py
from plugins.hooks import hookspec

class PluginHooks:
    """Hook specifications for the Services AI plugin system"""
    
    @hookspec
    def lead_created(self, lead):
        """Hook called when a new lead is created"""
    
    @hookspec
    def booking_created(self, booking):
        """Hook called when a new booking is created"""
    
    @hookspec
    def booking_updated(self, booking, previous_state):
        """Hook called when a booking is updated"""
    
    @hookspec
    def dashboard_widget(self, context):
        """Hook called when dashboard widgets are rendered"""
        
    @hookspec
    def plugin_installed(self):
        """Hook called when the plugin is installed"""
    
    @hookspec
    def plugin_uninstalled(self):
        """Hook called when the plugin is uninstalled"""
        
    @hookspec
    def data_export(self, data_type, filters):
        """Hook called when data is exported"""
    
    @hookspec
    def settings_page(self, plugin_id):
        """Hook to render custom settings page"""
```

```python
# plugins/plugin_manager.py
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
            # Add plugin directory to path
            plugin_dir = os.path.dirname(plugin.package_path)
            if plugin_dir not in sys.path:
                sys.path.insert(0, plugin_dir)
            
            # Load the entry point module
            module_path = os.path.join(plugin.package_path, plugin.entry_point)
            module_name = f"plugin_{plugin.id}"
            
            spec = importlib.util.spec_from_file_location(module_name, module_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            
            # Register the plugin with Pluggy
            self.manager.register(module)
            
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
        hook = getattr(self.manager.hook, hook_name, None)
        if hook:
            return hook(**kwargs)
        return []

# Create a singleton instance
plugin_manager = ServicesAIPluginManager()
```

### 2. Event Notification System

Implement an event system to notify plugins about system events:

```python
# plugins/events.py
from django.conf import settings
from django_q.tasks import async_task
from plugins.plugin_manager import plugin_manager

def notify_plugins(event_name, **kwargs):
    """Notify all plugins about an event"""
    try:
        return plugin_manager.call_hook(event_name, **kwargs)
    except Exception as e:
        print(f"Error notifying plugins about {event_name}: {str(e)}")
        return []

def notify_plugins_async(event_name, **kwargs):
    """Notify all plugins about an event asynchronously"""
    async_task("plugins.events.notify_plugins", event_name, **kwargs)

# Event-specific notification functions
def notify_lead_created(lead):
    """Notify plugins about a new lead"""
    return notify_plugins('lead_created', lead=lead)

def notify_booking_created(booking):
    """Notify plugins about a new booking"""
    return notify_plugins('booking_created', booking=booking)

def notify_booking_updated(booking, previous_state):
    """Notify plugins about an updated booking"""
    return notify_plugins('booking_updated', booking=booking, previous_state=previous_state)
```

### 3. Forms

Create forms for plugin management:

```python
# plugins/forms.py
from django import forms
from plugins.models import Plugin, PluginSetting

class PluginUploadForm(forms.Form):
    """Form for uploading a plugin"""
    plugin_file = forms.FileField(help_text="Upload a ZIP file containing the plugin")

class PluginSettingForm(forms.ModelForm):
    """Form for plugin settings"""
    class Meta:
        model = PluginSetting
        fields = ['setting_value']
    
    def __init__(self, *args, **kwargs):
        setting_type = kwargs.pop('setting_type', None)
        super().__init__(*args, **kwargs)
        
        # Customize the field based on setting type
        if setting_type == 'checkbox':
            self.fields['setting_value'] = forms.BooleanField(required=False)
        elif setting_type == 'number':
            self.fields['setting_value'] = forms.IntegerField()
        elif setting_type == 'select':
            choices = kwargs.get('choices', [])
            self.fields['setting_value'] = forms.ChoiceField(choices=choices)
```

### 4. Signal Handlers

Implement signal handlers to trigger plugin events:

```python
# plugins/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver

from leads.models import Lead
from bookings.models import Booking
from plugins.events import notify_lead_created, notify_booking_created, notify_booking_updated

@receiver(post_save, sender=Lead)
def handle_lead_created(sender, instance, created, **kwargs):
    """Handle lead creation event"""
    if created:
        notify_lead_created(instance)

@receiver(post_save, sender=Booking)
def handle_booking_saved(sender, instance, created, **kwargs):
    """Handle booking creation and update events"""
    if created:
        notify_booking_created(instance)
    else:
        # For simplicity, we're not tracking the previous state here
        # In a real implementation, you'd need to store the previous state
        notify_booking_updated(instance, {})
```

### 5. App Configuration

Configure the app to connect signals:

```python
# plugins/apps.py
from django.apps import AppConfig

class PluginsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'plugins'
    
    def ready(self):
        # Import signal handlers
        import plugins.signals
        
        # Load enabled plugins
        from plugins.plugin_manager import plugin_manager
        plugin_manager.discover_plugins()
```

### 6. Template Tags

Create custom template tags for accessing plugin settings:

```python
# plugins/templatetags/__init__.py
# Empty file to make the directory a Python package
```

```python
# plugins/templatetags/plugin_tags.py
from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    """Get an item from a dictionary using bracket notation"""
    return dictionary.get(key)

@register.inclusion_tag('plugins/widgets.html')
def render_dashboard_widgets(user):
    """Render dashboard widgets from all plugins"""
    from plugins.plugin_manager import plugin_manager
    
    widgets = plugin_manager.call_hook('dashboard_widget', context={'user': user})
    return {'widgets': widgets}
```

```html
<!-- templates/plugins/widgets.html -->
{% for widget in widgets %}
<div class="card mb-4">
    <div class="card-header">
        {{ widget.title }}
    </div>
    <div class="card-body">
        {{ widget.html|safe }}
    </div>
</div>
{% endfor %}
```

### 7. Views and URLs

Implement views for plugin management and configure URLs:

```python
# plugins/views.py (partial)
import os
import json
import zipfile
import shutil
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
from django.http import HttpResponse, JsonResponse

from plugins.models import Plugin, PluginPermission, PluginSetting
from plugins.forms import PluginUploadForm
from plugins.plugin_manager import plugin_manager

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
    try:
        custom_settings_page = plugin_manager.call_hook('settings_page', plugin_id=plugin_id)
    except Exception:
        pass
    
    return render(request, 'plugins/detail.html', {
        'plugin': plugin,
        'permissions': permissions,
        'settings': settings,
        'custom_settings_page': custom_settings_page[0] if custom_settings_page else None
    })

@login_required
def upload_plugin(request):
    """View to upload a new plugin"""
    if request.method == 'POST':
        form = PluginUploadForm(request.POST, request.FILES)
        if form.is_valid():
            plugin_file = request.FILES['plugin_file']
            
            # Process the uploaded plugin (ZIP file)
            # Implementation details omitted for brevity
            # See the full implementation in the complete code
            
            messages.success(request, f'Plugin installed successfully')
            return redirect('plugin_list')
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
    
    return redirect('plugin_detail', plugin_id=plugin.id)

@login_required
def toggle_permission(request, plugin_id, permission_id):
    """Enable or disable a plugin permission"""
    permission = get_object_or_404(PluginPermission, id=permission_id, plugin_id=plugin_id)
    permission.enabled = not permission.enabled
    permission.save()
    
    return redirect('plugin_detail', plugin_id=plugin_id)

@login_required
def uninstall_plugin(request, plugin_id):
    """Uninstall a plugin"""
    plugin = get_object_or_404(Plugin, id=plugin_id)
    
    if request.method == 'POST':
        # Call plugin_uninstalled hook
        plugin_manager.call_hook('plugin_uninstalled')
        
        # Unload the plugin
        plugin_manager.unload_plugin(plugin.id)
        
        # Remove plugin directory
        if os.path.exists(plugin.package_path):
            shutil.rmtree(plugin.package_path)
        
        # Delete plugin from database
        plugin_name = plugin.name
        plugin.delete()
        
        messages.success(request, f'Plugin {plugin_name} uninstalled successfully')
        return redirect('plugin_list')
    
    return render(request, 'plugins/confirm_uninstall.html', {'plugin': plugin})
```

```python
# plugins/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.plugin_list, name='plugin_list'),
    path('upload/', views.upload_plugin, name='upload_plugin'),
    path('<int:plugin_id>/', views.plugin_detail, name='plugin_detail'),
    path('<int:plugin_id>/toggle/', views.toggle_plugin, name='toggle_plugin'),
    path('<int:plugin_id>/permission/<int:permission_id>/toggle/', views.toggle_permission, name='toggle_permission'),
    path('<int:plugin_id>/settings/', views.update_settings, name='update_settings'),
    path('<int:plugin_id>/uninstall/', views.uninstall_plugin, name='uninstall_plugin'),
    path('dashboard/widgets/', views.get_dashboard_widgets, name='get_dashboard_widgets'),
]
```

### 8. Templates

#### 8.1 Plugin Detail Template

```html
<!-- templates/plugins/detail.html -->
{% extends "base.html" %}
{% load plugin_tags %}

{% block content %}
<div class="container">
    <div class="row mb-4">
        <div class="col">
            <h1>{{ plugin.name }}</h1>
            <p class="lead">{{ plugin.description }}</p>
        </div>
        <div class="col text-end">
            <a href="{% url 'plugin_list' %}" class="btn btn-secondary">Back to Plugins</a>
            <form method="post" action="{% url 'toggle_plugin' plugin.id %}" class="d-inline">
                {% csrf_token %}
                <button type="submit" class="btn {% if plugin.enabled %}btn-warning{% else %}btn-success{% endif %}">
                    {% if plugin.enabled %}Disable{% else %}Enable{% endif %}
                </button>
            </form>
            <button type="button" class="btn btn-danger" data-bs-toggle="modal" data-bs-target="#uninstallModal">
                Uninstall
            </button>
        </div>
    </div>
    
    {% if messages %}
    <div class="row">
        <div class="col">
            {% for message in messages %}
            <div class="alert alert-{{ message.tags }}">{{ message }}</div>
            {% endfor %}
        </div>
    </div>
    {% endif %}
    
    <div class="row">
        <div class="col-md-4">
            <div class="card mb-4">
                <div class="card-header">
                    Plugin Information
                </div>
                <div class="card-body">
                    <p><strong>Version:</strong> {{ plugin.version }}</p>
                    <p><strong>Author:</strong> {{ plugin.author }}</p>
                    <p><strong>Email:</strong> {{ plugin.email }}</p>
                    <p><strong>Status:</strong> 
                        <span class="badge {% if plugin.enabled %}bg-success{% else %}bg-danger{% endif %}">
                            {% if plugin.enabled %}Enabled{% else %}Disabled{% endif %}
                        </span>
                    </p>
                    <p><strong>Installed:</strong> {{ plugin.installed_at|date:"M d, Y" }}</p>
                    <p><strong>Updated:</strong> {{ plugin.updated_at|date:"M d, Y" }}</p>
                </div>
            </div>
            
            <div class="card mb-4">
                <div class="card-header">
                    Permissions
                </div>
                <div class="card-body">
                    {% if permissions %}
                    <ul class="list-group">
                        {% for permission in permissions %}
                        <li class="list-group-item d-flex justify-content-between align-items-center">
                            {{ permission.permission_name }}
                            <form method="post" action="{% url 'toggle_permission' plugin.id permission.id %}">
                                {% csrf_token %}
                                <button type="submit" class="btn btn-sm {% if permission.enabled %}btn-success{% else %}btn-secondary{% endif %}">
                                    {% if permission.enabled %}Enabled{% else %}Disabled{% endif %}
                                </button>
                            </form>
                        </li>
                        {% endfor %}
                    </ul>
                    {% else %}
                    <p>No permissions required.</p>
                    {% endif %}
                </div>
            </div>
        </div>
        
        <div class="col-md-8">
            {% if custom_settings_page %}
            <div class="card mb-4">
                <div class="card-header">
                    Custom Settings
                </div>
                <div class="card-body">
                    {{ custom_settings_page|safe }}
                </div>
            </div>
            {% endif %}
            
            {% if settings %}
            <div class="card mb-4">
                <div class="card-header">
                    Settings
                </div>
                <div class="card-body">
                    <form method="post" action="{% url 'update_settings' plugin.id %}">
                        {% csrf_token %}
                        {% for setting in settings %}
                        <div class="mb-3">
                            <label for="{{ setting.setting_name }}" class="form-label">
                                {{ setting.setting_name|title }}
                            </label>
                            
                            {% if setting.setting_type == 'checkbox' %}
                            <div class="form-check">
                                <input type="checkbox" class="form-check-input" id="{{ setting.setting_name }}" 
                                       name="{{ setting.setting_name }}" value="true"
                                       {% if setting.setting_value == 'true' %}checked{% endif %}>
                            </div>
                            {% elif setting.setting_type == 'textarea' %}
                            <textarea class="form-control" id="{{ setting.setting_name }}" 
                                      name="{{ setting.setting_name }}" rows="3">{{ setting.setting_value }}</textarea>
                            {% elif setting.setting_type == 'select' %}
                            <select class="form-select" id="{{ setting.setting_name }}" name="{{ setting.setting_name }}">
                                {% for option in plugin.manifest.settings|get_item:forloop.counter0|get_item:'options' %}
                                <option value="{{ option.value }}" 
                                        {% if setting.setting_value == option.value %}selected{% endif %}>
                                    {{ option.label }}
                                </option>
                                {% endfor %}
                            </select>
                            {% else %}
                            <input type="{{ setting.setting_type }}" class="form-control" id="{{ setting.setting_name }}" 
                                   name="{{ setting.setting_name }}" value="{{ setting.setting_value }}">
                            {% endif %}
                            
                            {% if plugin.manifest.settings|get_item:forloop.counter0|get_item:'description' %}
                            <div class="form-text">
                                {{ plugin.manifest.settings|get_item:forloop.counter0|get_item:'description' }}
                            </div>
                            {% endif %}
                        </div>
                        {% endfor %}
                        
                        <button type="submit" class="btn btn-primary">Save Settings</button>
                    </form>
                </div>
            </div>
            {% endif %}
        </div>
    </div>
</div>

<!-- Uninstall Confirmation Modal -->
<div class="modal fade" id="uninstallModal" tabindex="-1" aria-labelledby="uninstallModalLabel" aria-hidden="true">
    <div class="modal-dialog">
        <div class="modal-content">
            <div class="modal-header">
                <h5 class="modal-title" id="uninstallModalLabel">Confirm Uninstallation</h5>
                <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
            </div>
            <div class="modal-body">
                Are you sure you want to uninstall <strong>{{ plugin.name }}</strong>? This action cannot be undone.
            </div>
            <div class="modal-footer">
                <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancel</button>
                <form method="post" action="{% url 'uninstall_plugin' plugin.id %}">
                    {% csrf_token %}
                    <button type="submit" class="btn btn-danger">Uninstall</button>
                </form>
            </div>
        </div>
    </div>
</div>
{% endblock %}
```

## Step-by-Step Implementation Guide

Follow these steps to implement the Pluggy-based plugin system for the Services AI platform:

### Step 1: Set Up Project Dependencies

1. Install required packages:
   ```bash
   pip install pluggy django-q
   ```

2. Add the plugins app to your Django settings:
   ```python
   # settings.py
   INSTALLED_APPS = [
       # Existing apps
       'plugins',
       'django_q',
   ]
   ```

3. Configure Django Q for asynchronous task processing:
   ```python
   # settings.py
   Q_CLUSTER = {
       'name': 'services_ai',
       'workers': 4,
       'recycle': 500,
       'timeout': 60,
       'compress': True,
       'save_limit': 250,
       'queue_limit': 500,
       'cpu_affinity': 1,
       'label': 'Django Q',
       'redis': {
           'host': '127.0.0.1',
           'port': 6379,
           'db': 0,
       }
   }
   ```

### Step 2: Create the Plugins App

1. Create a new Django app:
   ```bash
   python manage.py startapp plugins
   ```

2. Create the basic directory structure:
   ```bash
   mkdir -p plugins/templatetags
   mkdir -p plugins/templates/plugins
   ```

### Step 3: Implement Core Plugin System

1. Create the hook specifications and markers
2. Implement the plugin manager
3. Set up event notification system
4. Create database models
5. Implement signal handlers

### Step 4: Implement Plugin Management UI

1. Create forms for plugin upload and settings
2. Implement views for plugin listing, detail, upload, and management
3. Create URL configurations
4. Develop templates for the plugin management interface

### Step 5: Create Plugin Integration Points

1. Implement dashboard widget integration
2. Create event handlers for leads and bookings
3. Set up data export hooks
4. Implement settings page hooks

### Step 6: Create Sample Plugins

1. Create a basic plugin structure template
2. Implement a sample lead management plugin
3. Implement a sample dashboard widget plugin
4. Implement a sample CRM integration plugin

### Step 7: Write Documentation

1. Create developer documentation for plugin creation
2. Document plugin structure requirements
3. Document available hooks and their usage
4. Create a user guide for plugin management

## Plugin Development Guide

This section provides guidelines for developers creating plugins for the Services AI platform.

### Plugin Structure

A plugin must adhere to the following structure:

```
plugin_name/
├── __init__.py           # Package initialization
├── main.py               # Hook implementations and main plugin code
├── manifest.json         # Plugin metadata and configuration
├── static/               # Static assets (CSS, JS, images)
│   └── ...
└── templates/            # HTML templates for widgets and UI components
    └── ...
```

### Manifest File Requirements

The `manifest.json` file must include the following fields:

- `name`: Plugin name (required)
- `version`: Plugin version (required)
- `description`: Plugin description (required)
- `author`: Plugin author name (required)
- `email`: Contact email (required)
- `is_pluggy_plugin`: Set to `true` to indicate Pluggy compatibility (required)
- `entry_point`: Main plugin file (default: `main.py`)
- `hook_specs`: Array of implemented hook specifications
- `permissions`: Array of required permissions
- `settings`: Array of configurable settings

### Available Hooks

Developers can implement any of the following hooks:

- `lead_created(lead)`: Called when a new lead is created
- `booking_created(booking)`: Called when a new booking is created
- `booking_updated(booking, previous_state)`: Called when a booking is updated
- `dashboard_widget(context)`: Called when dashboard widgets are rendered
- `plugin_installed()`: Called when the plugin is installed
- `plugin_uninstalled()`: Called when the plugin is uninstalled
- `data_export(data_type, filters)`: Called when data is exported
- `settings_page(plugin_id)`: Called to render a custom settings page

### Best Practices

1. **Security**: Never access user data without appropriate permissions
2. **Performance**: Keep hook implementations lightweight, especially for synchronous hooks
3. **Dependency Management**: Include all dependencies in the plugin package
4. **Error Handling**: Implement proper error handling to prevent plugin failures from affecting the main application
5. **Documentation**: Include documentation for your plugin's functionality and configuration options

## Conclusion

This Pluggy-based plugin system provides a flexible and maintainable way to extend the Services AI platform's functionality. The system follows the modular architecture principles defined in the user guidelines with proper separation of concerns and comprehensive error handling. The event-driven approach allows plugins to respond to system events without modifying core application code.