from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from .models import (
    Lead,
    LeadField,
    LeadCommunication,
    WebhookEndpoint,
    WebhookLog
)


class LeadFieldInline(admin.TabularInline):
    model = LeadField
    extra = 0
    readonly_fields = ('created_at', 'updated_at')
    fields = ('field', 'value', 'created_at', 'updated_at')
    can_delete = True


class LeadCommunicationInline(admin.TabularInline):
    model = LeadCommunication
    extra = 0
    readonly_fields = ('created_at', 'updated_at', 'external_id')
    fields = ('direction', 'comm_type', 'content', 'status', 'created_at')
    can_delete = False
    max_num = 10  # Limit the number of communications shown
    ordering = ('-created_at',)


@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    list_display = ('get_full_name', 'business', 'email', 'phone', 'status', 'source', 'created_at', 'last_contacted')
    list_filter = ('business', 'status', 'source', 'created_at')
    search_fields = ('first_name', 'last_name', 'email', 'phone')
    readonly_fields = ('id', 'created_at', 'updated_at')
    inlines = [LeadFieldInline, LeadCommunicationInline]
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('id', 'business', 'first_name', 'last_name', 'email', 'phone')
        }),
        ('Status Information', {
            'fields': ('status', 'source', 'notes', 'last_contacted')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_full_name(self, obj):
        return obj.get_full_name()
    get_full_name.short_description = 'Name'
    
    def save_model(self, request, obj, form, change):
        if change and 'status' in form.changed_data and obj.status == 'contacted':
            obj.mark_contacted()
        else:
            super().save_model(request, obj, form, change)


@admin.register(LeadCommunication)
class LeadCommunicationAdmin(admin.ModelAdmin):
    list_display = ('lead', 'direction', 'comm_type', 'status', 'created_at', 'content_preview')
    list_filter = ('direction', 'comm_type', 'status', 'created_at')
    search_fields = ('lead__first_name', 'lead__last_name', 'lead__email', 'content')
    readonly_fields = ('id', 'created_at', 'updated_at')
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Communication Details', {
            'fields': ('id', 'lead', 'direction', 'comm_type', 'status')
        }),
        ('Content', {
            'fields': ('content',),
            'classes': ('wide',)
        }),
        ('External Service', {
            'fields': ('external_id', 'metadata'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def content_preview(self, obj):
        if len(obj.content) > 50:
            return f"{obj.content[:50]}..."
        return obj.content
    content_preview.short_description = 'Content'


class WebhookLogInline(admin.TabularInline):
    model = WebhookLog
    extra = 0
    readonly_fields = ('created_at', 'status_code', 'ip_address', 'lead_link')
    fields = ('created_at', 'status_code', 'ip_address', 'lead_link')
    can_delete = False
    max_num = 10
    ordering = ('-created_at',)
    
    def lead_link(self, obj):
        if obj.lead:
            url = reverse('admin:leads_lead_change', args=[obj.lead.id])
            return format_html('<a href="{}">View Lead</a>', url)
        return '-'
    lead_link.short_description = 'Lead'


@admin.register(WebhookEndpoint)
class WebhookEndpointAdmin(admin.ModelAdmin):
    list_display = ('name', 'business', 'is_active', 'created_at')
    list_filter = ('business', 'is_active', 'created_at')
    search_fields = ('name', 'business__name')
    readonly_fields = ('created_at', 'updated_at')
    inlines = [WebhookLogInline]
    
    fieldsets = (
        ('Endpoint Details', {
            'fields': ('business', 'name', 'slug', 'is_active')
        }),
        ('Security', {
            'fields': ('secret_key',),
            'classes': ('collapse',)
        }),
        ('Field Mapping', {
            'fields': ('field_mapping',),
            'description': 'JSON mapping of webhook fields to lead fields'
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(WebhookLog)
class WebhookLogAdmin(admin.ModelAdmin):
    list_display = ('endpoint', 'status_code', 'ip_address', 'created_at', 'lead_link')
    list_filter = ('endpoint', 'status_code', 'created_at')
    search_fields = ('endpoint__name', 'ip_address')
    readonly_fields = ('endpoint', 'request_data', 'response_data', 'ip_address', 'user_agent', 'status_code', 'lead', 'created_at')
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Log Details', {
            'fields': ('endpoint', 'status_code', 'ip_address', 'user_agent', 'created_at')
        }),
        ('Lead', {
            'fields': ('lead',)
        }),
        ('Request Data', {
            'fields': ('request_data',),
            'classes': ('wide',)
        }),
        ('Response Data', {
            'fields': ('response_data',),
            'classes': ('wide',)
        }),
    )
    
    def lead_link(self, obj):
        if obj.lead:
            url = reverse('admin:leads_lead_change', args=[obj.lead.id])
            return format_html('<a href="{}">View Lead</a>', url)
        return '-'
    lead_link.short_description = 'Lead'
    
    def has_add_permission(self, request):
        return False
    
    def has_change_permission(self, request, obj=None):
        return False
