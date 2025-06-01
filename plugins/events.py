from django.conf import settings
from django_q.tasks import async_task
from plugins.plugin_manager import plugin_manager

def notify_plugins(event_name, **kwargs):
    """
    Notify all plugins about an event
    
    This function calls the appropriate hook in all registered plugins,
    passing the provided kwargs.
    
    Args:
        event_name: Name of the hook to call
        **kwargs: Arguments to pass to the hook
    
    Returns:
        List of results from all plugin hook implementations
    """
    try:
        result = plugin_manager.call_hook(event_name, **kwargs)
        print(f"HOOK CALLED: {event_name}, result: {result}")
        return result
    except Exception as e:
        print(f"Error notifying plugins about {event_name}: {str(e)}")
        return []

def notify_plugins_async(event_name, **kwargs):
    """
    Notify all plugins about an event asynchronously
    
    Args:
        event_name: Name of the hook to call
        **kwargs: Arguments to pass to the hook
    """
    notify_plugins(event_name, **kwargs)


# Event-specific notification functions
def notify_lead_created(lead, request=None, user=None):
    """
    Notify plugins about a new lead
    
    Args:
        lead: Lead instance that was created
        request: Current HTTP request (optional)
        user: Current user (optional)
    """
    context = {
        'request': request,
        'user': user
    }
    notify_plugins('lead_created', lead=lead, context=context)

def notify_lead_created_async(lead, request=None, user=None):
    """
    Notify plugins about a new lead asynchronously
    
    Args:
        lead: Lead instance that was created
        request: Current HTTP request (optional)
        user: Current user (optional)
    """
    context = {
        'request': request,
        'user': user
    }
    notify_plugins_async('lead_created', lead=lead, context=context)

def notify_booking_created(booking, request=None, user=None):
    """
    Notify plugins about a new booking
    
    Args:
        booking: Booking instance that was created
        request: Current HTTP request (optional)
        user: Current user (optional)
    """
    context = {
        'request': request,
        'user': user
    }
    notify_plugins('booking_created', booking=booking, context=context)

def notify_booking_created_async(booking, request=None, user=None):
    """
    Notify plugins about a new booking asynchronously
    
    Args:
        booking: Booking instance that was created
        request: Current HTTP request (optional)
        user: Current user (optional)
    """
    context = {
        'request': request,
        'user': user
    }
    notify_plugins_async('booking_created', booking=booking, context=context)

def notify_booking_updated(booking, previous_state, request=None, user=None):
    """
    Notify plugins about an updated booking
    
    Args:
        booking: Booking instance that was updated
        previous_state: Dictionary containing the previous state of the booking
        request: Current HTTP request (optional)
        user: Current user (optional)
    """
    context = {
        'request': request,
        'user': user
    }
    notify_plugins('booking_updated', booking=booking, previous_state=previous_state, context=context)

def notify_booking_updated_async(booking, previous_state, request=None, user=None):
    """
    Notify plugins about an updated booking asynchronously
    
    Args:
        booking: Booking instance that was updated
        previous_state: Dictionary containing the previous state of the booking
        request: Current HTTP request (optional)
        user: Current user (optional)
    """
    context = {
        'request': request,
        'user': user
    }
    notify_plugins_async('booking_updated', booking=booking, previous_state=previous_state, context=context)

def get_dashboard_widgets(context):
    """
    Get dashboard widgets from all plugins
    
    Args:
        context: Context to pass to the dashboard_widget hook
    
    Returns:
        List of widget definitions
    """
    notify_plugins('dashboard_widget', context=context)
