from django.utils import timezone
from datetime import datetime, timedelta, time
from django.db.models import Q

from bookings.models import (
    StaffMember, 
    StaffAvailability, 
    Booking, 
    BookingStatus, 
    AVAILABILITY_TYPE, 
    BookingStaffAssignment
)


def check_timeslot_availability(
    business_id, 
    date_str, 
    time_str, 
    duration_minutes=60, 
    service_offering_id=None, 
    staff_member_id=None
):
    """
    Check if a timeslot is available for a business and provide alternate timeslots if not.
    
    Args:
        business_id (UUID): ID of the business
        date_str (str): Date string in format 'YYYY-MM-DD'
        time_str (str): Time string in format 'HH:MM'
        duration_minutes (int): Duration of the appointment in minutes
        service_offering_id (UUID, optional): ID of the service offering (not used for availability check)
        staff_member_id (UUID, optional): ID of a specific staff member to check
        
    Returns:
        dict: {
            'is_available': bool,
            'available_staff': list of staff objects with id and name,
            'reason': str (if not available),
            'alternate_slots': list of dicts with alternate date/time options
        }
    """
    try:
        print(f"DEBUG: Parsing date={date_str}, time={time_str}, duration={duration_minutes}")
        
        # Parse date and time
        booking_date = datetime.strptime(date_str, '%Y-%m-%d').date()
        booking_start_time = datetime.strptime(time_str, '%H:%M').time()
        
        # Calculate end time
        start_datetime = datetime.combine(booking_date, booking_start_time)
        end_datetime = start_datetime + timedelta(minutes=duration_minutes)
        booking_end_time = end_datetime.time()
        
        print(f"DEBUG: Parsed date={booking_date}, start_time={booking_start_time}, end_time={booking_end_time}")
        
        # Validate the date is not in the past
        current_date = timezone.now().date()
        if booking_date < current_date:
            return {
                'is_available': False,
                'available_staff': [],
                'reason': 'The selected date is in the past.',
                'alternate_slots': get_alternate_timeslots(business_id, current_date, booking_start_time, duration_minutes, None, staff_member_id)
            }
        
        # If date is today, ensure time is not in the past
        if booking_date == current_date and booking_start_time < timezone.now().time():
            return {
                'is_available': False,
                'available_staff': [],
                'reason': 'The selected time is in the past.',
                'alternate_slots': get_alternate_timeslots(business_id, current_date, timezone.now().time(), duration_minutes, None, staff_member_id)
            }
        
        # Get qualified staff members - removed service offering filter
        staff_query = Q(business_id=business_id, is_active=True, is_available=True)
        
        if staff_member_id:
            staff_query &= Q(id=staff_member_id)
        
        qualified_staff = StaffMember.objects.filter(staff_query).distinct()
        
        if not qualified_staff.exists():
            return {
                'is_available': False,
                'available_staff': [],
                'reason': 'No qualified staff members found for this service.',
                'alternate_slots': []
            }
        
        # Check for overlapping bookings
        overlapping_bookings = Booking.objects.filter(
            business_id=business_id,
            booking_date=booking_date,
            start_time__lt=booking_end_time,
            end_time__gt=booking_start_time,
            status__in=[BookingStatus.PENDING, BookingStatus.CONFIRMED, BookingStatus.RESCHEDULED]
        )
        
        # Get staff members with overlapping bookings
        unavailable_staff_ids = set(
            BookingStaffAssignment.objects.filter(
                booking__in=overlapping_bookings
            ).values_list('staff_member_id', flat=True)
        )
        
        # Filter out staff with availability constraints
        available_staff = []
        for staff in qualified_staff:
            if staff.id in unavailable_staff_ids:
                continue
                
            if is_staff_available(staff, booking_date, booking_start_time, booking_end_time):
                available_staff.append({
                    'id': str(staff.id),
                    'name': staff.get_full_name()
                })
        
        if available_staff:
            return {
                'is_available': True,
                'available_staff': available_staff,
                'reason': '',
                'alternate_slots': []
            }
        else:
            # No staff available, find alternate slots
            return {
                'is_available': False,
                'available_staff': [],
                'reason': 'No staff members are available at the selected time.',
                'alternate_slots': get_alternate_timeslots(business_id, booking_date, booking_start_time, duration_minutes, None, staff_member_id)
            }
            
    except Exception as e:
        return {
            'is_available': False,
            'available_staff': [],
            'reason': f'Error checking availability: {str(e)}',
            'alternate_slots': []
        }


