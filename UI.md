## 3. Page-Specific Designs

### 3.1 Public Pages (base.html)

#### 3.1.1 Landing Page
- **Hero Section**:
  - Gradient background with subtle pattern (varies by industry)
  - Main value proposition headline
  - Concise subheadline
  - Primary CTA button
  - Responsive illustration/animation (related to AI communication)
  - Mobile: Stacked layout with simplified illustration
  - Desktop: Split layout with larger illustration

- **Features Section**:
  - 3-column grid of feature cards (stacked on mobile)
  - Each with icon, heading, description
  - Subtle hover effects
  - Consistent vertical spacing

- **Industries Section**:
  - Tabbed interface showing industry-specific benefits
  - Visual examples of customized workflows
  - Mobile-optimized tab UI with horizontal scroll
  - Desktop: Full-width display with larger visuals

- **Testimonials Section**:
  - Carousel with client quotes and logos
  - Star ratings where applicable
  - Mobile: Single testimonial view with swipe
  - Desktop: Multiple testimonials visible

- **Pricing Section**:
  - Clearly defined tiers
  - Feature comparison
  - Highlighted recommended plan
  - Mobile: Stacked card layout
  - Desktop: Side-by-side comparison

- **CTA Section**:
  - Contrasting background color
  - Strong headline
  - Simple form or button
  - Trust indicators below

#### 3.1.2 About Page
- **Team Story**:
  - Brief company narrative
  - Mission statement
  - Timeline of milestones (horizontal on desktop, vertical on mobile)

- **Team Section**:
  - Grid of team members
  - Mobile: 1-2 columns
  - Desktop: 3-4 columns
  - Consistent card height
  - Optional hover effect revealing more details

#### 3.1.3 Contact Page
- **Contact Form**:
  - Clean, focused layout
  - Minimal required fields
  - Clear submit button
  - Success/error handling with toast
  - Mobile: Full-width stacked fields
  - Desktop: Two-column layout for shorter fields

- **Contact Information**:
  - Address with embedded map
  - Phone with click-to-call
  - Email with click-to-email
  - Social media links with icons

### 3.2 Authentication Pages (auth_base.html)

#### 3.2.1 Login Page
- **Form Card**:
  - Centered on page with brand-colored accent
  - Email/username and password fields
  - "Remember me" checkbox
  - Prominent login button
  - "Forgot password" link
  - Alternative login methods (if applicable)
  - Mobile: Full-width card, simplified visuals
  - Desktop: Fixed-width card (max 480px), rich visuals

- **Secondary Actions**:
  - "Don't have an account?" with signup link
  - Help or support link
  - Return to home link

#### 3.2.2 Signup Page
- **Form Layout**:
  - Step indicator for multi-step process
  - Clear field validation with inline feedback
  - Industry selection with visual cues
  - Mobile: Single column, progressive disclosure of fields
  - Desktop: Two columns where appropriate

- **Information Sections**:
  - Expandable sections for terms, privacy policy
  - Tooltip help text for complex fields
  - Contextual validation messages

#### 3.2.3 Password Reset Flow
- **Request Page**:
  - Simple email field
  - Clear instructions
  - Success notification via toast

- **Reset Page**:
  - Password and confirm password fields
  - Password strength indicator
  - Success notification and redirect to login

### 3.3 Dashboard Pages (dashboard_base.html)

#### 3.3.1 Dashboard Home
- **Layout**:
  - Mobile: Stacked full-width cards
  - Tablet: Two-column grid for key metrics
  - Desktop: Responsive grid with 3-4 columns

- **Components**:
  - Key metrics cards with comparisons to previous period
  - Recent leads table (responsive, simplified on mobile)
  - Upcoming appointments card with quick-action buttons
  - Conversion funnel chart (simplified visualization on mobile)# UI Design Specifications
# AI-Powered Appointment Assistant

## 1. Design Philosophy

