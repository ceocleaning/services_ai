from django.contrib import admin

from .models import EmailVerification

@admin.register(EmailVerification)
class EmailVerificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'email', 'is_verified', 'otp_created_at', 'otp_expiry')
    list_filter = ('is_verified', 'otp_expiry')
    search_fields = ('email',)
    ordering = ('-otp_created_at',)