def is_staff_available(staff, booking_date, booking_start_time, booking_end_time):
    """
    Check if a staff member is available at the given date and time.
    
    Args:
        staff (StaffMember): Staff member to check
        booking_date (date): Date of the booking
        booking_start_time (time): Start time of the booking
        booking_end_time (time): End time of the booking
        
    Returns:
        bool: True if staff is available, False otherwise
    """
    weekday = booking_date.weekday()
    
    # First check specific date availability/unavailability (higher priority)
    specific_availabilities = staff.availability.filter(
        availability_type=AVAILABILITY_TYPE.SPECIFIC,
        specific_date=booking_date
    )
    
    if specific_availabilities.exists():
        # Check if any specific date rule marks this time as unavailable
        for avail in specific_availabilities:
            if avail.off_day:
                # This is an "off day" record - check if time overlaps with the off period
                if (booking_start_time < avail.end_time and booking_end_time > avail.start_time):
                    return False
            else:
                # This is an "available" record - check if time is fully contained in the available period
                if (booking_start_time >= avail.start_time and booking_end_time <= avail.end_time):
                    return True
        
        # If we have specific date rules but none explicitly allow this time, staff is unavailable
        return False
    
    # Check weekly availability if no specific date rules exist
    weekly_availabilities = staff.availability.filter(
        availability_type=AVAILABILITY_TYPE.WEEKLY,
        weekday=weekday
    )
    
    if weekly_availabilities.exists():
        # Check if any weekly rule marks this time as unavailable
        for avail in weekly_availabilities:
            if avail.off_day:
                # This is an "off day" record - check if time overlaps with the off period
                if (booking_start_time < avail.end_time and booking_end_time > avail.start_time):
                    return False
            else:
                # This is an "available" record - check if time is fully contained in the available period
                if (booking_start_time >= avail.start_time and booking_end_time <= avail.end_time):
                    return True
        
        # If we have weekly rules but none explicitly allow this time, staff is unavailable
        return False
    
    # If no availability rules exist for this day, staff is considered unavailable by default
    return False


def get_alternate_timeslots(business_id, date, start_time, duration_minutes, service_offering_id=None, staff_member_id=None):
    """
    Find alternate available timeslots when the requested slot is unavailable.
    
    Args:
        business_id (UUID): ID of the business
        date (date): Date to check
        start_time (time): Start time that was unavailable
        duration_minutes (int): Duration of the appointment in minutes
        service_offering_id (UUID, optional): ID of the service offering
        staff_member_id (UUID, optional): ID of a specific staff member to check
        
    Returns:
        list: List of dicts with alternate date/time options
    """
    alternate_slots = []
    current_date = date
    
    # Try same day, different times
    same_day_slots = find_available_slots_on_date(
        business_id, 
        current_date, 
        duration_minutes, 
        None, 
        staff_member_id,
        max_slots=3
    )
    
    alternate_slots.extend(same_day_slots)
    
    # If we don't have enough slots, try the next day
    if len(alternate_slots) < 3:
        next_day = current_date + timedelta(days=1)
        next_day_slots = find_available_slots_on_date(
            business_id, 
            next_day, 
            duration_minutes, 
            None, 
            staff_member_id,
            max_slots=3 - len(alternate_slots)
        )
        alternate_slots.extend(next_day_slots)
    
    # If we still don't have enough slots, try two days later
    if len(alternate_slots) < 3:
        two_days_later = current_date + timedelta(days=2)
        two_days_later_slots = find_available_slots_on_date(
            business_id, 
            two_days_later, 
            duration_minutes, 
            None, 
            staff_member_id,
            max_slots=3 - len(alternate_slots)
        )
        alternate_slots.extend(two_days_later_slots)
    
    return alternate_slots


