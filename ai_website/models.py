from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.text import slugify
import os


class GeneratedWebsite(models.Model):
    """
    Model to store AI-generated websites for users
    Each user can have one active website accessible at domain.com/<business-slug>/
    """
    user = models.OneToOneField(
        User, 
        on_delete=models.CASCADE, 
        related_name='generated_website',
        help_text="User who owns this website"
    )
    business_name = models.CharField(
        max_length=255,
        help_text="Business name used for website generation"
    )
    business_slug = models.SlugField(
        max_length=255,
        unique=True,
        help_text="URL-friendly slug generated from business name"
    )
    ai_prompt = models.TextField(
        help_text="User's custom prompt for AI website generation"
    )
    html_file_path = models.CharField(
        max_length=500,
        help_text="Path to the generated HTML file in media directory"
    )
    is_published = models.BooleanField(
        default=True,
        help_text="Whether the website is publicly accessible"
    )
    view_count = models.IntegerField(
        default=0,
        help_text="Number of times the website has been viewed"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="When the website was first generated"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text="When the website was last regenerated"
    )
    
    class Meta:
        verbose_name = "Generated Website"
        verbose_name_plural = "Generated Websites"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.business_name} ({self.business_slug})"
    
    def save(self, *args, **kwargs):
        """Auto-generate slug from business name if not provided"""
        if not self.business_slug:
            base_slug = slugify(self.business_name)
            slug = base_slug
            counter = 1
            
            # Ensure unique slug
            while GeneratedWebsite.objects.filter(business_slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            
            self.business_slug = slug
        
        super().save(*args, **kwargs)
    
    def get_public_url(self):
        """Return the public URL for this website"""
        return f"/{self.business_slug}/"
    
    def get_file_path(self):
        """Return the full file path for the HTML file"""
        from django.conf import settings
        return os.path.join(settings.MEDIA_ROOT, self.html_file_path)
    
    def increment_view_count(self):
        """Increment the view counter"""
        self.view_count += 1
        self.save(update_fields=['view_count'])


class WebsiteGenerationSession(models.Model):
    """
    Track individual generation sessions and conversation history
    Similar to ChatGPT conversation threads
    """
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    )
    
    website = models.ForeignKey(
        GeneratedWebsite,
        on_delete=models.CASCADE,
        related_name='generation_sessions',
        help_text="The website this session belongs to"
    )
    user_prompt = models.TextField(
        help_text="User's prompt/request for this generation"
    )
    ai_response = models.TextField(
        blank=True,
        null=True,
        help_text="AI's response or status message"
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',
        help_text="Current status of the generation"
    )
    progress_percentage = models.IntegerField(
        default=0,
        help_text="Generation progress (0-100)"
    )
    error_message = models.TextField(
        blank=True,
        null=True,
        help_text="Error message if generation failed"
    )
    tokens_used = models.IntegerField(
        default=0,
        help_text="Number of tokens used in this generation"
    )
    generation_time_seconds = models.FloatField(
        default=0.0,
        help_text="Time taken to generate (in seconds)"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="When this session was created"
    )
    completed_at = models.DateTimeField(
        blank=True,
        null=True,
        help_text="When this session was completed"
    )
    
    class Meta:
        verbose_name = "Website Generation Session"
        verbose_name_plural = "Website Generation Sessions"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.website.business_name} - {self.status} - {self.created_at.strftime('%Y-%m-%d %H:%M')}"
    
    def mark_processing(self):
        """Mark session as processing"""
        self.status = 'processing'
        self.progress_percentage = 10
        self.save(update_fields=['status', 'progress_percentage'])
    
    def update_progress(self, percentage, message=None):
        """Update generation progress"""
        self.progress_percentage = min(percentage, 100)
        if message:
            self.ai_response = message
        self.save(update_fields=['progress_percentage', 'ai_response'])
    
    def mark_completed(self, response_message, tokens=0, generation_time=0.0):
        """Mark session as completed"""
        from django.utils import timezone
        self.status = 'completed'
        self.progress_percentage = 100
        self.ai_response = response_message
        self.tokens_used = tokens
        self.generation_time_seconds = generation_time
        self.completed_at = timezone.now()
        self.save(update_fields=['status', 'progress_percentage', 'ai_response', 
                                'tokens_used', 'generation_time_seconds', 'completed_at'])
    
    def mark_failed(self, error_message):
        """Mark session as failed"""
        from django.utils import timezone
        self.status = 'failed'
        self.error_message = error_message
        self.ai_response = f"❌ Generation failed: {error_message}"
        self.completed_at = timezone.now()
        self.save(update_fields=['status', 'error_message', 'ai_response', 'completed_at'])
