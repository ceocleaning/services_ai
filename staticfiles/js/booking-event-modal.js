// booking-event-modal.js - Dynamic event modal handler
// All configurations now come from backend via window.DYNAMIC_EVENT_CONFIGS

// Fallback configurations (only used if backend data is missing)
const FALLBACK_CONFIGS = {
    'confirmed': {
        title: 'Confirm Booking',
        icon: 'fa-check',
        color: 'success',
        requiresReason: false,
        fields: [
            {
                type: 'alert',
                variant: 'info',
                message: 'This will confirm the booking and notify the customer.'
            }
        ],
        submitText: 'Confirm Booking',
        successMessage: 'Booking confirmed successfully'
    },
    
    'cancelled': {
        title: 'Cancel Booking',
        icon: 'fa-times',
        color: 'danger',
        requiresReason: true,
        fields: [
            {
                type: 'alert',
                variant: 'warning',
                message: 'Bookings can only be cancelled at least 24 hours before appointment.'
            },
            {
                type: 'textarea',
                id: 'reason',
                label: 'Cancellation Reason',
                required: true,
                placeholder: 'Please provide a reason for cancelling...'
            },
            {
                type: 'checkbox',
                id: 'notify_customer',
                label: 'Send cancellation notification to customer',
                checked: true
            }
        ],
        submitText: 'Cancel Booking',
        successMessage: 'Booking cancelled successfully'
    },
    
    'completed': {
        title: 'Mark as Completed',
        icon: 'fa-check-double',
        color: 'success',
        requiresReason: false,
        fields: [
            {
                type: 'alert',
                variant: 'success',
                message: 'Mark this booking as completed.'
            },
            {
                type: 'textarea',
                id: 'notes',
                label: 'Completion Notes (Optional)',
                required: false,
                placeholder: 'Add any notes about the completed appointment...'
            },
            {
                type: 'checkbox',
                id: 'send_thank_you',
                label: 'Send thank you message to customer',
                checked: true
            },
            {
                type: 'checkbox',
                id: 'request_review',
                label: 'Request review from customer',
                checked: false
            }
        ],
        submitText: 'Mark Completed',
        successMessage: 'Booking marked as completed'
    },
    
    'no_show': {
        title: 'Mark as No-Show',
        icon: 'fa-user-times',
        color: 'dark',
        requiresReason: true,
        fields: [
            {
                type: 'alert',
                variant: 'warning',
                message: 'Mark this booking as a no-show (customer did not arrive).'
            },
            {
                type: 'textarea',
                id: 'reason',
                label: 'Notes',
                required: true,
                placeholder: 'Add notes about the no-show...'
            },
            {
                type: 'checkbox',
                id: 'charge_cancellation_fee',
                label: 'Charge cancellation fee',
                checked: false
            }
        ],
        submitText: 'Mark No-Show',
        successMessage: 'Booking marked as no-show'
    },
    
    'note_added': {
        title: 'Add Note',
        icon: 'fa-sticky-note',
        color: 'info',
        requiresReason: false,
        fields: [
            {
                type: 'textarea',
                id: 'note',
                label: 'Note',
                required: true,
                placeholder: 'Add a note to this booking...'
            }
        ],
        submitText: 'Add Note',
        successMessage: 'Note added successfully'
    },
    
    'payment_received': {
        title: 'Record Payment',
        icon: 'fa-dollar-sign',
        color: 'success',
        requiresReason: false,
        fields: [
            {
                type: 'number',
                id: 'amount',
                label: 'Payment Amount',
                required: true,
                placeholder: '0.00'
            },
            {
                type: 'select',
                id: 'payment_method',
                label: 'Payment Method',
                required: true,
                options: [
                    { value: 'cash', label: 'Cash' },
                    { value: 'card', label: 'Credit/Debit Card' },
                    { value: 'bank_transfer', label: 'Bank Transfer' },
                    { value: 'other', label: 'Other' }
                ]
            },
            {
                type: 'textarea',
                id: 'notes',
                label: 'Payment Notes (Optional)',
                required: false
            }
        ],
        submitText: 'Record Payment',
        successMessage: 'Payment recorded successfully'
    }
};

