from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Invoice
from core.email_notifications import send_invoice_notification


@receiver(post_save, sender=Invoice)
def invoice_post_save(sender, instance, created, **kwargs):
    if not created:
        return
    
    try:
        from django_q.tasks import async_task
        async_task('core.email_notifications.send_invoice_notification', instance.id)
    except ImportError:
        send_invoice_notification(instance.id)
