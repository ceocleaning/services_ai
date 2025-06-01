from django.contrib import admin
from .models import Plugin, PluginPermission, PluginSetting

class PluginPermissionInline(admin.TabularInline):
    model = PluginPermission
    extra = 1

class PluginSettingInline(admin.TabularInline):
    model = PluginSetting
    extra = 1

@admin.register(Plugin)
class PluginAdmin(admin.ModelAdmin):
    list_display = ('name', 'version', 'author', 'enabled', 'installed_at')
    list_filter = ('enabled',)
    search_fields = ('name', 'description', 'author')
    readonly_fields = ('installed_at', 'updated_at')
    inlines = [PluginPermissionInline, PluginSettingInline]
    fieldsets = (
        (None, {
            'fields': ('name', 'description', 'version', 'enabled')
        }),
        ('Author Information', {
            'fields': ('author', 'email')
        }),
        ('Plugin Details', {
            'fields': ('package_path', 'entry_point', 'manifest')
        }),
        ('Timestamps', {
            'fields': ('installed_at', 'updated_at')
        }),
    )

@admin.register(PluginPermission)
class PluginPermissionAdmin(admin.ModelAdmin):
    list_display = ('plugin', 'permission_name', 'enabled')
    list_filter = ('enabled', 'plugin')
    search_fields = ('permission_name', 'plugin__name')

@admin.register(PluginSetting)
class PluginSettingAdmin(admin.ModelAdmin):
    list_display = ('plugin', 'setting_name', 'setting_type')
    list_filter = ('setting_type', 'plugin')
    search_fields = ('setting_name', 'plugin__name')
