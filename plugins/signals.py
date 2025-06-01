from django.db.models.signals import post_save
from django.dispatch import receiver

# Import models - these should match your actual app structure
# Replace with your actual Lead and Booking model imports
try:
    from leads.models import Lead
    from bookings.models import Booking
except ImportError:
    # This allows the signals module to be imported even if these models don't exist yet
    # Useful during initial setup and migrations
    Lead = None
    Booking = None

from plugins.events import notify_lead_created_async, notify_booking_created_async, notify_booking_updated_async

# Only register the signals if the models are available
if Lead is not None:
    @receiver(post_save, sender=Lead)
    def handle_lead_created(sender, instance, created, **kwargs):
        """
        Handle lead creation event
        
        Args:
            sender: The model class
            instance: The actual instance being saved
            created: A boolean; True if a new record was created
        """
        if created:
            # Get the request from thread local storage if available
            request = getattr(instance, 'request', None)
            user = getattr(request, 'user', None) if request else None
            
            notify_lead_created_async(instance, request=request, user=user)
            print("Plugins notified about new lead: ", instance.id)

if Booking is not None:
    @receiver(post_save, sender=Booking)
    def handle_booking_saved(sender, instance, created, **kwargs):
        """
        Handle booking creation and update events
        
        Args:
            sender: The model class
            instance: The actual instance being saved
            created: A boolean; True if a new record was created
        """
        # Get the request from thread local storage if available
        request = getattr(instance, 'request', None)
        user = getattr(request, 'user', None) if request else None
        
        if created:
            notify_booking_created_async(instance, request=request, user=user)
            print("Plugins notified about new booking: ", instance.id)
        else:
            # For simplicity, we're not tracking the previous state here
            # In a real implementation, you'd need to store the previous state
            # This could be done using Django's pre_save signal or other methods
            notify_booking_updated_async(instance, {}, request=request, user=user)
            print("Plugins notified about updated booking: ", instance.id)
