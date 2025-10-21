# Business Landing Page System - Setup Guide

## Quick Start

Follow these steps to set up the business landing page system:

### Step 1: Run Migrations

```bash
python manage.py makemigrations business_page
python manage.py migrate
```

### Step 2: Setup Default Templates

```bash
python manage.py setup_page_templates
```

This creates Modern and Classic templates for all industries.

### Step 3: Access the Management Interface

Business owners can access their landing page management at:
```
http://your-domain.com/manage/
```

### Step 4: Publish Your First Page

1. Log in as a business owner
2. Navigate to `/manage/`
3. Select a template
4. Customize content and SEO settings
5. Add testimonials, gallery images, and FAQs
6. Preview your page
7. Click "Publish"

## URL Structure

- **Public Page**: `http://your-domain.com/{business-slug}/`
- **Management Dashboard**: `http://your-domain.com/manage/`
- **Preview**: `http://your-domain.com/preview/`

## Features Implemented

### ✅ Core Features

- [x] Multiple template support (Modern & Classic)
- [x] Customizable page sections
- [x] SEO optimization (meta tags)
- [x] Testimonials management
- [x] Gallery/portfolio images
- [x] FAQ management
- [x] Publishing control
- [x] Preview mode
- [x] Analytics (view count)
- [x] Responsive design
- [x] Industry-specific templates

### ✅ Architecture

- [x] Loosely coupled design
- [x] Standardized models
- [x] Optimized queries
- [x] Editable content via dashboard
- [x] Admin interface for superusers
- [x] RESTful API endpoints

## File Structure

```
business_page/
├── models.py                 # Database models
├── views.py                  # View logic
├── urls.py                   # URL routing
├── admin.py                  # Django admin configuration
├── management/
│   └── commands/
│       └── setup_page_templates.py  # Setup command
├── README.md                 # Detailed documentation
templates/business_page/
├── modern_template.html      # Modern design template
├── classic_template.html     # Classic design template
└── manage_page.html          # Management dashboard
static/
├── css/business_page/
│   └── manage_page.css       # Dashboard styles
└── js/business_page/
    └── manage_page.js        # Dashboard JavaScript
```

## Models Overview

### PageTemplate
- Stores template designs
- Can be industry-specific or universal
- Includes template file path and metadata

### BusinessPage
- One per business
- Links to a template
- Contains SEO settings
- Tracks publishing status and analytics

### PageSection
- Customizable page sections
- JSON content for flexibility
- Reorderable and toggleable

### Testimonial
- Customer reviews
- Rating system (1-5 stars)
- Approval workflow

### GalleryImage
- Portfolio/work images
- Categorization support
- Featured image option

### FAQ
- Question and answer pairs
- Categorization support
- Visibility control

## Template System

### Available Templates

1. **Modern Template** (`modern_template.html`)
   - Gradient backgrounds
   - Smooth animations
   - Card-based layouts
   - Inter font family
   - Indigo/purple color scheme

2. **Classic Template** (`classic_template.html`)
   - Serif typography (Playfair Display)
   - Gold accents (#d4af37)
   - Elegant borders
   - Traditional layout
   - Professional appearance

### Template Context

All templates receive:
- `business_page` - BusinessPage object
- `business` - Business object
- `sections` - Visible page sections
- `testimonials` - Approved testimonials
- `gallery_images` - Gallery images
- `faqs` - Visible FAQs
- `services` - Active service offerings

## Customization Guide

### Adding a New Template

1. Create HTML file in `templates/business_page/`
2. Use TailwindCSS for styling
3. Include Font Awesome for icons
4. Create PageTemplate record:

```python
from business_page.models import PageTemplate

PageTemplate.objects.create(
    name='My Template',
    template_type='custom',
    template_file='business_page/my_template.html',
    industry=None,  # or specific industry
    is_active=True
)
```

### Customizing Section Content

Sections use JSON for flexible content. Example:

```python
from business_page.models import PageSection

section = PageSection.objects.create(
    business_page=business_page,
    section_type='hero',
    title='Welcome',
    content={
        'heading': 'Your Heading Here',
        'subheading': 'Your subheading',
        'cta_text': 'Get Started',
        'background_image': 'https://...'
    },
    display_order=0,
    is_visible=True
)
```

## API Usage

### Update Page Settings

```javascript
fetch('/settings/update/', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': getCookie('csrftoken')
    },
    body: JSON.stringify({
        template_id: 'tmpl_xxx',
        slug: 'my-business',
        meta_title: 'My Business - Best Services',
        meta_description: 'We provide...',
        is_published: true
    })
})
```

### Add Testimonial

```javascript
fetch('/testimonials/add/', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': getCookie('csrftoken')
    },
    body: JSON.stringify({
        customer_name: 'John Doe',
        customer_title: 'Homeowner',
        rating: 5,
        testimonial_text: 'Excellent service!',
        is_featured: true
    })
})
```

## Best Practices

### Content
- Keep hero headings under 10 words
- Meta descriptions should be 150-160 characters
- Use high-quality images (min 1200px wide)
- Write testimonials in customer's voice

### SEO
- Include target keywords in meta title
- Use unique meta descriptions for each page
- Add alt text to all images
- Keep URLs short and descriptive

### Performance
- Use CDN for images
- Optimize image sizes
- Minimize custom CSS
- Test on mobile devices

## Troubleshooting

### Issue: Page not accessible
**Solution**: Check `is_published` is True and slug is unique

### Issue: Template not loading
**Solution**: Verify template file path in PageTemplate model

### Issue: Sections not showing
**Solution**: Check `is_visible` is True and content is valid JSON

### Issue: Images not displaying
**Solution**: Ensure image URLs are publicly accessible

## Next Steps

1. Run migrations: `python manage.py makemigrations && python manage.py migrate`
2. Setup templates: `python manage.py setup_page_templates`
3. Create test business page
4. Customize content
5. Publish and test

## Support

For detailed documentation, see `business_page/README.md`

For issues or questions, check:
- Model definitions in `business_page/models.py`
- View logic in `business_page/views.py`
- Template examples in `templates/business_page/`
