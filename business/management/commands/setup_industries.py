import json
from django.core.management.base import BaseCommand
from django.utils.text import slugify
from business.models import Industry, IndustryField, IndustryPrompt

class Command(BaseCommand):
    help = 'Set up initial industries and their default fields'

    def handle(self, *args, **options):
        # Define the industries and their fields
        industries_data = {
            'cleaning': {
                'name': 'Cleaning Services',
                'description': 'Residential and commercial cleaning services',
                'icon': 'fa-broom',
                'fields': [
                    {
                        'name': 'Square Footage',
                        'field_type': 'number',
                        'required': True,
                        'placeholder': 'Enter the square footage of the property',
                        'help_text': 'This helps us estimate the cleaning time and cost',
                        'display_order': 1,
                    },
                    {
                        'name': 'Property Type',
                        'field_type': 'select',
                        'options': json.dumps(['Residential', 'Commercial', 'Industrial']),
                        'required': True,
                        'placeholder': 'Select property type',
                        'display_order': 2,
                    },
                    {
                        'name': 'Number of Bedrooms',
                        'field_type': 'number',
                        'required': False,
                        'placeholder': 'Number of bedrooms (for residential only)',
                        'display_order': 3,
                    },
                    {
                        'name': 'Number of Bathrooms',
                        'field_type': 'number',
                        'required': False,
                        'placeholder': 'Number of bathrooms',
                        'display_order': 4,
                    },
                    {
                        'name': 'Cleaning Type',
                        'field_type': 'select',
                        'options': json.dumps(['Regular', 'Deep Clean', 'Move-in/Move-out', 'Post-Construction']),
                        'required': True,
                        'placeholder': 'Select cleaning type',
                        'display_order': 5,
                    },
                    {
                        'name': 'Special Instructions',
                        'field_type': 'textarea',
                        'required': False,
                        'placeholder': 'Any special instructions or requirements',
                        'display_order': 6,
                    },
                ],
                'prompts': [
                    {
                        'name': 'Initial Contact',
                        'description': 'Prompt for initial contact with cleaning service leads',
                        'prompt_text': """You are an AI assistant for a cleaning service company. 
                        Your goal is to gather information about the client's cleaning needs and schedule an appointment.
                        Ask about: property type, square footage, number of rooms, cleaning frequency, and preferred date/time.
                        Be professional, friendly, and helpful. Provide brief information about our services when relevant.""",
                        'version': '1.0',
                    },
                    {
                        'name': 'Follow-up',
                        'description': 'Prompt for follow-up with leads who haven\'t responded',
                        'prompt_text': """You are following up with a potential client who inquired about cleaning services.
                        Remind them of their previous inquiry and ask if they're still interested.
                        Offer a special discount for booking within the next 48 hours.
                        Be friendly but not pushy.""",
                        'version': '1.0',
                    }
                ]
            },
            'roofing': {
                'name': 'Roofing Services',
                'description': 'Residential and commercial roofing installation and repair',
                'icon': 'fa-home',
                'fields': [
                    {
                        'name': 'Roof Size',
                        'field_type': 'number',
                        'required': True,
                        'placeholder': 'Approximate roof size in square feet',
                        'help_text': 'This helps us estimate materials and cost',
                        'display_order': 1,
                    },
                    {
                        'name': 'Property Type',
                        'field_type': 'select',
                        'options': json.dumps(['Residential', 'Commercial', 'Industrial']),
                        'required': True,
                        'placeholder': 'Select property type',
                        'display_order': 2,
                    },
                    {
                        'name': 'Service Type',
                        'field_type': 'select',
                        'options': json.dumps(['Repair', 'Replacement', 'New Installation', 'Inspection']),
                        'required': True,
                        'placeholder': 'Select service type',
                        'display_order': 3,
                    },
                    {
                        'name': 'Roof Type',
                        'field_type': 'select',
                        'options': json.dumps(['Asphalt Shingle', 'Metal', 'Tile', 'Flat/Low Slope', 'Other']),
                        'required': True,
                        'placeholder': 'Select roof type',
                        'display_order': 4,
                    },
                    {
                        'name': 'Issue Description',
                        'field_type': 'textarea',
                        'required': False,
                        'placeholder': 'Describe any issues or damage (leaks, missing shingles, etc.)',
                        'display_order': 5,
                    },
                    {
                        'name': 'Building Age',
                        'field_type': 'number',
                        'required': False,
                        'placeholder': 'Approximate age of the building in years',
                        'display_order': 6,
                    },
                ],
                'prompts': [
                    {
                        'name': 'Initial Contact',
                        'description': 'Prompt for initial contact with roofing service leads',
                        'prompt_text': """You are an AI assistant for a roofing company. 
                        Your goal is to gather information about the client's roofing needs and schedule an inspection.
                        Ask about: property type, roof size, current issues, roof age, and preferred date for inspection.
                        Be professional, knowledgeable, and emphasize safety and quality. Mention our free inspection service.""",
                        'version': '1.0',
                    },
                    {
                        'name': 'Emergency Response',
                        'description': 'Prompt for emergency roofing situations',
                        'prompt_text': """You are responding to an emergency roofing situation.
                        Express concern and urgency. Ask about the nature of the emergency (leak, storm damage, etc.).
                        Gather essential information for our emergency response team.
                        Assure the client that we have 24/7 emergency services and will dispatch a team as soon as possible.""",
                        'version': '1.0',
                    }
                ]
            },
            'salon': {
                'name': 'Salon Services',
                'description': 'Hair, nail, and beauty salon services',
                'icon': 'fa-cut',
                'fields': [
                    {
                        'name': 'Service Type',
                        'field_type': 'select',
                        'options': json.dumps(['Haircut', 'Hair Coloring', 'Styling', 'Manicure/Pedicure', 'Facial', 'Waxing', 'Other']),
                        'required': True,
                        'placeholder': 'Select service type',
                        'display_order': 1,
                    },
                    {
                        'name': 'Preferred Stylist',
                        'field_type': 'text',
                        'required': False,
                        'placeholder': 'Enter preferred stylist name (if any)',
                        'display_order': 2,
                    },
                    {
                        'name': 'Current Hair Length',
                        'field_type': 'select',
                        'options': json.dumps(['Short', 'Medium', 'Long', 'Not Applicable']),
                        'required': False,
                        'placeholder': 'Select current hair length',
                        'display_order': 3,
                    },
                    {
                        'name': 'Special Requests',
                        'field_type': 'textarea',
                        'required': False,
                        'placeholder': 'Any special requests or references',
                        'display_order': 4,
                    },
                    {
                        'name': 'First-time Client',
                        'field_type': 'boolean',
                        'required': True,
                        'display_order': 5,
                    },
                ],
                'prompts': [
                    {
                        'name': 'Initial Contact',
                        'description': 'Prompt for initial contact with salon service leads',
                        'prompt_text': """You are an AI assistant for a beauty salon. 
                        Your goal is to understand the client's beauty needs and schedule an appointment.
                        Ask about: desired service, preferred stylist, any references/inspiration photos, and preferred date/time.
                        Be friendly, stylish, and make the client feel special. Mention our new client discount if applicable.""",
                        'version': '1.0',
                    },
                    {
                        'name': 'Follow-up',
                        'description': 'Prompt for follow-up with salon clients',
                        'prompt_text': """You are following up with a client after their salon visit.
                        Ask about their experience and satisfaction with the service.
                        Mention our loyalty program and upcoming promotions.
                        Suggest booking their next appointment to maintain their style.""",
                        'version': '1.0',
                    }
                ]
            },
            'dental': {
                'name': 'Dental Services',
                'description': 'General and specialized dental care services',
                'icon': 'fa-tooth',
                'fields': [
                    {
                        'name': 'Service Type',
                        'field_type': 'select',
                        'options': json.dumps(['Check-up/Cleaning', 'Filling', 'Root Canal', 'Crown/Bridge', 'Extraction', 'Whitening', 'Orthodontics', 'Emergency', 'Other']),
                        'required': True,
                        'placeholder': 'Select service type',
                        'display_order': 1,
                    },
                    {
                        'name': 'Insurance Provider',
                        'field_type': 'text',
                        'required': False,
                        'placeholder': 'Enter dental insurance provider (if any)',
                        'display_order': 2,
                    },
                    {
                        'name': 'Previous Patient',
                        'field_type': 'boolean',
                        'required': True,
                        'display_order': 3,
                    },
                    {
                        'name': 'Pain Level',
                        'field_type': 'select',
                        'options': json.dumps(['None', 'Mild', 'Moderate', 'Severe']),
                        'required': False,
                        'placeholder': 'Current pain level (if applicable)',
                        'display_order': 4,
                    },
                    {
                        'name': 'Medical Conditions',
                        'field_type': 'textarea',
                        'required': False,
                        'placeholder': 'List any relevant medical conditions or allergies',
                        'display_order': 5,
                    },
                ],
                'prompts': [
                    {
                        'name': 'Initial Contact',
                        'description': 'Prompt for initial contact with dental service leads',
                        'prompt_text': """You are an AI assistant for a dental practice. 
                        Your goal is to understand the patient's dental needs and schedule an appointment.
                        Ask about: reason for visit, any pain or discomfort, insurance information, and preferred date/time.
                        Be professional, compassionate, and reassuring. Emphasize our gentle approach to dental care.""",
                        'version': '1.0',
                    },
                    {
                        'name': 'Emergency Response',
                        'description': 'Prompt for dental emergencies',
                        'prompt_text': """You are responding to a dental emergency.
                        Express concern and gather information about the nature of the emergency.
                        Provide basic first-aid advice appropriate to the situation.
                        Arrange for the earliest possible emergency appointment.
                        Reassure the patient and emphasize that help is on the way.""",
                        'version': '1.0',
                    }
                ]
            }
        }

        # Create the industries and their fields
        for industry_key, industry_data in industries_data.items():
            self.stdout.write(f"Setting up {industry_data['name']}...")
            
            # Create or update the industry
            industry, created = Industry.objects.update_or_create(
                slug=slugify(industry_key),
                defaults={
                    'name': industry_data['name'],
                    'description': industry_data['description'],
                    'icon': industry_data['icon'],
                }
            )
            
            if created:
                self.stdout.write(self.style.SUCCESS(f"Created industry: {industry.name}"))
            else:
                self.stdout.write(self.style.SUCCESS(f"Updated industry: {industry.name}"))
            
            # Create the industry fields
            for field_data in industry_data['fields']:
                field, field_created = IndustryField.objects.update_or_create(
                    industry=industry,
                    slug=slugify(field_data['name']),
                    defaults={
                        'name': field_data['name'],
                        'field_type': field_data['field_type'],
                        'required': field_data['required'],
                        'placeholder': field_data.get('placeholder', ''),
                        'help_text': field_data.get('help_text', ''),
                        'options': field_data.get('options', None),
                        'display_order': field_data['display_order'],
                    }
                )
                
                if field_created:
                    self.stdout.write(f"  Created field: {field.name}")
                else:
                    self.stdout.write(f"  Updated field: {field.name}")
            
            # Create the industry prompts
            for prompt_data in industry_data['prompts']:
                prompt, prompt_created = IndustryPrompt.objects.update_or_create(
                    industry=industry,
                    name=prompt_data['name'],
                    version=prompt_data['version'],
                    defaults={
                        'description': prompt_data['description'],
                        'prompt_text': prompt_data['prompt_text'],
                    }
                )
                
                if prompt_created:
                    self.stdout.write(f"  Created prompt: {prompt.name} (v{prompt.version})")
                else:
                    self.stdout.write(f"  Updated prompt: {prompt.name} (v{prompt.version})")
            
        self.stdout.write(self.style.SUCCESS("Industry setup completed successfully!"))