### 1.1 Core Principles
- **Trust-Building**: The design must establish credibility and trust for businesses and their clients
- **Efficiency**: Interfaces should minimize clicks and streamline workflows
- **Clarity**: Information must be presented clearly with intuitive navigation
- **Flexibility**: The design must adapt to different industries while maintaining consistency
- **Accessibility**: All interfaces must be accessible to users with disabilities
- **Mobile-First**: All interfaces must be designed primarily for mobile devices, then scaled up to desktop

### 1.2 Brand Personality
- **Professional**: Conveys reliability and competence
- **Friendly**: Approachable but not casual
- **Intelligent**: Reflects the AI capabilities without appearing intimidating
- **Efficient**: Suggests time-saving and automation

## 2. Design System

### 2.1 Typography

#### 2.1.1 Font Families
- **Primary Font**: Outfit (sans-serif)
  - Headers: Outfit Medium/Semi-Bold
  - Body: Outfit Regular
  - Small text/captions: Outfit Light
- **Secondary Font**: JetBrains Mono (monospace)
  - Used for code examples, technical information, and data displays
  - Available weights: Regular and Medium

#### 2.1.2 Font Sizes
- **Base size**: 16px (1rem)
- **Scale**: 1.2 ratio
- **Hierarchy**:
  - H1: 2.074rem (33.18px)
  - H2: 1.728rem (27.65px)
  - H3: 1.44rem (23.04px)
  - H4: 1.2rem (19.2px)
  - Body: 1rem (16px)
  - Small/Caption: 0.833rem (13.33px)

#### 2.1.3 Line Heights
- Headers: 1.3
- Body text: 1.6
- Small text: 1.5

### 2.2 Color Palette

#### 2.2.1 Primary Colors
- **Primary Indigo**: #4F46E5 (HSL: 243, 75%, 59%)
  - Light: #E0E7FF (HSL: 243, 100%, 93%)
  - Medium Light: #A5B4FC (HSL: 243, 94%, 82%)
  - Medium Dark: #4338CA (HSL: 243, 75%, 50%)
  - Dark: #312E81 (HSL: 243, 48%, 34%)

#### 2.2.2 Secondary Colors
- **Secondary Teal**: #0CA5E9 (HSL: 198, 93%, 48%)
  - Light: #BAE6FD (HSL: 198, 93%, 86%)
  - Medium Light: #38BDF8 (HSL: 198, 93%, 60%)
  - Medium Dark: #0369A1 (HSL: 198, 96%, 32%)
  - Dark: #075985 (HSL: 198, 86%, 28%)

#### 2.2.3 Neutral Colors
- **Gray**: #6B7280 (HSL: 220, 9%, 46%)
  - Lightest: #F8FAFC (HSL: 214, 15%, 98%)
  - Light: #F1F5F9 (HSL: 210, 20%, 96%)
  - Medium Light: #E2E8F0 (HSL: 214, 32%, 91%)
  - Medium: #CBD5E1 (HSL: 214, 32%, 84%)
  - Medium Dark: #475569 (HSL: 215, 25%, 35%)
  - Dark: #1E293B (HSL: 217, 33%, 18%)
  - Darkest: #0F172A (HSL: 222, 47%, 11%)

#### 2.2.4 Semantic Colors
- **Success**: #10B981 (HSL: 158, 84%, 39%)
  - Light: #D1FAE5 (HSL: 156, 71%, 90%)
- **Warning**: #F59E0B (HSL: 38, 92%, 50%)
  - Light: #FEF3C7 (HSL: 48, 96%, 89%)
- **Error**: #EF4444 (HSL: 0, 84%, 60%)
  - Light: #FEE2E2 (HSL: 0, 86%, 94%)
- **Info**: #3B82F6 (HSL: 217, 91%, 60%)
  - Light: #DBEAFE (HSL: 214, 95%, 93%)

#### 2.2.5 Industry-Specific Accent Colors
- **Cleaning Services**: #14B8A6 (Teal)
- **Real Estate**: #8B5CF6 (Purple)
- **Home Services**: #F97316 (Orange)
- **Wellness**: #06B6D4 (Cyan)

