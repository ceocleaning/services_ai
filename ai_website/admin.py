from django.contrib import admin
from .models import GeneratedWebsite, WebsiteGenerationSession


@admin.register(GeneratedWebsite)
class GeneratedWebsiteAdmin(admin.ModelAdmin):
    """
    Admin interface for Generated Websites
    """
    list_display = ['user', 'business_name', 'is_published', 'view_count', 'created_at', 'updated_at']
    list_filter = ['is_published', 'created_at', 'updated_at']
    search_fields = ['user__username', 'user__email', 'business_name', 'ai_prompt']
    readonly_fields = ['created_at', 'updated_at', 'view_count']
    
    fieldsets = (
        ('User Information', {
            'fields': ('user',)
        }),
        ('Website Details', {
            'fields': ('business_name', 'ai_prompt', 'html_file_path')
        }),
        ('Publishing', {
            'fields': ('is_published',)
        }),
        ('Statistics', {
            'fields': ('view_count', 'created_at', 'updated_at')
        }),
    )
    



@admin.register(WebsiteGenerationSession)
class WebsiteGenerationSessionAdmin(admin.ModelAdmin):
    """
    Admin interface for Website Generation Sessions
    """
    list_display = ['website', 'status', 'progress_percentage', 'tokens_used', 
                    'generation_time_seconds', 'created_at', 'completed_at']
    list_filter = ['status', 'created_at', 'completed_at']
    search_fields = ['website__business_name', 'user_prompt', 'ai_response']
    readonly_fields = ['created_at', 'completed_at', 'tokens_used', 'generation_time_seconds']
    
    fieldsets = (
        ('Session Information', {
            'fields': ('website', 'status', 'progress_percentage')
        }),
        ('Conversation', {
            'fields': ('user_prompt', 'ai_response')
        }),
        ('Metrics', {
            'fields': ('tokens_used', 'generation_time_seconds', 'created_at', 'completed_at')
        }),
        ('Error Details', {
            'fields': ('error_message',),
            'classes': ('collapse',)
        }),
    )
    
    
