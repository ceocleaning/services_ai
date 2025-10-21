"""
AI Service Router
Routes website generation requests to the appropriate AI service (OpenAI or Gemini)
based on business configuration
"""

from .openai_service import generate_website_with_openai
from .gemini_service import generate_website_with_gemini


def generate_website(business, ai_prompt, existing_html=None):
    """
    Generate a website using the business's preferred AI model
    
    Args:
        business: Business model instance
        ai_prompt: User's custom prompt/requirements
        existing_html: Optional existing HTML content for iterative improvements
        
    Returns:
        tuple: (html_content, model_used)
        
    Raises:
        Exception: If generation fails
    """
    # Get business configuration
    try:
        config = business.configuration
        ai_model = config.ai_model_preference
    except:
        # Default to OpenAI if no configuration exists
        ai_model = 'openai'
    
    # Route to appropriate service
    if ai_model == 'gemini':
        try:
            html_content = generate_website_with_gemini(business, ai_prompt, existing_html)
            return html_content, 'Google Gemini 2.5 Pro'
        except Exception as e:
            # Fallback to OpenAI if Gemini fails
            print(f"Gemini failed, falling back to OpenAI: {str(e)}")
            html_content = generate_website_with_openai(business, ai_prompt, existing_html)
            return html_content, 'OpenAI GPT-4o (Fallback)'
    else:
        html_content = generate_website_with_openai(business, ai_prompt, existing_html)
        return html_content, 'OpenAI GPT-4o'


def get_available_models():
    """
    Get list of available AI models
    
    Returns:
        list: List of tuples (value, label)
    """
    return [
        ('openai', 'OpenAI GPT-4o'),
        ('gemini', 'Google Gemini 2.5 Pro'),
    ]