#### 2.2.6 Dark Mode Colors
- **Dark Background**: #0F172A (Darkest Gray)
- **Dark Surface**: #1E293B (Dark Gray)
- **Dark Surface Elevated**: #334155 (Medium Dark Gray)
- **Dark Primary**: #818CF8 (HSL: 243, 90%, 74%)
- **Dark Secondary**: #38BDF8 (HSL: 198, 93%, 60%)
- **Dark Border**: #475569 (Medium Dark Gray)
- **Dark Text Primary**: #F1F5F9 (Light Gray)
- **Dark Text Secondary**: #CBD5E1 (Medium Gray)

### 2.3 Color Mode System

#### 2.3.1 Color Mode Toggle
- Prominently displayed in the application header
- Persists user preference using local storage
- Respects system preference by default (prefers-color-scheme)

#### 2.3.2 Color Mode CSS Variables
- Implemented using CSS custom properties
- Transition between modes with smooth animation (0.3s)
- Scoped to :root selector with separate dark mode variables

#### 2.3.3 Theme Implementation
- Color tokens defined by semantic purpose, not visual appearance
- Examples:
  - `--color-background`
  - `--color-surface`
  - `--color-text-primary`
  - `--color-text-secondary`
  - `--color-border`

### 2.3 Spacing System

#### 2.3.1 Base Unit
- Base unit: 4px (0.25rem)

#### 2.3.2 Spacing Scale
- 2xs: 0.25rem (4px)
- xs: 0.5rem (8px)
- sm: 0.75rem (12px)
- md: 1rem (16px)
- lg: 1.5rem (24px)
- xl: 2rem (32px)
- 2xl: 3rem (48px)
- 3xl: 4rem (64px)

### 2.4 Layout

#### 2.4.1 Grid System
- Bootstrap 12-column grid with Flexbox
- Container widths:
  - Extra small (<576px): 100%
  - Small (≥576px): 540px
  - Medium (≥768px): 720px
  - Large (≥992px): 960px
  - Extra large (≥1200px): 1140px
  - XXL (≥1400px): 1320px

#### 2.4.2 Breakpoints
- xs: 0
- sm: 576px
- md: 768px
- lg: 992px
- xl: 1200px
- xxl: 1400px

#### 2.4.3 Base Layout Templates

##### Base Template (base.html)
- **Purpose**: Public-facing pages (landing, about, contact, pricing)
- **Structure**:
  - Fixed navigation bar with logo, main links, light/dark toggle, and authentication buttons
  - Hero section for landing page
  - Content containers with varying widths based on purpose
  - Sticky footer with sitemap, social links, legal info
  - Toast container for messages (fixed position, top-right)
- **Responsiveness**:
  - Mobile: Stack navigation items into hamburger menu
  - Tablet: Show critical navigation, collapse secondary items
  - Desktop: Show full navigation

##### Dashboard Template (dashboard_base.html)
- **Purpose**: Authenticated user dashboard pages
- **Structure**:
  - Fixed top navbar with logo, search bar, notifications, light/dark toggle, user menu
  - Collapsible sidebar navigation with icons and labels
  - Main content area with page header and dynamic content
  - Contextual right sidebar for supplementary information (collapsible on mobile)
  - Toast container for messages (fixed position, top-right)
- **Responsiveness**:
  - Mobile: Hidden sidebar (reveals with gesture/button), simplified top navbar
  - Tablet: Collapsed sidebar (icons only), standard top navbar
  - Desktop: Full sidebar and top navbar

##### Authentication Template (auth_base.html)
- **Purpose**: User authentication flows (login, signup, password reset)
- **Structure**:
  - Minimal header with logo and light/dark toggle
  - Centered card container with form
  - Background with subtle brand pattern/gradient
  - Secondary actions below form card
  - Toast container for messages (fixed position, top-center)
- **Responsiveness**:
  - Mobile: Full-width card with simplified visuals
  - Tablet/Desktop: Centered card with rich visuals

### 2.5 Components

#### 2.5.1 Toast Notification System
- **Implementation**: Django messages framework with custom JS
- **Position**: Fixed top-right (top-center for auth pages)
- **Behavior**: 
  - Auto-dismiss after 5 seconds
  - Manual dismiss option (× button)
  - Animation: Slide in from right, fade out
