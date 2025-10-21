"""
OpenAI Service for AI Website Builder
Handles all OpenAI API interactions for generating business websites
"""

from openai import OpenAI
from django.conf import settings
import json
from .utils import get_business_context, build_system_prompt, build_user_prompt


# All prompt building functions have been moved to utils.py for DRY principles
# This allows both OpenAI and Gemini services to use the same prompts


def generate_website_with_openai(business, ai_prompt, existing_html=None):
    """
    Generate a complete website using OpenAI API
    
    Args:
        business: Business model instance
        ai_prompt: User's custom prompt/requirements
        existing_html: Optional existing HTML content for iterative improvements
        
    Returns:
        str: Generated HTML content
        
    Raises:
        Exception: If OpenAI API call fails
    """
    # Check if OpenAI API key is configured
    if not settings.OPENAI_API_KEY:
        raise ValueError("OpenAI API key is not configured. Please set OPENAI_API_KEY in your environment variables.")
    
    # Initialize OpenAI client
    client = OpenAI(api_key=settings.OPENAI_API_KEY)
    
    # Get business context
    business_context = get_business_context(business)
    
    # Build prompts using centralized functions from utils
    system_prompt = build_system_prompt()
    user_prompt = build_user_prompt(business_context, ai_prompt)
    
    # If existing HTML is provided, modify the user prompt for iterative improvement
    if existing_html:
        user_prompt = f"""{user_prompt}

**📄 EXISTING WEBSITE HTML:**
You are modifying an EXISTING website. Below is the current HTML code. Make the requested changes while preserving the overall structure and design unless specifically asked to change it.

```html
{existing_html}  
```

**IMPORTANT INSTRUCTIONS FOR MODIFICATION:**
1. Keep the existing design style, color scheme, and layout UNLESS the user specifically asks to change them
2. Only modify the parts that the user requested to change
3. Preserve all existing sections that weren't mentioned in the request
4. Maintain consistency with the existing design language
5. If adding new sections, match the style of existing sections
6. Return the COMPLETE modified HTML (not just the changed parts)

Now, apply the following changes: {ai_prompt}"""
    
    try:
        # Call OpenAI API
        response = client.chat.completions.create(
            model="gpt-4o",  # Using GPT-4o for best quality
            messages=[
                {
                    "role": "system",
                    "content": system_prompt
                },
                {
                    "role": "user",
                    "content": user_prompt
                }
            ],
            temperature=0.7,
            max_tokens=16000
        )
        
        # Extract HTML content
        html_content = response.choices[0].message.content
        
        # Clean up markdown code blocks if present
        if "```html" in html_content:
            html_content = html_content.split("```html")[1].split("```")[0].strip()
        elif "```" in html_content:
            html_content = html_content.split("```")[1].split("```")[0].strip()
        
        return html_content
        
    except Exception as e:
        raise Exception(f"OpenAI API error: {str(e)}")


def estimate_cost(business):
    """
    Estimate the cost of generating a website for a business
    
    Args:
        business: Business model instance
        
    Returns:
        dict: Cost estimation details
    """
    # Rough token estimation
    # System prompt: ~2000 tokens
    # User prompt with business data: ~1500 tokens
    # Response (HTML): ~12000 tokens
    
    estimated_input_tokens = 3500
    estimated_output_tokens = 12000
    
    # GPT-4o pricing (as of 2024)
    # Input: $0.03 per 1K tokens
    # Output: $0.06 per 1K tokens
    
    input_cost = (estimated_input_tokens / 1000) * 0.03
    output_cost = (estimated_output_tokens / 1000) * 0.06
    total_cost = input_cost + output_cost
    
    return {
        'estimated_input_tokens': estimated_input_tokens,
        'estimated_output_tokens': estimated_output_tokens,
        'estimated_cost_usd': round(total_cost, 4),
        'model': 'gpt-4o'
    }
