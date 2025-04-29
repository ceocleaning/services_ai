from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
import uuid

class Industry(models.Model):
    """
    Represents different business domains (cleaning, roofing, salons, dental, etc.)
    """
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=120, unique=True, blank=True)
    description = models.TextField(blank=True, null=True)
    icon = models.CharField(max_length=50, blank=True, null=True, help_text="CSS class for icon")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Industry"
        verbose_name_plural = "Industries"
        ordering = ['name']

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Business(models.Model):
    """
    Represents a business entity that belongs to a specific industry.
    Each business can have its own configuration and customization.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=150)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='business')
    industry = models.ForeignKey(Industry, on_delete=models.CASCADE, related_name='businesses')
    phone_number = models.CharField(max_length=20)
    email = models.EmailField()
    website = models.URLField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    zip_code = models.CharField(max_length=20, blank=True, null=True)
    logo = models.ImageField(upload_to='business_logos/', blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Business"
        verbose_name_plural = "Businesses"
        ordering = ['-created_at']

    def __str__(self):
        return self.name


FIELD_TYPES = (
    ('text', 'Text'),
    ('number', 'Number'),
    ('select', 'Select'),
    ('date', 'Date'),
    ('time', 'Time'),
    ('datetime', 'Date and Time'),
    ('boolean', 'Yes/No'),
    ('email', 'Email'),
    ('phone', 'Phone Number'),
    ('url', 'URL'),
    ('textarea', 'Text Area'),
)


class IndustryField(models.Model):
    """
    Dynamic fields tied to each industry (e.g., "square feet" for cleaning).
    These fields define the data that needs to be collected for each industry.
    """
    industry = models.ForeignKey(Industry, on_delete=models.CASCADE, related_name='fields')
    name = models.CharField(max_length=100)  # e.g., "Square Feet"
    slug = models.SlugField(max_length=120, blank=True)
    field_type = models.CharField(max_length=20, choices=FIELD_TYPES)
    options = models.JSONField(blank=True, null=True)  # used for select dropdowns
    placeholder = models.CharField(max_length=200, blank=True, null=True)
    help_text = models.CharField(max_length=255, blank=True, null=True)
    required = models.BooleanField(default=True)
    default_value = models.CharField(max_length=255, blank=True, null=True)
    validation_regex = models.CharField(max_length=255, blank=True, null=True)
    display_order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Industry Field"
        verbose_name_plural = "Industry Fields"
        ordering = ['display_order', 'name']
        unique_together = ['industry', 'slug']

    def __str__(self):
        return f"{self.industry.name} - {self.name}"
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class BusinessCustomField(models.Model):
    """
    Override or add more fields at a business level (optional).
    Allows businesses to customize their own fields beyond the industry defaults.
    """
    business = models.ForeignKey(Business, on_delete=models.CASCADE, related_name='custom_fields')
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=120, blank=True)
    field_type = models.CharField(max_length=20, choices=FIELD_TYPES)
    options = models.JSONField(blank=True, null=True)
    placeholder = models.CharField(max_length=200, blank=True, null=True)
    help_text = models.CharField(max_length=255, blank=True, null=True)
    required = models.BooleanField(default=True)
    default_value = models.CharField(max_length=255, blank=True, null=True)
    validation_regex = models.CharField(max_length=255, blank=True, null=True)
    display_order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Business Custom Field"
        verbose_name_plural = "Business Custom Fields"
        ordering = ['display_order', 'name']
        unique_together = ['business', 'slug']

    def __str__(self):
        return f"{self.business.name} - {self.name}"
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class IndustryPrompt(models.Model):
    """
    Industry-specific AI prompts for generating responses.
    """
    industry = models.ForeignKey(Industry, on_delete=models.CASCADE, related_name='prompts')
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    prompt_text = models.TextField()
    version = models.CharField(max_length=20, default='1.0')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Industry Prompt"
        verbose_name_plural = "Industry Prompts"
        ordering = ['-version', 'name']

    def __str__(self):
        return f"{self.industry.name} - {self.name} (v{self.version})"


class BusinessConfiguration(models.Model):
    """
    Business-specific configuration settings.
    """
    business = models.OneToOneField(Business, on_delete=models.CASCADE, related_name='configuration')
    webhook_secret = models.CharField(max_length=100, blank=True, null=True)
    lead_notification_email = models.EmailField(blank=True, null=True)
    sms_enabled = models.BooleanField(default=True)
    voice_enabled = models.BooleanField(default=True)
    twilio_phone_number = models.CharField(max_length=20, blank=True, null=True)
    initial_response_delay = models.PositiveIntegerField(default=5, help_text="Delay in minutes before first contact")
    follow_up_attempts = models.PositiveIntegerField(default=3)
    follow_up_interval = models.PositiveIntegerField(default=60, help_text="Interval in minutes between follow-ups")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Configuration for {self.business.name}"
