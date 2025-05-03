from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import RetellAgent

# Create your views here.
@login_required
def index(request):
    agents = RetellAgent.objects.filter(business=request.user.business)
    return render(request, 'retell_agent/index.html', {
        'title': 'Retell Agents',
        'agents': agents,
    })

@login_required
def create_agent(request):
    error_message = None
    agent_name_error = None
    retell_agent_id_error = None
    retell_phone_number_error = None
    
    if request.method == 'POST':
        agent_name = request.POST.get('agent_name', '').strip()
        retell_agent_id = request.POST.get('retell_agent_id', '').strip()
        retell_phone_number = request.POST.get('retell_phone_number', '').strip()
        
        # Validate input
        is_valid = True
        
        if not agent_name:
            agent_name_error = "Agent name is required"
            is_valid = False
        
        if not retell_agent_id:
            retell_agent_id_error = "Retell Agent ID is required"
            is_valid = False
        
        if not retell_phone_number:
            retell_phone_number_error = "Phone number is required"
            is_valid = False
        elif not retell_phone_number.startswith('+'):
            retell_phone_number_error = "Phone number must start with + and country code (e.g., +1234567890)"
            is_valid = False
        
        if is_valid:
            # Create new agent
            agent = RetellAgent(
                business=request.user.business,
                agent_name=agent_name,
                retell_agent_id=retell_agent_id,
                retell_phone_number=retell_phone_number
            )
            agent.save()
            
            messages.success(request, 'Retell Agent created successfully!')
            return redirect('retell_agent:index')
    
    context = {
        'error_message': error_message,
        'agent_name_error': agent_name_error,
        'retell_agent_id_error': retell_agent_id_error,
        'retell_phone_number_error': retell_phone_number_error,
    }
    
    return render(request, 'retell_agent/form.html', context)

@login_required
def edit_agent(request, agent_id):
    agent = get_object_or_404(RetellAgent, id=agent_id, business=request.user.business)
    
    error_message = None
    agent_name_error = None
    retell_agent_id_error = None
    retell_phone_number_error = None
    
    if request.method == 'POST':
        agent_name = request.POST.get('agent_name', '').strip()
        retell_agent_id = request.POST.get('retell_agent_id', '').strip()
        retell_phone_number = request.POST.get('retell_phone_number', '').strip()
        
        # Validate input
        is_valid = True
        
        if not agent_name:
            agent_name_error = "Agent name is required"
            is_valid = False
        
        if not retell_agent_id:
            retell_agent_id_error = "Retell Agent ID is required"
            is_valid = False
        
        if not retell_phone_number:
            retell_phone_number_error = "Phone number is required"
            is_valid = False
        elif not retell_phone_number.startswith('+'):
            retell_phone_number_error = "Phone number must start with + and country code (e.g., +1234567890)"
            is_valid = False
        
        if is_valid:
            # Update agent
            agent.agent_name = agent_name
            agent.retell_agent_id = retell_agent_id
            agent.retell_phone_number = retell_phone_number
            agent.save()
            
            messages.success(request, 'Retell Agent updated successfully!')
            return redirect('retell_agent:index')
    
    context = {
        'agent': agent,
        'error_message': error_message,
        'agent_name_error': agent_name_error,
        'retell_agent_id_error': retell_agent_id_error,
        'retell_phone_number_error': retell_phone_number_error,
    }
    
    return render(request, 'retell_agent/form.html', context)

@login_required
def delete_agent(request, agent_id):
    agent = get_object_or_404(RetellAgent, id=agent_id, business=request.user.business)
    agent.delete()
    messages.success(request, 'Retell Agent deleted successfully!')
    return redirect('retell_agent:index')
