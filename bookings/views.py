from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from business.models import ServiceOffering, BusinessCustomField
from .models import Booking, BookingField
from django.utils import timezone

# Create your views here.
def index(request):
    return render(request, 'bookings/index.html', {
        'title': 'Bookings',
    })

@login_required
def create_booking(request):
    business = getattr(request.user, 'business', None)
    if not business:
        messages.error(request, 'Please register your business first.')
        return redirect('business:register')

    service_offerings = ServiceOffering.objects.filter(business=business, is_active=True).order_by('name')
    custom_fields = BusinessCustomField.objects.filter(business=business, is_active=True).order_by('display_order', 'name')

    if request.method == 'POST':
        # Basic Booking fields
        service_type_id = request.POST.get('service_type')
        booking_date = request.POST.get('booking_date')
        start_time = request.POST.get('start_time')
        end_time = request.POST.get('end_time')
        location_type = request.POST.get('location_type')
        location_details = request.POST.get('location_details')
        notes = request.POST.get('notes')

        # Validation (minimal, expand as needed)
        errors = []
        if not service_type_id:
            errors.append('Service type is required.')
        if not booking_date:
            errors.append('Booking date is required.')
        if not start_time or not end_time:
            errors.append('Start and end time are required.')
        if errors:
            for err in errors:
                messages.error(request, err)
            return render(request, 'bookings/create_booking.html', {
                'service_offerings': service_offerings,
                'custom_fields': custom_fields,
            })

        # Create Booking
        booking = Booking.objects.create(
            business=business,
            service_type_id=service_type_id,
            booking_date=booking_date,
            start_time=start_time,
            end_time=end_time,
            location_type=location_type,
            location_details=location_details,
            notes=notes,
            status='pending',
        )

        # Save custom fields
        for field in custom_fields:
            val = request.POST.get(f'custom_{field.slug}', '')
            if field.required and not val:
                messages.error(request, f'{field.name} is required.')
                booking.delete()
                return render(request, 'bookings/create_booking.html', {
                    'service_offerings': service_offerings,
                    'custom_fields': custom_fields,
                })
            BookingField.objects.create(
                booking=booking,
                field_type='business',
                business_field=field,
                value=val,
            )

        messages.success(request, 'Booking created successfully!')
        return redirect(reverse('bookings:index'))

    # GET
    return render(request, 'bookings/create_booking.html', {
        'service_offerings': service_offerings,
        'custom_fields': custom_fields,
    })