function buildField(field) {
    switch (field.type) {
        case 'alert':
            return `
                <div class="alert alert-${field.variant}" role="alert">
                    ${field.message}
                </div>
            `;
        
        case 'text':
            return `
                <div class="mb-3">
                    <label for="${field.id}" class="form-label">
                        ${field.label}
                        ${field.required ? '<span class="text-danger">*</span>' : ''}
                    </label>
                    <input type="text" class="form-control" id="${field.id}" 
                           placeholder="${field.placeholder || ''}"
                           ${field.required ? 'required' : ''}>
                </div>
            `;
        
        case 'textarea':
            return `
                <div class="mb-3">
                    <label for="${field.id}" class="form-label">
                        ${field.label}
                        ${field.required ? '<span class="text-danger">*</span>' : ''}
                    </label>
                    <textarea class="form-control" id="${field.id}" rows="4" 
                              placeholder="${field.placeholder || ''}"
                              ${field.required ? 'required' : ''}></textarea>
                </div>
            `;
        
        case 'checkbox':
        case 'boolean':
            return `
                <div class="form-check mb-3">
                    <input class="form-check-input" type="checkbox" id="${field.id}" 
                           ${field.checked ? 'checked' : ''}>
                    <label class="form-check-label" for="${field.id}">
                        ${field.label}
                        ${field.required ? '<span class="text-danger">*</span>' : ''}
                    </label>
                </div>
            `;
        
        case 'number':
            return `
                <div class="mb-3">
                    <label for="${field.id}" class="form-label">
                        ${field.label}
                        ${field.required ? '<span class="text-danger">*</span>' : ''}
                    </label>
                    <input type="number" class="form-control" id="${field.id}" 
                           placeholder="${field.placeholder || ''}" 
                           step="${field.step || '0.01'}"
                           ${field.min !== undefined ? `min="${field.min}"` : ''}
                           ${field.max !== undefined ? `max="${field.max}"` : ''}
                           ${field.required ? 'required' : ''}>
                </div>
            `;
        
        case 'select':
            const options = (field.options || []).map(opt => 
                `<option value="${opt.value}">${opt.label}</option>`
            ).join('');
            return `
                <div class="mb-3">
                    <label for="${field.id}" class="form-label">
                        ${field.label}
                        ${field.required ? '<span class="text-danger">*</span>' : ''}
                    </label>
                    <select class="form-select" id="${field.id}" ${field.required ? 'required' : ''}>
                        <option value="">Select...</option>
                        ${options}
                    </select>
                </div>
            `;
        
        default:
            return '';
    }
}

function showEventModal(eventKey, eventTypeId) {
    // Get configuration from backend (passed via template)
    const backendConfig = window.DYNAMIC_EVENT_CONFIGS?.[eventKey];

    console.log(backendConfig);
    
    if (!backendConfig) {
        console.error('Event configuration not found for:', eventKey);
        console.log('Available configs:', window.DYNAMIC_EVENT_CONFIGS);
        return;
    }
    
    // Use backend configuration directly (it includes everything)
    const config = {
        title: backendConfig.title,
        icon: backendConfig.icon,
        color: backendConfig.color,
        fields: backendConfig.fields || [],
        submitText: backendConfig.submitText,
        successMessage: backendConfig.successMessage
    };

    console.log(config);
    
    
    // Set modal title and icon (using dynamic values)
    document.getElementById('eventModalTitle').textContent = config.title;
    document.getElementById('eventModalIcon').className = `fas ${config.icon} me-2 text-${config.color}`;
    
    // Set submit button
    const submitBtn = document.getElementById('eventModalSubmit');
    submitBtn.className = `btn btn-${config.color}`;
    submitBtn.dataset.eventKey = eventKey;
    submitBtn.dataset.eventTypeId = backendConfig.id || eventTypeId;
    submitBtn.dataset.config = JSON.stringify(config);
    document.getElementById('eventModalSubmitText').textContent = config.submitText;
    
    // Build dynamic content
    const content = document.getElementById('eventModalContent');
    content.innerHTML = '';
    
    config.fields.forEach(field => {
        const fieldHtml = buildField(field);
        content.insertAdjacentHTML('beforeend', fieldHtml);
    });
    
    // Show modal
    const modal = new bootstrap.Modal(document.getElementById('eventModal'));
    modal.show();
}

// Export for use in booking-detail.js
window.showEventModal = showEventModal;
