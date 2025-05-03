"""
Signal handlers for the leads app.
"""

from django.db.models.signals import post_save
from django.dispatch import receiver
import logging

from .models import Lead
from core.email_notifications import send_lead_notification

logger = logging.getLogger(__name__)

@receiver(post_save, sender=Lead)
def lead_post_save(sender, instance, created, **kwargs):
    """
    Signal handler for when a lead is saved.
    Sends email notifications when a new lead is created.
    """
    if created:
        logger.info(f"New lead created: {instance.id} - {instance.get_full_name()}")
        
        # Send email notifications asynchronously
        try:
            from django_q.tasks import async_task
            async_task('core.email_notifications.send_lead_notification', instance.id)
            logger.info(f"Queued email notifications for lead: {instance.id}")
        except ImportError:
            # If django_q is not available, send emails synchronously
            business_email_sent, lead_email_sent = send_lead_notification(instance.id)
            logger.info(f"Email notifications for lead {instance.id}: Business: {business_email_sent}, Lead: {lead_email_sent}")
