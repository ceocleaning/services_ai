# Reminder Workflow System - Future Implementation Plan

## 📋 Overview

A comprehensive reminder system for booking management that allows businesses to create automated reminder workflows based on booking events.

---

## 🎯 Goals

1. **Automate Communication** - Send timely reminders to customers
2. **Reduce No-Shows** - Remind customers before appointments
3. **Improve Experience** - Follow up after appointments
4. **Flexible Configuration** - Each business customizes their reminder strategy

---

## 🏗️ Architecture Options

### Option 1: Rule-Based System (Recommended - Phase 1)

**Complexity:** Medium  
**Dev Time:** 3-5 days  
**User Friendliness:** ⭐⭐⭐⭐⭐

#### Data Models

```python
class ReminderRule(models.Model):
    """Simple rule-based reminders"""
    business = models.ForeignKey(Business, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    is_active = models.BooleanField(default=True)
    
    # Trigger
    trigger_event = models.CharField(max_length=50, choices=(
        ('booking_created', 'When Booking Created'),
        ('booking_confirmed', 'When Booking Confirmed'),
        ('before_appointment', 'Before Appointment'),
        ('after_appointment', 'After Appointment'),
        ('booking_cancelled', 'When Booking Cancelled'),
        ('booking_rescheduled', 'When Booking Rescheduled'),
    ))
    
    # Timing
    timing_value = models.IntegerField(help_text="Number of hours/days")
    timing_unit = models.CharField(max_length=10, choices=(
        ('minutes', 'Minutes'),
        ('hours', 'Hours'),
        ('days', 'Days'),
    ))
    timing_direction = models.CharField(max_length=10, choices=(
        ('before', 'Before'),
        ('after', 'After'),
        ('immediately', 'Immediately'),
    ))
    
    # Channel & Template
    channel = models.CharField(max_length=20, choices=(
        ('sms', 'SMS'),
        ('email', 'Email'),
        ('whatsapp', 'WhatsApp'),
        ('voice', 'Voice Call'),
    ))
    template = models.ForeignKey('ReminderTemplate', on_delete=models.SET_NULL, null=True)
    
    # Conditions (optional)
    conditions = models.JSONField(blank=True, null=True, help_text="Simple if/then rules")
    
    # Priority & Order
    priority = models.IntegerField(default=0)
    display_order = models.IntegerField(default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class ReminderTemplate(models.Model):
    """Message templates with variable substitution"""
    business = models.ForeignKey(Business, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    channel = models.CharField(max_length=20)
    
    # Content
    subject = models.CharField(max_length=200, blank=True, help_text="For email only")
    message = models.TextField(help_text="Use {customer_name}, {appointment_date}, {appointment_time}, etc.")
    
    # Available variables
    available_variables = models.JSONField(default=list, help_text="List of available variables")
    
    # Metadata
    is_default = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class ScheduledReminder(models.Model):
    """Tracks scheduled and sent reminders"""
    booking = models.ForeignKey('Booking', on_delete=models.CASCADE, related_name='scheduled_reminders')
    rule = models.ForeignKey(ReminderRule, on_delete=models.SET_NULL, null=True)
    
    scheduled_time = models.DateTimeField()
    sent_time = models.DateTimeField(blank=True, null=True)
    
    channel = models.CharField(max_length=20)
    recipient = models.CharField(max_length=200)
    message = models.TextField()
    
    status = models.CharField(max_length=20, choices=(
        ('pending', 'Pending'),
        ('sent', 'Sent'),
        ('failed', 'Failed'),
        ('cancelled', 'Cancelled'),
    ), default='pending')
    
    error_message = models.TextField(blank=True, null=True)
    external_id = models.CharField(max_length=100, blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
```

#### UI Design

**Simple Form-Based Interface:**

