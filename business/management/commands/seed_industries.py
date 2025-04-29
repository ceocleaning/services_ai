from django.core.management.base import BaseCommand
from django.db import transaction
from business.models import Industry, IndustryField


class Command(BaseCommand):
    help = 'Seeds the database with industries and their default fields'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting to seed industries and their fields...'))
        
        # Define industries with their fields
        industries_data = [
            {
                'name': 'Cleaning Services',
                'slug': 'cleaning-services',
                'description': 'Professional cleaning services for homes and businesses',
                'fields': [
                    {
                        'name': 'Property Size',
                        'slug': 'property-size',
                        'field_type': 'number',
                        'required': True,
                        'display_order': 1,
                        'help_text': 'Size of the property in square feet',
                    },
                    {
                        'name': 'Number of Rooms',
                        'slug': 'number-of-rooms',
                        'field_type': 'number',
                        'required': True,
                        'display_order': 2,
                        'help_text': 'Total number of rooms to be cleaned',
                    },
                    {
                        'name': 'Cleaning Type',
                        'slug': 'cleaning-type',
                        'field_type': 'select',
                        'options': {'choices': ['Standard', 'Deep Clean', 'Move-in/Move-out']},
                        'required': True,
                        'display_order': 3,
                        'help_text': 'Type of cleaning service needed',
                    },
                    {
                        'name': 'Special Instructions',
                        'slug': 'special-instructions',
                        'field_type': 'text',
                        'required': False,
                        'display_order': 4,
                        'help_text': 'Any special instructions or areas that need attention',
                    },
                ]
            },
            {
                'name': 'Salon & Beauty',
                'slug': 'salon-beauty',
                'description': 'Hair, nail, and beauty services for all clients',
                'fields': [
                    {
                        'name': 'Service Type',
                        'slug': 'service-type',
                        'field_type': 'select',
                        'options': {'choices': ['Haircut', 'Color', 'Styling', 'Manicure', 'Pedicure', 'Facial', 'Massage']},
                        'required': True,
                        'display_order': 1,
                        'help_text': 'Type of beauty service needed',
                    },
                    {
                        'name': 'Hair Length',
                        'slug': 'hair-length',
                        'field_type': 'select',
                        'options': {'choices': ['Short', 'Medium', 'Long']},
                        'required': False,
                        'display_order': 2,
                        'help_text': 'Length of hair (for hair services)',
                    },
                    {
                        'name': 'Stylist Preference',
                        'slug': 'stylist-preference',
                        'field_type': 'text',
                        'required': False,
                        'display_order': 3,
                        'help_text': 'Preferred stylist name (if any)',
                    },
                    {
                        'name': 'Special Requests',
                        'slug': 'special-requests',
                        'field_type': 'text',
                        'required': False,
                        'display_order': 4,
                        'help_text': 'Any special requests or considerations',
                    },
                ]
            },
            {
                'name': 'Legal Services',
                'slug': 'legal-services',
                'description': 'Professional legal consultation and representation',
                'fields': [
                    {
                        'name': 'Case Type',
                        'slug': 'case-type',
                        'field_type': 'select',
                        'options': {'choices': ['Family Law', 'Criminal Defense', 'Estate Planning', 'Business Law', 'Personal Injury', 'Immigration', 'Real Estate']},
                        'required': True,
                        'display_order': 1,
                        'help_text': 'Type of legal case or service needed',
                    },
                    {
                        'name': 'Urgency',
                        'slug': 'urgency',
                        'field_type': 'select',
                        'options': {'choices': ['Routine', 'Urgent', 'Emergency']},
                        'required': True,
                        'display_order': 2,
                        'help_text': 'How urgent is your legal matter',
                    },
                    {
                        'name': 'Case Description',
                        'slug': 'case-description',
                        'field_type': 'text',
                        'required': True,
                        'display_order': 3,
                        'help_text': 'Brief description of your legal situation',
                    },
                    {
                        'name': 'Attorney Preference',
                        'slug': 'attorney-preference',
                        'field_type': 'text',
                        'required': False,
                        'display_order': 4,
                        'help_text': 'Preferred attorney (if any)',
                    },
                ]
            },
            {
                'name': 'Home Services',
                'slug': 'home-services',
                'description': 'Repair, maintenance, and improvement services for your home',
                'fields': [
                    {
                        'name': 'Service Category',
                        'slug': 'service-category',
                        'field_type': 'select',
                        'options': {'choices': ['Plumbing', 'Electrical', 'HVAC', 'Carpentry', 'Painting', 'Landscaping', 'Roofing', 'General Repair']},
                        'required': True,
                        'display_order': 1,
                        'help_text': 'Category of home service needed',
                    },
                    {
                        'name': 'Property Type',
                        'slug': 'property-type',
                        'field_type': 'select',
                        'options': {'choices': ['House', 'Apartment', 'Condo', 'Townhouse', 'Commercial']},
                        'required': True,
                        'display_order': 2,
                        'help_text': 'Type of property requiring service',
                    },
                    {
                        'name': 'Issue Description',
                        'slug': 'issue-description',
                        'field_type': 'text',
                        'required': True,
                        'display_order': 3,
                        'help_text': 'Detailed description of the issue or project',
                    },
                    {
                        'name': 'Emergency Service',
                        'slug': 'emergency-service',
                        'field_type': 'boolean',
                        'required': False,
                        'display_order': 4,
                        'help_text': 'Is this an emergency requiring immediate attention?',
                    },
                ]
            },
        ]
        
        # Use a transaction to ensure data integrity
        with transaction.atomic():
            # Create industries and their fields
            for industry_data in industries_data:
                fields = industry_data.pop('fields')
                
                # Create or update industry
                industry, created = Industry.objects.update_or_create(
                    slug=industry_data['slug'],
                    defaults=industry_data
                )
                
                action = 'Created' if created else 'Updated'
                self.stdout.write(self.style.SUCCESS(f'{action} industry: {industry.name}'))
                
                # Create or update fields for this industry
                for field_data in fields:
                    field, created = IndustryField.objects.update_or_create(
                        industry=industry,
                        slug=field_data['slug'],
                        defaults=field_data
                    )
                    
                    action = 'Created' if created else 'Updated'
                    self.stdout.write(f'  {action} field: {field.name}')
        
        self.stdout.write(self.style.SUCCESS('Successfully seeded industries and their fields!'))