def find_available_slots_on_date(business_id, date, duration_minutes, service_offering_id=None, staff_member_id=None, max_slots=3):
    """
    Find available time slots on a specific date.
    
    Args:
        business_id (UUID): ID of the business
        date (date): Date to check
        duration_minutes (int): Duration of the appointment in minutes
        service_offering_id (UUID, optional): ID of the service offering
        staff_member_id (UUID, optional): ID of a specific staff member to check
        max_slots (int): Maximum number of slots to return
        
    Returns:
        list: List of dicts with available time slots
    """
    print(f"DEBUG: Finding available slots on date={date}, duration={duration_minutes}, max_slots={max_slots}")
    available_slots = []
    
    # Get qualified staff members
    staff_query = Q(business_id=business_id, is_active=True, is_available=True)
    
    if staff_member_id:
        staff_query &= Q(id=staff_member_id)
    
    qualified_staff = StaffMember.objects.filter(staff_query).distinct()
    
    if not qualified_staff.exists():
        return []
    
    # Get all existing bookings for this date
    existing_bookings = Booking.objects.filter(
        business_id=business_id,
        booking_date=date,
        status__in=[BookingStatus.PENDING, BookingStatus.CONFIRMED, BookingStatus.RESCHEDULED]
    ).order_by('start_time')
    
    # Define standard business hours (can be customized based on business settings)
    business_start = time(9, 0)  # 9:00 AM
    business_end = time(17, 0)   # 5:00 PM
    
    # If checking for today, start from current time
    if date == timezone.now().date() and timezone.now().time() > business_start:
        current_time = timezone.now().time()
        # Round up to the nearest half hour
        minutes = current_time.minute
        if minutes < 30:
            business_start = time(current_time.hour, 30)
        else:
            business_start = time(current_time.hour + 1, 0)
    
    # Generate potential time slots at 30-minute intervals
    slot_interval = 30  # minutes
    slot_start = datetime.combine(date, business_start)
    slot_end = datetime.combine(date, business_end)
    
    # Track which staff members are booked at which times
    staff_bookings = {}
    for staff in qualified_staff:
        staff_bookings[str(staff.id)] = []
        
    # Populate staff bookings
    for booking in existing_bookings:
        staff_assignments = BookingStaffAssignment.objects.filter(booking=booking)
        for assignment in staff_assignments:
            staff_id = str(assignment.staff_member.id)
            if staff_id in staff_bookings:
                staff_bookings[staff_id].append({
                    'start': datetime.combine(date, booking.start_time),
                    'end': datetime.combine(date, booking.end_time)
                })
    
    # Track which slots we've already added to avoid duplicates
    added_slots = set()
    
    current_slot = slot_start
    while current_slot + timedelta(minutes=duration_minutes) <= slot_end and len(available_slots) < max_slots:
        slot_start_time = current_slot.time()
        slot_end_time = (current_slot + timedelta(minutes=duration_minutes)).time()
        
        slot_key = f"{slot_start_time.strftime('%H:%M')}-{slot_end_time.strftime('%H:%M')}"
        
        # Skip if we already added this slot
        if slot_key in added_slots:
            current_slot += timedelta(minutes=slot_interval)
            continue
        
        # Check if any staff member is available for this slot
        for staff in qualified_staff:
            staff_id = str(staff.id)
            
            # Check if staff has an overlapping booking
            has_overlap = False
            slot_start_dt = datetime.combine(date, slot_start_time)
            slot_end_dt = datetime.combine(date, slot_end_time)
            
            for booking in staff_bookings.get(staff_id, []):
                if (slot_start_dt < booking['end'] and slot_end_dt > booking['start']):
                    has_overlap = True
                    break
            
            if has_overlap:
                continue
                
            # Check staff availability
            if is_staff_available(staff, date, slot_start_time, slot_end_time):
                # Add this slot to available slots
                available_slots.append({
                    'date': date.strftime('%Y-%m-%d'),
                    'time': slot_start_time.strftime('%H:%M'),
                    'end_time': slot_end_time.strftime('%H:%M'),
                    'staff': {
                        'id': str(staff.id),
                        'name': staff.get_full_name()
                    }
                })
                
                # Mark this slot as added
                added_slots.add(slot_key)
                
                # Also mark this time as booked for this staff member to avoid suggesting overlapping slots
                staff_bookings[staff_id].append({
                    'start': slot_start_dt,
                    'end': slot_end_dt
                })
                
                break  # Found an available staff for this slot
        
        # Move to next slot
        current_slot += timedelta(minutes=slot_interval)
    
    print(f"DEBUG: Found {len(available_slots)} available slots")
    for slot in available_slots:
        print(f"DEBUG: Available slot: {slot['date']} {slot['time']}-{slot['end_time']} with {slot['staff']['name']}")
    
    return available_slots