```
┌─────────────────────────────────────────────────┐
│ Create Reminder Rule                            │
├─────────────────────────────────────────────────┤
│                                                 │
│ Rule Name: [24 Hour Appointment Reminder     ] │
│                                                 │
│ ┌─── Trigger ────────────────────────────────┐ │
│ │ When: [Before Appointment ▼]               │ │
│ │ Timing: [24] [Hours ▼] [Before ▼]         │ │
│ └────────────────────────────────────────────┘ │
│                                                 │
│ ┌─── Channel & Message ──────────────────────┐ │
│ │ Send Via: [SMS ▼]                          │ │
│ │ Template: [Appointment Reminder ▼]         │ │
│ │                                             │ │
│ │ Preview:                                    │ │
│ │ ┌─────────────────────────────────────────┐ │ │
│ │ │ Hi John, your appointment is tomorrow   │ │ │
│ │ │ at 2:00 PM at ABC Dental.               │ │ │
│ │ │ Reply CONFIRM to confirm.               │ │ │
│ │ └─────────────────────────────────────────┘ │ │
│ └────────────────────────────────────────────┘ │
│                                                 │
│ ┌─── Conditions (Optional) ──────────────────┐ │
│ │ ☑ Only if booking status is Confirmed      │ │
│ │ ☐ Only for specific services               │ │
│ │ ☐ Only for first-time customers            │ │
│ └────────────────────────────────────────────┘ │
│                                                 │
│ Status: ● Active                               │
│                                                 │
│ [Save Rule]  [Test Send]  [Cancel]            │
└─────────────────────────────────────────────────┘
```

#### Example Rules

1. **Confirmation Email** - Immediately after booking created
2. **24h Reminder SMS** - 24 hours before appointment
3. **2h Reminder SMS** - 2 hours before appointment
4. **Thank You Email** - 1 hour after appointment completed
5. **Review Request** - 24 hours after appointment completed
6. **Cancellation Notice** - Immediately when booking cancelled

#### Variable System

**Available Variables:**
- `{customer_name}` - Customer's full name
- `{customer_first_name}` - Customer's first name
- `{appointment_date}` - Formatted date (e.g., "Monday, Jan 15, 2025")
- `{appointment_time}` - Formatted time (e.g., "2:00 PM")
- `{appointment_duration}` - Duration (e.g., "60 minutes")
- `{service_name}` - Service name
- `{staff_name}` - Assigned staff member
- `{business_name}` - Business name
- `{business_phone}` - Business phone
- `{business_address}` - Business address
- `{location_details}` - Appointment location details
- `{booking_id}` - Booking reference number
- `{cancellation_link}` - Link to cancel booking
- `{reschedule_link}` - Link to reschedule booking

---

### Option 2: Visual Workflow Designer (Phase 2 - Future)

**Complexity:** Very High  
**Dev Time:** 3-5 weeks  
**User Friendliness:** ⭐⭐⭐ (requires learning)

#### Technology Stack

**Frontend:**
- **React Flow** - Node-based workflow canvas
- **React** - Component framework
- **Tailwind CSS** - Styling

**Backend:**
- **Workflow Engine** - Custom execution engine
- **Django Q2** - Task scheduling
- **Celery** (alternative) - Task queue

#### Features

**Node Types:**
1. **Trigger Nodes** - Booking events (created, confirmed, etc.)
2. **Action Nodes** - Send reminder (SMS, Email, WhatsApp)
3. **Delay Nodes** - Wait X hours/days
4. **Condition Nodes** - If/then logic
5. **Split Nodes** - A/B testing paths
6. **End Nodes** - Workflow completion

**Canvas Features:**
- Drag-and-drop nodes
- Connect nodes with lines
- Node configuration panels
- Real-time validation
- Workflow testing mode
- Version history
- Templates library

#### Example Workflow

```
[Booking Created]
       ↓
[Send Confirmation Email]
       ↓
[Wait 23 hours]
       ↓
[Check Status = Confirmed?]
    ↙        ↘
  Yes         No
   ↓           ↓
[Send SMS]  [Skip]
   ↓
[Wait 22 hours]
   ↓
[Send Final Reminder]
   ↓
[Wait until appointment time]
   ↓
[Wait 1 hour]
   ↓
[Send Thank You Email]
```

#### Data Structure

```python
class ReminderWorkflow(models.Model):
    business = models.ForeignKey(Business, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    
    # Canvas data (nodes, connections, positions)
    workflow_data = models.JSONField(default=dict)
    
    # Metadata
    version = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class WorkflowExecution(models.Model):
    """Track workflow executions"""
    workflow = models.ForeignKey(ReminderWorkflow, on_delete=models.CASCADE)
    booking = models.ForeignKey('Booking', on_delete=models.CASCADE)
    
    status = models.CharField(max_length=20)
    current_node = models.CharField(max_length=100, blank=True)
    execution_log = models.JSONField(default=list)
    
    started_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(blank=True, null=True)
```

---

## 🚀 Implementation Roadmap

### Phase 1: Rule-Based System (Week 1)

**Day 1-2: Backend**
- [ ] Create models (ReminderRule, ReminderTemplate, ScheduledReminder)
- [ ] Create migrations
- [ ] Admin interface
- [ ] Template variable parser

