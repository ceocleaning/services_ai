from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse, Http404
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
import os

from .models import GeneratedWebsite
from .utils import save_html_file
from .openai_service import generate_website_with_openai


@login_required
def website_builder(request):
    """
    Main view for the AI Website Builder
    Displays form for generating website or shows existing website info
    """
    # Check if user has a business
    if not hasattr(request.user, 'business'):
        messages.warning(request, 'Please register your business first.')
        return redirect('business:register')
    
    # Get existing website if any
    try:
        existing_website = GeneratedWebsite.objects.get(user=request.user)
    except GeneratedWebsite.DoesNotExist:
        existing_website = None
    
    context = {
        'existing_website': existing_website,
        'business': request.user.business,
    }
    
    return render(request, 'ai_website/builder.html', context)


@login_required
def generate_website(request):
    """
    Handle website generation request
    Creates or updates the user's AI-generated website
    """
    if request.method != 'POST':
        return redirect('ai_website:builder')
    
    # Check if user has a business
    if not hasattr(request.user, 'business'):
        messages.error(request, 'Please register your business first.')
        return redirect('business:register')
    
    # Get form data
    business_name = request.POST.get('business_name', '').strip()
    ai_prompt = request.POST.get('ai_prompt', '').strip()
    
    # Validate input
    if not business_name or not ai_prompt:
        messages.error(request, 'Please provide both business name and AI prompt.')
        return redirect('ai_website:builder')
    
    try:
        # Get the user's business
        business = request.user.business
        
        # Generate HTML content using OpenAI API with full business context
        html_content = generate_website_with_openai(business, ai_prompt)
        
        # Create or update GeneratedWebsite record (slug will be auto-generated)
        website, created = GeneratedWebsite.objects.update_or_create(
            user=request.user,
            defaults={
                'business_name': business_name,
                'ai_prompt': ai_prompt,
                'is_published': True,
            }
        )
        
        # Save HTML file to media directory using the generated slug
        file_path = save_html_file(website.business_slug, html_content)
        
        # Update the file path
        website.html_file_path = file_path
        website.save(update_fields=['html_file_path'])
        
        if created:
            messages.success(request, f'Website generated successfully! View it at {website.get_public_url()}')
        else:
            messages.success(request, f'Website updated successfully! View it at {website.get_public_url()}')
        
        return redirect('ai_website:preview')
        
    except ValueError as e:
        # Handle configuration errors (e.g., missing API key)
        messages.error(request, str(e))
        return redirect('ai_website:builder')
    except Exception as e:
        # Handle OpenAI API errors or other exceptions
        messages.error(request, f'Error generating website: {str(e)}')
        return redirect('ai_website:builder')


@login_required
def preview_website(request):
    """
    Preview the user's generated website in an iframe
    """
    try:
        website = GeneratedWebsite.objects.get(user=request.user)
    except GeneratedWebsite.DoesNotExist:
        messages.warning(request, 'You need to generate a website first.')
        return redirect('ai_website:builder')
    
    context = {
        'website': website,
        'public_url': website.get_public_url(),
    }
    
    return render(request, 'ai_website/preview.html', context)


@login_required
def toggle_publish(request, website_id):
    """
    Toggle the published status of a website
    """
    if request.method == 'POST':
        website = get_object_or_404(GeneratedWebsite, id=website_id, user=request.user)
        
        website.is_published = not website.is_published
        website.save()
        
        status = "published" if website.is_published else "unpublished"
        messages.success(request, f'Website {status} successfully!')
        
        # Return JSON for AJAX requests
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest' or request.content_type == 'application/json':
            from django.http import JsonResponse
            return JsonResponse({
                'success': True,
                'is_published': website.is_published,
                'status': status
            })
        
        return redirect('ai_website:builder')
    
    return redirect('ai_website:builder')


@login_required
def delete_website(request, website_id):
    """
    Delete the user's generated website
    """
    website = get_object_or_404(GeneratedWebsite, id=website_id, user=request.user)
    
    # Delete the HTML file
    try:
        file_path = website.get_file_path()
        if os.path.exists(file_path):
            os.remove(file_path)
    except Exception as e:
        pass  # Continue even if file deletion fails
    
    website.delete()
    messages.success(request, 'Website deleted successfully!')
    
    return redirect('ai_website:builder')


def public_website(request, business_slug):
    """
    Serve the public website for a given business slug
    Accessible at domain.com/<business-slug>/
    
    Args:
        business_slug: URL-friendly slug of the business name (e.g., 'kashif-mehmood')
    """
    # Get website by business slug
    try:
        website = GeneratedWebsite.objects.get(business_slug=business_slug, is_published=True)
    except GeneratedWebsite.DoesNotExist:
        raise Http404("Website not found or not published")
    
    # Increment view count
    website.increment_view_count()
    
    # Read and serve the HTML file
    try:
        file_path = website.get_file_path()
        with open(file_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        return HttpResponse(html_content, content_type='text/html')
    
    except FileNotFoundError:
        raise Http404("Website file not found")
    except Exception as e:
        raise Http404(f"Error loading website: {str(e)}")
