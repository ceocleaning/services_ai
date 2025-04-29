"""
Views for managing business custom fields
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.contrib import messages
from django.http import JsonResponse
import json

from .models import Business, Industry, IndustryField, BusinessCustomField


@login_required
@require_http_methods(["GET"])
def custom_fields(request):
    """
    Render the custom fields management page
    Shows all custom fields for the business and industry defaults
    """
    # Check if user has a business
    if not hasattr(request.user, 'business'):
        messages.warning(request, 'Please register your business first.')
        return redirect('business:register')
    
    business = request.user.business
    
    # Get all custom fields for this business
    custom_fields = BusinessCustomField.objects.filter(business=business).order_by('display_order')
    
    # Get all industry fields for reference
    industry_fields = IndustryField.objects.filter(industry=business.industry, is_active=True).order_by('display_order')
    
    context = {
        'business': business,
        'custom_fields': custom_fields,
        'industry_fields': industry_fields
    }
    
    return render(request, 'business/custom_fields.html', context)


@login_required
@require_http_methods(["POST"])
def add_custom_field(request):
    """
    Add a new custom field to the business
    Handles form submission from the custom fields page
    """
    # Check if user has a business
    if not hasattr(request.user, 'business'):
        messages.warning(request, 'Please register your business first.')
        return redirect('business:register')
    
    business = request.user.business
    
    try:
        # Process options for select field type
        options = None
        if request.POST.get('field_type') == 'select' and request.POST.get('options'):
            options = {
                'choices': [option.strip() for option in request.POST.get('options').split('\n') if option.strip()]
            }
        
        # Create new custom field
        field = BusinessCustomField.objects.create(
            business=business,
            name=request.POST.get('name'),
            field_type=request.POST.get('field_type'),
            options=options,
            placeholder=request.POST.get('placeholder', ''),
            help_text=request.POST.get('help_text', ''),
            required='required' in request.POST,
            display_order=request.POST.get('display_order', 0),
            is_active='is_active' in request.POST
        )
        
        messages.success(request, f'Field "{field.name}" added successfully!')
    except Exception as e:
        messages.error(request, f'An error occurred: {str(e)}')
    
    return redirect('business:custom_fields')


@login_required
@require_http_methods(["POST"])
def update_custom_field(request):
    """
    Update an existing custom field
    Handles form submission from the custom fields page
    """
    # Check if user has a business
    if not hasattr(request.user, 'business'):
        messages.warning(request, 'Please register your business first.')
        return redirect('business:register')
    
    business = request.user.business
    field_id = request.POST.get('field_id')
    
    if not field_id:
        messages.error(request, 'Field ID is required')
        return redirect('business:custom_fields')
    
    try:
        # Get field and verify it belongs to this business
        field = get_object_or_404(BusinessCustomField, id=field_id, business=business)
        
        # Process options for select field type
        if request.POST.get('field_type') == 'select' and request.POST.get('options'):
            field.options = {
                'choices': [option.strip() for option in request.POST.get('options').split('\n') if option.strip()]
            }
        else:
            field.options = None
        
        # Update field fields
        field.name = request.POST.get('name')
        field.field_type = request.POST.get('field_type')
        field.placeholder = request.POST.get('placeholder', '')
        field.help_text = request.POST.get('help_text', '')
        field.required = 'required' in request.POST
        field.display_order = request.POST.get('display_order', 0)
        field.is_active = 'is_active' in request.POST
        
        # Save changes
        field.save()
        
        messages.success(request, f'Field "{field.name}" updated successfully!')
    except Exception as e:
        messages.error(request, f'An error occurred: {str(e)}')
    
    return redirect('business:custom_fields')


@login_required
@require_http_methods(["POST"])
def delete_custom_field(request):
    """
    Delete an existing custom field
    Handles form submission from the custom fields page
    """
    # Check if user has a business
    if not hasattr(request.user, 'business'):
        messages.warning(request, 'Please register your business first.')
        return redirect('business:register')
    
    business = request.user.business
    field_id = request.POST.get('field_id')
    
    if not field_id:
        messages.error(request, 'Field ID is required')
        return redirect('business:custom_fields')
    
    try:
        # Get field and verify it belongs to this business
        field = get_object_or_404(BusinessCustomField, id=field_id, business=business)
        field_name = field.name
        
        # Delete field
        field.delete()
        
        messages.success(request, f'Field "{field_name}" deleted successfully!')
    except Exception as e:
        messages.error(request, f'An error occurred: {str(e)}')
    
    return redirect('business:custom_fields')


@login_required
def get_custom_field_details(request, field_id):
    """
    API endpoint to get custom field details for editing
    Returns JSON response with field data
    """
    # Check if user has a business
    if not hasattr(request.user, 'business'):
        return JsonResponse({'error': 'Please register your business first'}, status=403)
    
    business = request.user.business
    
    try:
        # Get field and verify it belongs to this business
        field = get_object_or_404(BusinessCustomField, id=field_id, business=business)
        
        # Return field data as JSON
        return JsonResponse({
            'id': field.id,
            'name': field.name,
            'field_type': field.field_type,
            'options': field.options,
            'placeholder': field.placeholder or '',
            'help_text': field.help_text or '',
            'required': field.required,
            'display_order': field.display_order,
            'is_active': field.is_active
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)


@login_required
@require_http_methods(["GET"])
def reset_custom_fields(request):
    """
    Reset custom fields to industry defaults
    Deletes all custom fields and creates new ones based on industry defaults
    """
    # Check if user has a business
    if not hasattr(request.user, 'business'):
        messages.warning(request, 'Please register your business first.')
        return redirect('business:register')
    
    business = request.user.business
    
    try:
        # Delete all existing custom fields
        BusinessCustomField.objects.filter(business=business).delete()
        
        # Get industry fields
        industry_fields = IndustryField.objects.filter(industry=business.industry, is_active=True)
        
        # Create custom fields based on industry defaults
        for field in industry_fields:
            BusinessCustomField.objects.create(
                business=business,
                name=field.name,
                field_type=field.field_type,
                options=field.options,
                placeholder=field.placeholder,
                help_text=field.help_text,
                required=field.required,
                default_value=field.default_value,
                validation_regex=field.validation_regex,
                display_order=field.display_order,
                is_active=True
            )
        
        messages.success(request, 'Custom fields reset to industry defaults successfully!')
    except Exception as e:
        messages.error(request, f'An error occurred: {str(e)}')
    
    return redirect('business:custom_fields')


@login_required
@require_http_methods(["POST"])
def reorder_custom_fields(request):
    """
    Update the display order of custom fields
    Accepts JSON data with field IDs and new order values
    """
    # Check if user has a business
    if not hasattr(request.user, 'business'):
        return JsonResponse({'error': 'Please register your business first'}, status=403)
    
    business = request.user.business
    
    try:
        # Parse JSON data
        data = json.loads(request.body)
        fields = data.get('fields', [])
        
        # Update field order
        for field_data in fields:
            field_id = field_data.get('id')
            new_order = field_data.get('order')
            
            if field_id and new_order is not None:
                # Get field and verify it belongs to this business
                field = get_object_or_404(BusinessCustomField, id=field_id, business=business)
                field.display_order = new_order
                field.save()
        
        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)
