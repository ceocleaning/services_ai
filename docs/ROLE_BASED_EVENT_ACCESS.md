# Role-Based Event Access Control

## Overview

The booking event system now supports **role-based access control**, allowing business owners to specify which user groups can see and trigger specific event types. This provides flexibility to:

- Restrict sensitive actions (e.g., payments) to business owners only
- Allow staff to perform certain tasks (e.g., mark complete, add notes)
- Enable customers to cancel their own bookings
- Create custom workflows for different roles (e.g., cleaners, technicians)

## User Roles

The system recognizes three primary user groups:

### 1. **Business Owner** (`business` group)
- Full access to all business operations
- Can manage settings, staff, services, and bookings
- Typically the business account owner

### 2. **Staff Members** (`staff` group)
- Employees assigned to bookings
- Limited access based on assigned bookings
- Can view and update their assigned appointments

### 3. **Customers** (`customer` group)
- Clients who made bookings
- Can view their own bookings
- Limited to customer-facing actions

## How It Works

### Display Logic Flow

When a user views a booking detail page, the system:

1. **Checks booking state** - Is the booking in the right status? (via `should_display_event_button()`)
2. **Checks user role** - Does the user belong to an allowed role? (via `is_accessible_by_user()`)
3. **Shows button** - Only if BOTH conditions are met

### Configuration Options

For each event type, you can:

- **Leave all roles unchecked** → Everyone can access (default)
- **Select one role** → Only that role can access
- **Select multiple roles** → Any of the selected roles can access

## Configuration Guide

### Step 1: Access Booking Preferences

1. Navigate to **Business Settings**
2. Click **Booking Preferences**
3. Find the **Event Types** section

### Step 2: Edit Event Type

1. Click the **Edit** button (pencil icon) next to the event
2. Scroll to **"Who Can Access This Event?"**
3. Check the roles that should have access:
   - ☑️ Business Owner
   - ☑️ Staff Members
   - ☑️ Customers

### Step 3: Save Changes

1. Click **Save Changes**
2. The page will reload with updated settings

## Common Configuration Examples

### Example 1: Payment Received (Business Owner Only)

**Use Case:** Only the business owner should record payments

**Configuration:**
- ☑️ Business Owner
- ☐ Staff Members
- ☐ Customers

### Example 2: Complete Booking (Business Owner + Staff)

**Use Case:** Both owner and assigned staff can mark bookings complete

**Configuration:**
- ☑️ Business Owner
- ☑️ Staff Members
- ☐ Customers

### Example 3: Add Note (Business Owner + Staff)

**Use Case:** Owner and staff can add internal notes

**Configuration:**
- ☑️ Business Owner
- ☑️ Staff Members
- ☐ Customers

### Example 4: Cancel Booking (Everyone)

**Use Case:** Anyone can cancel a booking (within policy)

**Configuration:**
- ☐ Business Owner
- ☐ Staff Members
- ☐ Customers

*Leave all unchecked for universal access*

### Example 5: Custom Role - Cleaner

**Use Case:** Create a "Complete Cleaning" event for cleaning staff

**Configuration:**
1. Create a new user group called `cleaner` in Django admin
2. Assign cleaning staff to this group
3. Create event type "Cleaning Completed"
4. In the future, you could extend the UI to include custom groups

## Technical Implementation

### Database Schema

**Model:** `BookingEventType`

```python
allowed_roles = models.JSONField(
    default=list,
    blank=True,
    help_text="List of user groups/roles that can access this event"
)
```

**Example Data:**
```json
{
    "allowed_roles": ["business", "staff"]
}
```

### Backend Logic

**Method:** `is_accessible_by_user(user)`

```python
def is_accessible_by_user(self, user):
    """Check if user has access based on their role/group"""
    # If no roles specified, everyone has access
    if not self.allowed_roles:
        return True
    
    # Get user's group names
    user_groups = list(user.groups.values_list('name', flat=True))
    
    # Check if user belongs to any allowed role
    for role in self.allowed_roles:
        if role in user_groups:
            return True
    
    return False
```

### View Integration

**File:** `bookings/views.py` → `booking_detail()`

```python
# Filter event types based on display logic AND user role
enabled_event_types = [
    event_type for event_type in all_event_types
    if should_display_event_button(booking, event_type.event_key) 
    and event_type.is_accessible_by_user(request.user)
]
```

### Frontend (JavaScript)

**File:** `static/js/booking-preferences.js`

- Fetches current `allowed_roles` when editing
- Sends updated `allowed_roles` array when saving
- Handles checkbox states for role selection

## Benefits

### 1. **Security**
- Prevent unauthorized actions
- Protect sensitive operations (payments, cancellations)

### 2. **Workflow Control**
- Define clear responsibilities
- Assign tasks to appropriate roles

### 3. **User Experience**
- Show only relevant actions
- Reduce clutter and confusion

### 4. **Flexibility**
- Different workflows per business
- Adapt to industry-specific needs

### 5. **Scalability**
- Easy to add new roles
- Support complex organizational structures

## Advanced Use Cases

### Multi-Level Staff Hierarchy

Create different staff roles:
- `staff_manager` - Can complete and cancel bookings
- `staff_technician` - Can only mark complete
- `staff_cleaner` - Can only mark cleaning complete

### Customer Self-Service

Allow customers to:
- Cancel their own bookings (with policy restrictions)
- Reschedule appointments
- Add notes/requests

### Industry-Specific Roles

**Healthcare:**
- `doctor` - Can complete appointments
- `nurse` - Can add notes
- `receptionist` - Can reschedule

**Home Services:**
- `technician` - Can mark complete
- `dispatcher` - Can reschedule
- `manager` - Full access

## Migration Notes

### For Existing Businesses

1. **Default Behavior:** All existing event types have `allowed_roles = []` (empty)
2. **This means:** Everyone has access (backward compatible)
3. **Action Required:** Configure role access for each event type as needed

### Database Migration

Run the migration to add the `allowed_roles` field:

```bash
python manage.py makemigrations bookings
python manage.py migrate bookings
```

## Troubleshooting

### Event Button Not Showing

**Check:**
1. Is the event type enabled?
2. Does the booking meet display conditions? (status, timing)
3. Does the user belong to an allowed role?
4. Are any roles selected? (empty = everyone)

### User Can't Access Event

**Solution:**
1. Go to Booking Preferences
2. Edit the event type
3. Check the user's role
4. Save changes

### Custom Role Not Working

**Steps:**
1. Create the group in Django admin
2. Assign users to the group
3. Update event type `allowed_roles` (may need database update)
4. Refresh the page

## Future Enhancements

Potential improvements:

1. **UI for Custom Roles** - Add custom roles directly in the interface
2. **Permission Templates** - Pre-configured role sets for different industries
3. **Conditional Access** - Role + booking conditions (e.g., staff only for their assigned bookings)
4. **Audit Log** - Track who triggered which events
5. **Role Hierarchy** - Inherit permissions from parent roles

## Related Documentation

- [Event Display Logic](./EVENT_DISPLAY_LOGIC.md) - Booking state-based display rules
- [User Groups Management](./USER_GROUPS.md) - How to create and manage user groups
- [Booking Workflow](./BOOKING_WORKFLOW.md) - Complete booking lifecycle

## Support

For questions or issues:
1. Check this documentation
2. Review the code comments in `bookings/models.py`
3. Test with different user roles
4. Contact development team
