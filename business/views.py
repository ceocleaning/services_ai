from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseRedirect
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.http import require_http_methods
from django.contrib import messages
from django.db import transaction
from django.urls import reverse
import json

from .models import Business, Industry, IndustryField, BusinessConfiguration, ServiceOffering


@login_required
@ensure_csrf_cookie
def business_registration(request):
    """Render the business registration page"""
    # Check if user already has a business
    if hasattr(request.user, 'business'):
        messages.info(request, 'You already have a registered business.')
        return redirect('business:dashboard')
        
    return render(request, 'business/register.html')


@login_required
@require_http_methods(["GET"])
def get_industries(request):
    """API endpoint to get all active industries"""
    industries = Industry.objects.filter(is_active=True).values('id', 'name', 'description', 'icon')
    return JsonResponse({'industries': list(industries)})



@login_required
@require_http_methods(["POST"])
def register_business(request):
    """API endpoint to register a business"""
    # Check if user already has a business
    if hasattr(request.user, 'business'):
        return JsonResponse({
            'success': False,
            'message': 'You already have a registered business.'
        })
    
    try:
        # Parse JSON data from request body
        data = json.loads(request.body)
        
        # Validate required fields
        required_fields = ['business_name', 'industry', 'phone_number', 'email']
        for field in required_fields:
            if not data.get(field):
                return JsonResponse({
                    'success': False,
                    'message': f'{field.replace("_", " ").title()} is required.'
                })
        
        # Get industry
        try:
            industry = Industry.objects.get(pk=data['industry'], is_active=True)
        except Industry.DoesNotExist:
            return JsonResponse({
                'success': False,
                'message': 'Selected industry does not exist.'
            })
        
        # Create business with transaction to ensure atomicity
        with transaction.atomic():
            # Create business
            business = Business.objects.create(
                name=data['business_name'],
                user=request.user,
                industry=industry,
                phone_number=data['phone_number'],
                email=data['email'],
                website=data.get('website', ''),
                address=data.get('address', ''),
                city=data.get('city', ''),
                state=data.get('state', ''),
                zip_code=data.get('zip_code', ''),
                description=data.get('business_description', '')
            )
            
               # Create business configuration
            BusinessConfiguration.objects.create(business=business)
            
            return JsonResponse({
                'success': True,
                'message': 'Business registered successfully!',
                'redirect_url': '/dashboard/'
            })
            
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'An error occurred: {str(e)}'
        })


@login_required
def business_profile(request):
    """
    Render the business profile page
    Requires user to be logged in and have a business
    """
    # Check if user has a business
    if not hasattr(request.user, 'business'):
        messages.warning(request, 'Please register your business first.')
        return redirect('business:register')
    
    # Get business data
    business = request.user.business
    
    context = {
        'business': business,
    }
    
    return render(request, 'business/profile.html', context)


@login_required
@require_http_methods(["POST"])
def update_profile(request):
    """
    Update business profile information
    Handles form submission from the profile page
    """
    # Check if user has a business
    if not hasattr(request.user, 'business'):
        messages.warning(request, 'Please register your business first.')
        return redirect('business:register')
    
    business = request.user.business
    
    # Process form data
    try:
        # Update business fields
        business.name = request.POST.get('name', business.name)
        business.email = request.POST.get('email', business.email)
        business.phone_number = request.POST.get('phone_number', business.phone_number)
        business.website = request.POST.get('website', business.website)
        business.address = request.POST.get('address', business.address)
        business.city = request.POST.get('city', business.city)
        business.state = request.POST.get('state', business.state)
        business.zip_code = request.POST.get('zip_code', business.zip_code)
        business.description = request.POST.get('description', business.description)
        
        # Handle logo upload if provided
        if 'logo' in request.FILES:
            business.logo = request.FILES['logo']
        
        # Save changes
        business.save()
        
        messages.success(request, 'Business profile updated successfully!')
    except Exception as e:
        messages.error(request, f'An error occurred: {str(e)}')
    
    return redirect('business:profile')




@login_required
@require_http_methods(["GET"])
def business_pricing(request):
    """
    Render the service pricing configuration page
    Shows all services and packages for the business
    """
    # Check if user has a business
    if not hasattr(request.user, 'business'):
        messages.warning(request, 'Please register your business first.')
        return redirect('business:register')
    
    business = request.user.business
    
    # Get all services for this business
    services = ServiceOffering.objects.filter(business=business).order_by('name')
    
    # Get all packages for this business
    packages = ServicePackage.objects.filter(business=business).order_by('name')
    
    context = {
        'business': business,
        'services': services,
        'packages': packages
    }
    
    return render(request, 'business/pricing.html', context)