**Day 3: Frontend**
- [ ] Rule creation form
- [ ] Template editor with variable picker
- [ ] Rule list/management page

**Day 4: Integration**
- [ ] Hook into booking events
- [ ] Schedule reminders via Django Q2
- [ ] Send reminders (SMS/Email)
- [ ] Handle reschedules/cancellations

**Day 5: Testing & Polish**
- [ ] Test all trigger types
- [ ] Test variable substitution
- [ ] Error handling
- [ ] Documentation

### Phase 2: Enhanced Features (Week 2-3)

**Week 2:**
- [ ] Conditional rules (if status = X)
- [ ] Multi-step sequences
- [ ] A/B testing for templates
- [ ] Analytics dashboard

**Week 3:**
- [ ] Template library
- [ ] Rule templates (common patterns)
- [ ] Bulk operations
- [ ] Import/export rules

### Phase 3: Visual Designer (Month 2-3)

**Only if user demand exists**

**Month 2:**
- [ ] React Flow integration
- [ ] Node components
- [ ] Canvas workspace
- [ ] Basic workflow execution

**Month 3:**
- [ ] Advanced conditions
- [ ] Workflow testing
- [ ] Version control
- [ ] Migration from rules to workflows

---

## 📊 Success Metrics

**Phase 1 Success Criteria:**
- [ ] 80% of businesses create at least 1 reminder rule
- [ ] 50% reduction in no-show rates
- [ ] 90% reminder delivery success rate
- [ ] Positive user feedback

**Phase 2 Decision Criteria:**
- [ ] 30%+ of businesses request complex workflows
- [ ] Users hit limitations of rule-based system
- [ ] Competitive pressure (competitors have visual designers)
- [ ] ROI justifies 3-5 week investment

---

## 💡 Best Practices

### Template Writing

**Good:**
```
Hi {customer_first_name}! Your appointment with {staff_name} is tomorrow 
at {appointment_time}. See you at {business_name}!
Reply CONFIRM to confirm or CANCEL to cancel.
```

**Bad:**
```
Dear Sir/Madam, this is a reminder that you have an appointment.
```

### Timing Strategy

**Recommended Schedule:**
1. **Immediate** - Confirmation email after booking
2. **24 hours before** - First reminder (SMS)
3. **2 hours before** - Final reminder (SMS)
4. **1 hour after** - Thank you message (Email)
5. **24 hours after** - Review request (Email)

### Conditional Logic

**Common Conditions:**
- Only send if `status = confirmed`
- Skip if customer already confirmed
- Different messages for first-time vs returning customers
- Service-specific templates

---

## 🔧 Technical Considerations

### Scheduling

**Django Q2 Integration:**
```python
from django_q.tasks import schedule

def schedule_reminder(booking, rule):
    """Schedule a reminder based on rule"""
    trigger_time = calculate_trigger_time(booking, rule)
    
    schedule(
        'reminders.tasks.send_reminder',
        booking.id,
        rule.id,
        schedule_type='O',  # Once
        next_run=trigger_time
    )
```

### Reschedule Handling

When booking is rescheduled:
1. Cancel all pending reminders for old time
2. Recalculate trigger times
3. Schedule new reminders

### Variable Substitution

```python
def render_template(template, booking):
    """Replace variables with actual values"""
    context = {
        'customer_name': booking.lead.name,
        'customer_first_name': booking.lead.name.split()[0],
        'appointment_date': booking.booking_date.strftime('%A, %B %d, %Y'),
        'appointment_time': booking.start_time.strftime('%I:%M %p'),
        'service_name': booking.service_offering.name,
        'staff_name': booking.get_primary_staff().name,
        'business_name': booking.business.name,
        # ... more variables
    }
    
    message = template.message
    for key, value in context.items():
        message = message.replace(f'{{{key}}}', str(value))
    
    return message
```

---

## 📝 Notes

- Start with **Rule-Based System** (simple, effective)
- Collect user feedback for 2-3 months
- Only build **Visual Designer** if clear demand exists
- Focus on **reliability** over **complexity**
- **80% of value** comes from **20% of features**

---

## 🎯 Decision: Start with Phase 1

**Rationale:**
1. Covers 95% of use cases
2. Quick to implement (1 week)
3. Easy for users to understand
4. Proven pattern (used by major platforms)
5. Can upgrade to visual designer later if needed

**Next Steps:**
1. Complete Event Types feature
2. Implement Rule-Based Reminder System
3. Gather user feedback
4. Decide on Phase 2 based on data
