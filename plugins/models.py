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
    entry_point = models.CharField(max_length=100, default='main.py')
    plugin_class = models.CharField(max_length=100, blank=True, null=True, help_text="Name of the plugin class to instantiate")
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
