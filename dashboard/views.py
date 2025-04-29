from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages


@login_required
def index(request):
    """
    Render the dashboard index page
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
    
    return render(request, 'dashboard/index.html', context)
