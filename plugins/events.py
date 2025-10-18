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
    print(f"\n{'='*60}")
    print(f"[PLUGIN] notify_plugins called: {event_name}")
    print(f"   Arguments: {list(kwargs.keys())}")
    try:
        result = plugin_manager.call_hook(event_name, **kwargs)
        print(f"[SUCCESS] HOOK CALLED: {event_name}")
        print(f"   Result: {result}")
        print(f"   Result type: {type(result)}")
        print(f"   Result length: {len(result) if result else 0}")
        print(f"{'='*60}\n")
        return result
    except Exception as e:
        print(f"[ERROR] Error notifying plugins about {event_name}: {str(e)}")
        import traceback
        traceback.print_exc()
        print(f"{'='*60}\n")
        return []

def notify_plugins_async(event_name, **kwargs):
    """
    Notify all plugins about an event asynchronously using Django Q
    
    Args:
        event_name: Name of the hook to call
        **kwargs: Arguments to pass to the hook
    """
    try:
        # Use Django Q for async execution
        async_task('plugins.events.notify_plugins', event_name, **kwargs)
    except Exception as e:
        print(f"Error scheduling async plugin notification: {str(e)}")
        # Fallback to synchronous
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
    print(f"[LEAD] notify_lead_created called for lead: {lead.id if hasattr(lead, 'id') else lead}")
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
    print(f"[ASYNC] notify_lead_created_async called for lead: {lead.id if hasattr(lead, 'id') else lead}")
    try:
        # Serialize lead ID instead of the object for async processing
        print(f"   Scheduling async task...")
        async_task(
            'plugins.events.notify_lead_created',
            lead,
            request=request,
            user=user
        )
        print(f"   [OK] Async task scheduled")
    except Exception as e:
        print(f"   [ERROR] Error scheduling async lead notification: {str(e)}")
        # Fallback to synchronous
        print(f"   Falling back to synchronous...")
        notify_lead_created(lead, request=request, user=user)

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
    try:
        # Serialize booking ID instead of the object for async processing
        async_task(
            'plugins.events.notify_booking_created',
            booking,
            request=request,
            user=user
        )
    except Exception as e:
        print(f"Error scheduling async booking notification: {str(e)}")
        # Fallback to synchronous
        notify_booking_created(booking, request=request, user=user)

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
    try:
        # Serialize for async processing
        async_task(
            'plugins.events.notify_booking_updated',
            booking,
            previous_state,
            request=request,
            user=user
        )
    except Exception as e:
        print(f"Error scheduling async booking update notification: {str(e)}")
        # Fallback to synchronous
        notify_booking_updated(booking, previous_state, request=request, user=user)

def get_dashboard_widgets(context):
    """
    Get dashboard widgets from all plugins
    
    Args:
        context: Context to pass to the dashboard_widget hook
    
    Returns:
        List of widget definitions
    """
    notify_plugins('dashboard_widget', context=context)