@login_required
@require_http_methods(["GET"])
def booking_settings(request):
    """
    Render the booking settings configuration page
    Placeholder for future implementation
    """
    return render(request, 'business/booking_settings.html')


@login_required
@require_http_methods(["GET"])
def notification_preferences(request):
    """
    Render the notification preferences configuration page
    Placeholder for future implementation
    """
    return render(request, 'business/notifications.html')


@login_required
@require_http_methods(["GET"])
def upgrade_plan(request):
    """
    Render the plan upgrade page
    Placeholder for future implementation
    """
    return render(request, 'business/upgrade.html')


@login_required
@require_http_methods(["POST"])
def add_service(request):
    """
    Add a new service to the business
    Handles form submission from the pricing page
    """
    # Check if user has a business
    if not hasattr(request.user, 'business'):
        messages.warning(request, 'Please register your business first.')
        return redirect('business:register')
    
    business = request.user.business
    
    try:
        # Create new service
        service = ServiceOffering.objects.create(
            business=business,
            name=request.POST.get('name'),
            description=request.POST.get('description', ''),
            price=request.POST.get('price'),
            duration=request.POST.get('duration'),
            icon=request.POST.get('icon', 'concierge-bell'),
            color=request.POST.get('color', '#6366f1'),
            is_active='is_active' in request.POST
        )
        
        messages.success(request, f'Service "{service.name}" added successfully!')
    except Exception as e:
        messages.error(request, f'An error occurred: {str(e)}')
    
    return redirect('business:pricing')


@login_required
@require_http_methods(["POST"])
def update_service(request):
    """
    Update an existing service
    Handles form submission from the pricing page
    """
    # Check if user has a business
    if not hasattr(request.user, 'business'):
        messages.warning(request, 'Please register your business first.')
        return redirect('business:register')
    
    business = request.user.business
    service_id = request.POST.get('service_id')
    
    if not service_id:
        messages.error(request, 'Service ID is required')
        return redirect('business:pricing')
    
    try:
        # Get service and verify it belongs to this business
        service = get_object_or_404(ServiceOffering, id=service_id, business=business)
        
        # Update service fields
        service.name = request.POST.get('name')
        service.description = request.POST.get('description', '')
        service.price = request.POST.get('price')
        service.duration = request.POST.get('duration')
        service.icon = request.POST.get('icon', 'concierge-bell')
        service.color = request.POST.get('color', '#6366f1')
        service.is_active = 'is_active' in request.POST
        
        # Save changes
        service.save()
        
        messages.success(request, f'Service "{service.name}" updated successfully!')
    except Exception as e:
        messages.error(request, f'An error occurred: {str(e)}')
    
    return redirect('business:pricing')


@login_required
@require_http_methods(["POST"])
def delete_service(request):
    """
    Delete an existing service
    Handles form submission from the pricing page
    """
    # Check if user has a business
    if not hasattr(request.user, 'business'):
        messages.warning(request, 'Please register your business first.')
        return redirect('business:register')
    
    business = request.user.business
    service_id = request.POST.get('service_id')
    
    if not service_id:
        messages.error(request, 'Service ID is required')
        return redirect('business:pricing')
    
    try:
        # Get service and verify it belongs to this business
        service = get_object_or_404(ServiceOffering, id=service_id, business=business)
        service_name = service.name
        
        # Delete service
        service.delete()
        
        messages.success(request, f'Service "{service_name}" deleted successfully!')
    except Exception as e:
        messages.error(request, f'An error occurred: {str(e)}')
    
    return redirect('business:pricing')


@login_required
@require_http_methods(["POST"])
def add_package(request):
    """
    Add a new package deal to the business
    Handles form submission from the pricing page
    """
    # Check if user has a business
    if not hasattr(request.user, 'business'):
        messages.warning(request, 'Please register your business first.')
        return redirect('business:register')
    
    business = request.user.business
    
    try:
        # Create new package
        package = ServicePackage.objects.create(
            business=business,
            name=request.POST.get('name'),
            description=request.POST.get('description', ''),
            price=request.POST.get('price'),
            savings=request.POST.get('savings', 0),
            is_active='is_active' in request.POST
        )
        
        # Add services to package
        service_ids = request.POST.getlist('services')
        if service_ids:
            services = ServiceOffering.objects.filter(id__in=service_ids, business=business)
            package.services.set(services)
        
        messages.success(request, f'Package "{package.name}" added successfully!')
    except Exception as e:
        messages.error(request, f'An error occurred: {str(e)}')
    
    return redirect('business:pricing')
