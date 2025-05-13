
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Lead
from core.email_notifications import send_lead_notification
from .tasks import make_call_to_lead
from django_q.tasks import schedule
from django_q.models import Schedule
from django.utils import timezone
import datetime


@receiver(post_save, sender=Lead)
def lead_post_save(sender, instance, created, **kwargs):
    if created:
        try:
            from django_q.tasks import async_task
            async_task('core.email_notifications.send_lead_notification', instance.id)

            business_config = instance.business.businessconfiguration

            if business_config.call_enabled and business_config.initial_response_delay > 0:

                schedule(
                    'leads.tasks.make_call_to_lead',  
                    instance.id,  
                    schedule_type='O',
                    next_run=timezone.now() + datetime.timedelta(minutes=business_config.initial_response_delay),
                )
                print(f"Call scheduled for lead {instance.id} in {business_config.initial_response_delay} minutes")

          
        except ImportError:
            business_email_sent, lead_email_sent = send_lead_notification(instance.id)
           