- **Variants**:
  - Success: Green background with check icon
  - Warning: Yellow background with exclamation icon
  - Error: Red background with alert icon
  - Info: Blue background with info icon
- **Structure**:
  - Icon (FontAwesome)
  - Title (message type)
  - Message content
  - Close button
- **Stacking**: Multiple messages stack vertically with 0.5rem gap

#### 2.5.2 Buttons
- **Primary Button**
  - Background: Primary Indigo
  - Text: White
  - Hover: Primary Indigo Dark
  - Padding: 0.75rem 1.5rem (12px 24px)
  - Border radius: 0.5rem (8px)
  - Font weight: Semi-Bold
  - Icon: Optional left or right aligned

- **Secondary Button**
  - Background: White (Light mode) / Dark Surface (Dark mode)
  - Border: 1px solid Primary Indigo
  - Text: Primary Indigo
  - Hover: Light Indigo background
  - Padding: 0.75rem 1.5rem (12px 24px)
  - Border radius: 0.5rem (8px)

- **Tertiary Button**
  - Background: Transparent
  - Text: Primary Indigo
  - Hover: Light Indigo background
  - Padding: 0.75rem 1.5rem (12px 24px)
  - Border radius: 0.5rem (8px)

- **Danger Button**
  - Background: Error
  - Text: White
  - Hover: Darker Error
  - Padding: 0.75rem 1.5rem (12px 24px)
  - Border radius: 0.5rem (8px)

#### 2.5.3 Form Elements
- **Text Input**
  - Border: 1px solid Medium Gray
  - Focus: Primary Indigo border, light indigo highlight
  - Background: White (Light mode) / Dark Surface (Dark mode)
  - Padding: 0.75rem 1rem (12px 16px)
  - Border radius: 0.5rem (8px)
  - Floating labels: Transform from placeholder to top on focus/filled

- **Select Dropdown**
  - Border: 1px solid Medium Gray
  - Focus: Primary Indigo border, light indigo highlight
  - Background: White (Light mode) / Dark Surface (Dark mode)
  - Padding: 0.75rem 1rem (12px 16px)
  - Border radius: 0.5rem (8px)
  - Dropdown icon: FontAwesome chevron (fa-chevron-down)

- **Checkbox & Radio**
  - Border: 1px solid Medium Gray
  - Checked: Primary Indigo
  - Focus: Light indigo highlight
  - Size: 1.125rem × 1.125rem (18px × 18px)
  - Custom styled using CSS (not default browser controls)

- **Form Labels**
  - Color: Dark Gray (Light mode) / Medium Gray (Dark mode)
  - Font weight: Medium
  - Margin bottom: 0.375rem (6px)

#### 2.5.4 Cards
- **Standard Card**
  - Background: White (Light mode) / Dark Surface (Dark mode)
  - Border: None
  - Shadow: 0 4px 6px -1px rgba(0,0,0,0.1), 0 2px 4px -1px rgba(0,0,0,0.06)
  - Border radius: 0.75rem (12px)
  - Padding: 1.5rem (24px)

- **Interactive Card**
  - Standard card properties
  - Hover: Subtle shadow increase
  - Transition: All properties 0.2s ease
  - Hover transform: translateY(-2px)

- **Dashboard Card**
  - Standard card properties
  - Optional colored top border (4px)
  - Header with icon and action buttons
  - Content area with consistent padding
  - Footer with secondary actions

#### 2.5.5 Tables
- **Standard Table**
  - Header background: Light Gray (Light mode) / Dark Surface Elevated (Dark mode)
  - Header text: Dark Gray (Light mode) / Light Gray (Dark mode)
  - Border: 1px solid Medium Light Gray
  - Row hover: Lightest Gray (Light mode) / Subtle highlight in dark mode
  - Zebra striping: Optional
  - Responsive: Horizontal scroll on mobile, optional stacked view

- **Data Table**
  - Standard table properties
  - Sortable columns with indicators
  - Column resize handles
  - Selection checkboxes
  - Action menu for rows
  - Pagination controls with items per page selector

