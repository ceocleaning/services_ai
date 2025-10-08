# Event Button Display Logic

This document outlines the predefined logic for when each booking event button should be displayed on the booking detail page.

## Overview

The display logic is centralized in the `should_display_event_button()` function in `bookings/views.py`. This function evaluates the booking's current state and determines which event buttons should be shown to the user.

## Role-Based Access Control

In addition to the display logic based on booking state, each event type can be restricted to specific user roles:

- **Business Owner** (`business` group): Full access to all business operations
- **Staff Members** (`staff` group): Employees assigned to bookings
- **Customers** (`customer` group): Clients who made bookings

### How It Works

1. **No roles selected** = Everyone can access the event
2. **One or more roles selected** = Only users in those roles can see the event button

### Configuration

Business owners can configure role access in **Business Settings > Booking Preferences**:
1. Click the edit button (pencil icon) next to any event type
2. Select which roles should have access to this event
3. Save changes

### Example Use Cases

- **Complete Booking**: Only Business Owner and Staff
- **Add Note**: Business Owner and Staff only
- **Payment Received**: Business Owner only
- **Cancel Booking**: All roles (leave unchecked)

## Display Rules by Event Type

### 1. **Booking Created** (`created`)
- **Display:** Never
- **Reason:** This event is automatically created when a booking is made. No manual trigger needed.

### 2. **Booking Confirmed** (`confirmed`)
- **Display:** Never
- **Reason:** Not needed in current workflow. Deleted/disabled.

### 3. **Cancel Booking** (`cancelled`)
- **Display:** When ALL conditions are met:
  - Booking status is NOT `completed`
  - Booking status is NOT `cancelled`
  - More than 24 hours until booking time
- **Logic:** Users can only cancel if the booking hasn't happened yet and they're within the cancellation policy window.

### 4. **Reschedule Booking** (`rescheduled`)
- **Display:** When ALL conditions are met:
  - Booking status is NOT `completed`
  - Booking status is NOT `cancelled`
  - More than 24 hours until booking time
- **Logic:** Same as cancel - users need sufficient notice to reschedule.

### 5. **Complete Booking** (`completed`)
- **Display:** When ALL conditions are met:
  - Booking status is `confirmed`
  - Booking date/time is today or in the past
  - Booking status is NOT already `completed`
  - Booking status is NOT `cancelled`
- **Logic:** You can only mark a booking complete if it's confirmed and the appointment time has arrived or passed.

### 6. **No Show** (`no_show`)
- **Display:** When ALL conditions are met:
  - Booking status is `confirmed`
  - Booking date/time is in the past
  - Booking status is NOT `completed`
  - Booking status is NOT `cancelled`
- **Logic:** Mark as no-show only if the customer was confirmed but didn't show up after the appointment time.

### 7. **Add Note** (`note_added`)
- **Display:** When:
  - Booking status is NOT `completed`
  - Booking status is NOT `cancelled`
- **Logic:** You can add notes to active bookings. Once completed or cancelled, the booking is closed.

### 8. **Payment Received** (`payment_received`)
- **Display:** When:
  - Booking status is NOT `cancelled`
- **Logic:** You can record payments for any booking except cancelled ones.

### 9. **Status Changed** (`status_changed`)
- **Display:** Always
- **Logic:** Admin/advanced feature that allows manual status changes regardless of booking state.

### 10. **Follow-up** (`follow_up`)
- **Display:** When:
  - Booking status is `completed`
- **Logic:** Schedule follow-ups only after the service has been completed.

### 11. **Reminder Sent** (`reminder_sent`)
- **Display:** When:
  - Booking date/time is in the future
- **Logic:** Only send reminders for upcoming appointments.

## Technical Implementation

### Backend Function
```python
def should_display_event_button(booking, event_key):
    """
    Determine if an event button should be displayed based on predefined logic.
    
    Args:
        booking: Booking instance
        event_key: Event type key (e.g., 'cancelled', 'completed')
    
    Returns:
        bool: True if button should be displayed
    """
```

### Time Calculations
- **hours_until**: Calculated as `(booking_datetime - now).total_seconds() / 3600`
- **is_future**: `hours_until > 0`
- **is_past**: `hours_until < 0`

### View Integration
The `booking_detail` view filters event types before passing them to the template:

```python
# Get all enabled event types
all_event_types = BookingEventType.objects.filter(
    business=business,
    is_enabled=True
).order_by('display_order')

# Filter based on display logic
enabled_event_types = [
    event_type for event_type in all_event_types
    if should_display_event_button(booking, event_type.event_key)
]
```

### Template Simplification
The template now simply loops through `enabled_event_types` without any conditional logic:

```django
{% for event_type in enabled_event_types %}
    <li>
        <a class="dropdown-item event-action" 
           data-event-key="{{ event_type.event_key }}" 
           data-event-type-id="{{ event_type.id }}">
            <i class="fas {{ event_type.icon }}"></i> {{ event_type.name }}
        </a>
    </li>
{% endfor %}
```

## Benefits of This Approach

1. **Centralized Logic**: All display rules are in one place, making it easy to maintain and update.
2. **Consistent Behavior**: Same rules apply across the entire application.
3. **Easy to Extend**: Adding new event types or modifying rules is straightforward.
4. **Clean Templates**: Templates are simplified and focus on presentation, not business logic.
5. **Testable**: The logic can be easily unit tested.

## Future Enhancements

If needed, this system can be extended to support:
- Database-driven display conditions (user-configurable rules)
- Role-based visibility (different rules for different user roles)
- Industry-specific rules (different logic per business type)
- Custom field-based conditions (show/hide based on booking field values)

## Modifying Display Logic

To change when an event button is displayed:

1. Open `bookings/views.py`
2. Find the `should_display_event_button()` function
3. Locate the event key in the `display_rules` dictionary
4. Update the boolean expression for that event
5. Save and test

Example:
```python
# Change "Complete" to show only for confirmed bookings on the exact day
'completed': (
    booking.status == 'confirmed' and 
    booking.booking_date == timezone.now().date()
),
```
