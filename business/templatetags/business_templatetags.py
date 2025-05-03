from django import template

register = template.Library()

@register.filter
def filter_by_weekday(availabilities, weekday):
    """
    Filter a queryset of staff availabilities by weekday
    
    Args:
        availabilities: A queryset of StaffAvailability objects
        weekday: The weekday number (0-6) to filter by
        
    Returns:
        A filtered queryset containing only availabilities for the specified weekday
    """
    return [avail for avail in availabilities if avail.weekday == weekday]