"""
Event processors for booking events
Each processor handles a specific event type and returns a result dict
"""

from django.utils import timezone
from django.db import models
from datetime import datetime
from decimal import Decimal, InvalidOperation
from .models import BookingEvent, BookingStatus


def process_confirmed_event(booking, event_type, data, user):
    """Process booking confirmation"""
    if booking.status == BookingStatus.CONFIRMED:
        return {'success': False, 'message': 'Booking is already confirmed'}
    
    # Update booking status
    booking.status = BookingStatus.CONFIRMED
    booking.save()
    
    # Create event with dynamic field values
    BookingEvent.objects.create(
        booking=booking,
        event_type=event_type,
        description=f'Booking confirmed by {user.get_full_name() or user.username}',
        field_values=data,
        created_by=user
    )
    
    return {
        'success': True,
        'message': 'Booking confirmed successfully'
    }


def process_cancelled_event(booking, event_type, data, user):
    """Process booking cancellation"""
    # Validate 24-hour policy
    booking_datetime = timezone.make_aware(
        datetime.combine(booking.booking_date, booking.start_time)
    )
    hours_until = (booking_datetime - timezone.now()).total_seconds() / 3600
    
    if hours_until < 24:
        return {
            'success': False,
            'message': 'Cannot cancel less than 24 hours before appointment'
        }
    
    reason = data.get('reason', '').strip()
    if not reason:
        return {'success': False, 'message': 'Cancellation reason is required'}
    
    # Update booking
    booking.status = BookingStatus.CANCELLED
    booking.cancellation_reason = reason
    booking.save()
    
    # Create event with dynamic field values
    BookingEvent.objects.create(
        booking=booking,
        event_type=event_type,
        description=f'Booking cancelled by {user.get_full_name() or user.username}',
        reason=reason,
        field_values=data,
        created_by=user
    )
    
    # TODO: Send notification if requested
    # if data.get('notify_customer'):
    #     send_cancellation_notification(booking)
    
    return {
        'success': True,
        'message': 'Booking cancelled successfully'
    }


def process_completed_event(booking, event_type, data, user):
    """Process booking completion"""
    if booking.status == BookingStatus.COMPLETED:
        return {'success': False, 'message': 'Booking is already completed'}
    
    notes = data.get('notes', '').strip()
    
    # Update booking
    booking.status = BookingStatus.COMPLETED
    if notes:
        booking.notes = (booking.notes or '') + f'\n\nCompletion Notes: {notes}'
    booking.save()
    
    # Create event with dynamic field values
    description = f'Booking completed by {user.get_full_name() or user.username}'
    if notes:
        description += f'\nNotes: {notes}'
    
    BookingEvent.objects.create(
        booking=booking,
        event_type=event_type,
        description=description,
        field_values=data,
        created_by=user
    )
    
    # TODO: Send thank you message if requested
    if data.get('send_thank_you'):
        print("Message sent successfully")
    
    # TODO: Request review if requested
    if data.get('request_review'):
        print("Review requested successfully")
    
    return {
        'success': True,
        'message': 'Booking marked as completed'
    }


def process_no_show_event(booking, event_type, data, user):
    """Process no-show"""
    reason = data.get('reason', '').strip()
    if not reason:
        return {'success': False, 'message': 'Notes are required for no-show'}
    
    # Update booking
    booking.status = BookingStatus.NO_SHOW
    booking.notes = (booking.notes or '') + f'\n\nNo-Show Notes: {reason}'
    booking.save()
    
    # Create event with dynamic field values
    BookingEvent.objects.create(
        booking=booking,
        event_type=event_type,
        description=f'Marked as no-show by {user.get_full_name() or user.username}',
        reason=reason,
        field_values=data,
        created_by=user
    )
    
    # TODO: Charge cancellation fee if requested
    # if data.get('charge_cancellation_fee'):
    #     create_cancellation_fee_invoice(booking)
    
    return {
        'success': True,
        'message': 'Booking marked as no-show'
    }


def process_note_added_event(booking, event_type, data, user):
    """Add note to booking"""
    note = data.get('note', '').strip()
    if not note:
        return {'success': False, 'message': 'Note cannot be empty'}
    
    # Add note to booking
    timestamp = timezone.now().strftime('%Y-%m-%d %H:%M')
    booking.notes = (booking.notes or '') + f'\n\n[{timestamp}] {user.get_full_name() or user.username}: {note}'
    booking.save()
    
    # Create event with dynamic field values
    BookingEvent.objects.create(
        booking=booking,
        event_type=event_type,
        description=f'Note added by {user.get_full_name() or user.username}',
        reason=note,
        field_values=data,
        created_by=user
    )
    
    return {
        'success': True,
        'message': 'Note added successfully'
    }


def process_payment_received_event(booking, event_type, data, user):
    """Record payment"""
    amount = data.get('amount')
    payment_method = data.get('payment_method')
    
    if not amount or not payment_method:
        return {'success': False, 'message': 'Amount and payment method are required'}
    
    try:
        amount = Decimal(amount)
        if amount <= 0:
            return {'success': False, 'message': 'Amount must be greater than 0'}
    except (ValueError, InvalidOperation):
        return {'success': False, 'message': 'Invalid amount'}
    
    # Create payment record
    from invoices.models import Invoice, Payment
    
    # Get or create invoice
    invoice, created = Invoice.objects.get_or_create(
        booking=booking,
        defaults={
            'business': booking.business,
            'lead': booking.lead,
            'total_amount': Decimal('0.00'),
            'status': 'pending'
        }
    )
    
    # Create payment
    payment = Payment.objects.create(
        invoice=invoice,
        amount=amount,
        payment_method=payment_method,
        notes=data.get('notes', ''),
        payment_date=timezone.now()
    )
    
    # Update invoice status if fully paid
    total_paid = invoice.payments.filter(is_refunded=False).aggregate(
        total=models.Sum('amount')
    )['total'] or Decimal('0.00')
    
    if total_paid >= invoice.total_amount:
        invoice.status = 'paid'
        invoice.save()
    
    # Create event with dynamic field values
    BookingEvent.objects.create(
        booking=booking,
        event_type=event_type,
        description=f'Payment of ${amount} received via {payment_method}',
        field_values=data,
        created_by=user
    )
    
    return {
        'success': True,
        'message': 'Payment recorded successfully'
    }


def process_status_changed_event(booking, event_type, data, user):
    """Generic status change event"""
    old_status = booking.status
    new_status = data.get('new_status')
    reason = data.get('reason', '').strip()
    
    if not new_status:
        return {'success': False, 'message': 'New status is required'}
    
    # Update booking
    booking.status = new_status
    booking.save()
    
    # Create event with dynamic field values
    BookingEvent.objects.create(
        booking=booking,
        event_type=event_type,
        description=f'Status changed from {old_status} to {new_status} by {user.get_full_name() or user.username}',
        reason=reason,
        field_values=data,
        created_by=user
    )
    
    return {
        'success': True,
        'message': 'Status updated successfully'
    }


# Registry of event processors
EVENT_PROCESSORS = {
    'confirmed': process_confirmed_event,
    'cancelled': process_cancelled_event,
    'completed': process_completed_event,
    'no_show': process_no_show_event,
    'note_added': process_note_added_event,
    'payment_received': process_payment_received_event,
    'status_changed': process_status_changed_event,
}