#### 2.5.6 Alerts
- **Standard Alert**
  - Success: Success Light background, Success border
  - Warning: Warning Light background, Warning border
  - Error: Error Light background, Error border
  - Info: Info Light background, Info border
  - Border radius: 0.5rem (8px)
  - Padding: 1rem (16px)
  - Icon: Left-aligned FontAwesome icon (fa-check-circle, fa-exclamation-triangle, etc.)

- **Dismissible Alert**
  - Standard alert properties
  - Close button (×) aligned right
  - Animation: Fade out on dismiss

#### 2.5.7 Modals
- **Standard Modal**
  - Background: White (Light mode) / Dark Surface (Dark mode)
  - Shadow: 0 20px 25px -5px rgba(0,0,0,0.1), 0 10px 10px -5px rgba(0,0,0,0.04)
  - Border radius: 0.75rem (12px)
  - Header: Border bottom, distinctive
  - Body padding: 1.5rem (24px)
  - Footer: Border top, aligned buttons
  - Backdrop: Black at 75% opacity
  - Animation: Fade in/out with scale

- **Confirmation Modal**
  - Smaller width
  - Focused content
  - Clear primary and secondary actions
  - Optional icon for context

### 2.6 Icons

#### 2.6.1 Icon System
- **Icon Set**: FontAwesome 6 (Free version)
- **Integration**: CSS import with proper subset selection
- **Styling**: 
  - Regular style for navigation and UI elements
  - Solid style for actions and emphasis
  - Duotone or Light when available for illustrations
- **Sizes**:
  - Small: 1rem (16px)
  - Medium: 1.25rem (20px) 
  - Large: 1.5rem (24px)
  - XL: 2rem (32px) for featured icons

#### 2.6.2 Icon Usage
- **Navigation**: fa-regular icons with labels on larger screens
- **Actions**: fa-solid icons as visual reinforcement
- **Status Indicators**: fa-solid icons in semantic colors
- **Industry-Specific**: Consistent icon set per industry for recognition

## 3. Page-Specific Designs

### 3.1 Admin Dashboard

#### 3.1.1 Layout
- **Header**: App logo, business selector, user menu
- **Sidebar**: Navigation menu with icons and labels
- **Content Area**: Page title, actionable cards, data tables
- **Footer**: Copyright info, version number, help links

#### 3.1.2 Dashboard Home
- Top stats cards: Total leads, Appointments scheduled, Conversion rate, Active conversations
- Recent leads table (scrollable)
- Upcoming appointments card
- Conversion metrics chart
- Activity feed

### 3.2 Lead Management

#### 3.2.1 Lead List
- Comprehensive filter and search bar
- Table columns:
  - Name
  - Date added
  - Status
  - Lead source
  - Phone
  - Industry-specific field
  - Actions
- Bulk action dropdown
- Pagination controls

#### 3.2.2 Lead Detail
- Contact info card
- Industry-specific details card
- Appointment status card
- Communication timeline
- Notes and comments section
- Action buttons: Call, SMS, Email, Edit, Delete

### 3.3 Message Templates

#### 3.3.1 Template List
- Filterable by channel (SMS/Voice) and purpose
- Template cards with:
  - Name
  - Preview
  - Last modified
  - Status (Active/Draft)

#### 3.3.2 Template Editor
- Template name and description fields
- Channel selector (SMS/Voice)
- Purpose selector (Initial contact, Follow-up, Confirmation, etc.)
- Content editor with variable insertion tool
- Preview panel showing sample with variables populated
- Test sending capability
- Version history sidebar

### 3.4 Settings

#### 3.4.1 Business Settings
- Business profile form
- Industry selection with field configuration
- Business hours and availability calendar
- Holiday and exception dates
- Notification preferences

#### 3.4.2 Webhook Configuration
- Webhook URL display (copy button)
- Secret key management
- Field mapping interface
- Test webhook tool
- Activity log

#### 3.4.3 AI Settings
- Response style configuration
- AI personality adjustments
- Approval