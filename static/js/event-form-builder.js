// event-form-builder.js - Visual form builder for event types

document.addEventListener('DOMContentLoaded', function() {
    const fieldsContainer = document.getElementById('fieldsContainer');
    const emptyState = document.getElementById('emptyState');
    const addFieldBtn = document.getElementById('addFieldBtn');
    const saveFormBtn = document.getElementById('saveFormBtn');
    const previewBtn = document.getElementById('previewBtn');
    const fieldPropertiesPanel = document.getElementById('fieldPropertiesPanel');
    
    let fields = window.CURRENT_FIELDS || "{{ current_fields|safe }}";
    console.log(fields);
    


    let selectedFieldIndex = null;
    
    // Get CSRF token
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]')?.value || 
                     document.querySelector('meta[name="csrf-token"]')?.content;
    
    // Field type configurations
    const FIELD_TYPES = {
        'alert': { icon: 'fa-info-circle', label: 'Alert Message' },
        'text': { icon: 'fa-font', label: 'Text Input' },
        'textarea': { icon: 'fa-align-left', label: 'Text Area' },
        'number': { icon: 'fa-hashtag', label: 'Number Input' },
        'checkbox': { icon: 'fa-check-square', label: 'Checkbox' },
        'select': { icon: 'fa-list', label: 'Dropdown Select' }
    };
    
    // Initialize sortable
    if (typeof Sortable !== 'undefined') {
        new Sortable(fieldsContainer, {
            handle: '.handle',
            animation: 150,
            onEnd: function() {
                updateFieldsFromDOM();
                renderFields();
            }
        });
    }
    
    // Load existing fields
    if (fields.length > 0) {
        renderFields();
    }
    
    // Add field button
    addFieldBtn.addEventListener('click', function() {
        showFieldTypeSelector();
    });
    
    // Save form button
    saveFormBtn.addEventListener('click', async function() {
        this.disabled = true;
        this.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Saving...';
        
        try {
            const response = await fetch(`/business/event-type/${window.EVENT_TYPE_ID}/configure-form/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrfToken
                },
                body: JSON.stringify({ fields: fields })
            });
            
            const result = await response.json();
            
            if (result.success) {
                showAlert('success', result.message);
            } else {
                showAlert('danger', result.message);
            }
        } catch (error) {
            showAlert('danger', 'An error occurred while saving');
        } finally {
            this.disabled = false;
            this.innerHTML = '<i class="fas fa-save me-2"></i>Save Form Configuration';
        }
    });
    
    // Preview button
    previewBtn.addEventListener('click', function() {
        showPreview();
    });
    
    function renderFields() {
        fieldsContainer.innerHTML = '';
        
        if (fields.length === 0) {
            emptyState.style.display = 'block';
            return;
        }
        
        emptyState.style.display = 'none';
        
        fields.forEach((field, index) => {
            const fieldElement = createFieldElement(field, index);
            fieldsContainer.appendChild(fieldElement);
        });
    }
    
    function createFieldElement(field, index) {
        const template = document.getElementById('fieldItemTemplate');
        const clone = template.content.cloneNode(true);
        const fieldItem = clone.querySelector('.field-item');
        
        fieldItem.dataset.fieldIndex = index;
        
        const typeConfig = FIELD_TYPES[field.type] || { icon: 'fa-question', label: field.type };
        
        fieldItem.querySelector('.field-type-badge').innerHTML = `<i class="fas ${typeConfig.icon} me-1"></i>${typeConfig.label}`;
        fieldItem.querySelector('.field-label-display').textContent = field.label || field.message || 'Untitled Field';
        fieldItem.querySelector('.field-id-display').textContent = field.id ? `ID: ${field.id}` : '';
        
        if (field.required) {
            fieldItem.querySelector('.required-badge').style.display = 'inline-block';
        }
        
        // Edit button
        fieldItem.querySelector('.edit-field-btn').addEventListener('click', function() {
            selectField(index);
        });
        
        // Delete button
        fieldItem.querySelector('.delete-field-btn').addEventListener('click', function() {
            if (confirm('Are you sure you want to delete this field?')) {
                fields.splice(index, 1);
                renderFields();
                clearFieldProperties();
            }
        });
        
        return fieldItem;
    }
    
    function showFieldTypeSelector() {
        const html = `
            <div class="row g-3">
                ${Object.entries(FIELD_TYPES).map(([type, config]) => `
                    <div class="col-md-6">
                        <button class="btn btn-outline-primary w-100 field-type-option" data-type="${type}">
                            <i class="fas ${config.icon} fa-2x mb-2"></i>
                            <div>${config.label}</div>
                        </button>
                    </div>
                `).join('')}
            </div>
        `;
        
        const modal = new bootstrap.Modal(document.createElement('div'));
        const modalEl = document.createElement('div');
        modalEl.className = 'modal fade';
        modalEl.innerHTML = `
            <div class="modal-dialog">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title">Select Field Type</h5>
                        <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                    </div>
                    <div class="modal-body">
                        ${html}
                    </div>
                </div>
            </div>
        `;
        
        document.body.appendChild(modalEl);
        const bsModal = new bootstrap.Modal(modalEl);
        bsModal.show();
        
        modalEl.querySelectorAll('.field-type-option').forEach(btn => {
            btn.addEventListener('click', function() {
                const type = this.dataset.type;
                addField(type);
                bsModal.hide();
                setTimeout(() => modalEl.remove(), 300);
            });
        });
    }
    
    function addField(type) {
        const newField = createDefaultField(type);
        fields.push(newField);
        renderFields();
        selectField(fields.length - 1);
    }
    
    function createDefaultField(type) {
        const defaults = {
            'alert': {
                type: 'alert',
                variant: 'info',
                message: 'Enter your message here'
            },
            'text': {
                type: 'text',
                id: `field_${Date.now()}`,
                label: 'Text Field',
                required: false,
                placeholder: ''
            },
            'textarea': {
                type: 'textarea',
                id: `field_${Date.now()}`,
                label: 'Text Area',
                required: false,
                placeholder: ''
            },
            'number': {
                type: 'number',
                id: `field_${Date.now()}`,
                label: 'Number Field',
                required: false,
                placeholder: '0'
            },
            'checkbox': {
                type: 'checkbox',
                id: `field_${Date.now()}`,
                label: 'Checkbox',
                checked: false
            },
            'select': {
                type: 'select',
                id: `field_${Date.now()}`,
                label: 'Select Field',
                required: false,
                options: [
                    { value: 'option1', label: 'Option 1' },
                    { value: 'option2', label: 'Option 2' }
                ]
            }
        };
        
        return defaults[type] || {};
    }
    
    function selectField(index) {
        selectedFieldIndex = index;
        const field = fields[index];
        showFieldProperties(field, index);
        
        // Highlight selected field
        document.querySelectorAll('.field-item').forEach(item => item.classList.remove('border-primary'));
        document.querySelector(`[data-field-index="${index}"]`)?.classList.add('border-primary');
    }
    
    function showFieldProperties(field, index) {
        let html = '';
        
        if (field.type === 'alert') {
            html = `
                <div class="mb-3">
                    <label class="form-label">Variant</label>
                    <select class="form-select" id="prop_variant">
                        <option value="info" ${field.variant === 'info' ? 'selected' : ''}>Info (Blue)</option>
                        <option value="success" ${field.variant === 'success' ? 'selected' : ''}>Success (Green)</option>
                        <option value="warning" ${field.variant === 'warning' ? 'selected' : ''}>Warning (Yellow)</option>
                        <option value="danger" ${field.variant === 'danger' ? 'selected' : ''}>Danger (Red)</option>
                    </select>
                </div>
                <div class="mb-3">
                    <label class="form-label">Message</label>
                    <textarea class="form-control" id="prop_message" rows="3">${field.message || ''}</textarea>
                </div>
            `;
        } else if (field.type === 'select') {
            html = `
                <div class="mb-3">
                    <label class="form-label">Field ID</label>
                    <input type="text" class="form-control" id="prop_id" value="${field.id || ''}">
                </div>
                <div class="mb-3">
                    <label class="form-label">Label</label>
                    <input type="text" class="form-control" id="prop_label" value="${field.label || ''}">
                </div>
                <div class="mb-3">
                    <div class="form-check">
                        <input class="form-check-input" type="checkbox" id="prop_required" ${field.required ? 'checked' : ''}>
                        <label class="form-check-label" for="prop_required">Required</label>
                    </div>
                </div>
                <div class="mb-3">
                    <label class="form-label">Options</label>
                    <div id="optionsContainer">
                        ${(field.options || []).map((opt, i) => `
                            <div class="input-group mb-2">
                                <input type="text" class="form-control option-value" placeholder="Value" value="${opt.value}">
                                <input type="text" class="form-control option-label" placeholder="Label" value="${opt.label}">
                                <button class="btn btn-outline-danger remove-option-btn" type="button" data-index="${i}">
                                    <i class="fas fa-times"></i>
                                </button>
                            </div>
                        `).join('')}
                    </div>
                    <button type="button" class="btn btn-sm btn-outline-primary" id="addOptionBtn">
                        <i class="fas fa-plus me-1"></i>Add Option
                    </button>
                </div>
            `;
        } else if (field.type === 'checkbox') {
            html = `
                <div class="mb-3">
                    <label class="form-label">Field ID</label>
                    <input type="text" class="form-control" id="prop_id" value="${field.id || ''}">
                </div>
                <div class="mb-3">
                    <label class="form-label">Label</label>
                    <input type="text" class="form-control" id="prop_label" value="${field.label || ''}">
                </div>
                <div class="mb-3">
                    <div class="form-check">
                        <input class="form-check-input" type="checkbox" id="prop_checked" ${field.checked ? 'checked' : ''}>
                        <label class="form-check-label" for="prop_checked">Checked by default</label>
                    </div>
                </div>
            `;
        } else {
            html = `
                <div class="mb-3">
                    <label class="form-label">Field ID</label>
                    <input type="text" class="form-control" id="prop_id" value="${field.id || ''}">
                </div>
                <div class="mb-3">
                    <label class="form-label">Label</label>
                    <input type="text" class="form-control" id="prop_label" value="${field.label || ''}">
                </div>
                <div class="mb-3">
                    <label class="form-label">Placeholder</label>
                    <input type="text" class="form-control" id="prop_placeholder" value="${field.placeholder || ''}">
                </div>
                <div class="mb-3">
                    <div class="form-check">
                        <input class="form-check-input" type="checkbox" id="prop_required" ${field.required ? 'checked' : ''}>
                        <label class="form-check-label" for="prop_required">Required</label>
                    </div>
                </div>
            `;
        }
        
        html += `
            <button type="button" class="btn btn-primary w-100" id="updateFieldBtn">
                <i class="fas fa-check me-2"></i>Update Field
            </button>
        `;
        
        fieldPropertiesPanel.innerHTML = html;
        
        // Update field button
        document.getElementById('updateFieldBtn')?.addEventListener('click', function() {
            updateFieldFromProperties(index);
        });
        
        // Add option button (for select fields)
        document.getElementById('addOptionBtn')?.addEventListener('click', function() {
            const container = document.getElementById('optionsContainer');
            const newOption = document.createElement('div');
            newOption.className = 'input-group mb-2';
            newOption.innerHTML = `
                <input type="text" class="form-control option-value" placeholder="Value">
                <input type="text" class="form-control option-label" placeholder="Label">
                <button class="btn btn-outline-danger remove-option-btn" type="button">
                    <i class="fas fa-times"></i>
                </button>
            `;
            container.appendChild(newOption);
        });
        
        // Remove option buttons
        fieldPropertiesPanel.addEventListener('click', function(e) {
            if (e.target.closest('.remove-option-btn')) {
                e.target.closest('.input-group').remove();
            }
        });
    }
    
    function updateFieldFromProperties(index) {
        const field = fields[index];
        
        if (field.type === 'alert') {
            field.variant = document.getElementById('prop_variant')?.value;
            field.message = document.getElementById('prop_message')?.value;
        } else if (field.type === 'select') {
            field.id = document.getElementById('prop_id')?.value;
            field.label = document.getElementById('prop_label')?.value;
            field.required = document.getElementById('prop_required')?.checked;
            
            // Collect options
            const options = [];
            document.querySelectorAll('#optionsContainer .input-group').forEach(group => {
                const value = group.querySelector('.option-value').value;
                const label = group.querySelector('.option-label').value;
                if (value && label) {
                    options.push({ value, label });
                }
            });
            field.options = options;
        } else if (field.type === 'checkbox') {
            field.id = document.getElementById('prop_id')?.value;
            field.label = document.getElementById('prop_label')?.value;
            field.checked = document.getElementById('prop_checked')?.checked;
        } else {
            field.id = document.getElementById('prop_id')?.value;
            field.label = document.getElementById('prop_label')?.value;
            field.placeholder = document.getElementById('prop_placeholder')?.value;
            field.required = document.getElementById('prop_required')?.checked;
        }
        
        renderFields();
        selectField(index);
        showAlert('success', 'Field updated');
    }
    
    function updateFieldsFromDOM() {
        const newOrder = [];
        document.querySelectorAll('.field-item').forEach(item => {
            const index = parseInt(item.dataset.fieldIndex);
            newOrder.push(fields[index]);
        });
        fields = newOrder;
    }
    
    function clearFieldProperties() {
        selectedFieldIndex = null;
        fieldPropertiesPanel.innerHTML = `
            <div class="text-muted text-center py-5">
                <i class="fas fa-hand-pointer fa-3x mb-3"></i>
                <p>Select a field to edit its properties</p>
            </div>
        `;
        document.querySelectorAll('.field-item').forEach(item => item.classList.remove('border-primary'));
    }
    
    function showPreview() {
        // Build preview HTML
        let previewHtml = '';
        fields.forEach(field => {
            previewHtml += buildFieldPreview(field);
        });
        
        const modalEl = document.createElement('div');
        modalEl.className = 'modal fade';
        modalEl.innerHTML = `
            <div class="modal-dialog modal-lg">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title">Form Preview</h5>
                        <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                    </div>
                    <div class="modal-body">
                        ${previewHtml || '<p class="text-muted">No fields to preview</p>'}
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                    </div>
                </div>
            </div>
        `;
        
        document.body.appendChild(modalEl);
        const bsModal = new bootstrap.Modal(modalEl);
        bsModal.show();
        
        modalEl.addEventListener('hidden.bs.modal', () => modalEl.remove());
    }
    
    function buildFieldPreview(field) {
        switch (field.type) {
            case 'alert':
                return `<div class="alert alert-${field.variant}">${field.message}</div>`;
            case 'text':
                return `
                    <div class="mb-3">
                        <label class="form-label">${field.label}${field.required ? ' <span class="text-danger">*</span>' : ''}</label>
                        <input type="text" class="form-control" placeholder="${field.placeholder || ''}" ${field.required ? 'required' : ''}>
                    </div>
                `;
            case 'textarea':
                return `
                    <div class="mb-3">
                        <label class="form-label">${field.label}${field.required ? ' <span class="text-danger">*</span>' : ''}</label>
                        <textarea class="form-control" rows="3" placeholder="${field.placeholder || ''}" ${field.required ? 'required' : ''}></textarea>
                    </div>
                `;
            case 'number':
                return `
                    <div class="mb-3">
                        <label class="form-label">${field.label}${field.required ? ' <span class="text-danger">*</span>' : ''}</label>
                        <input type="number" class="form-control" placeholder="${field.placeholder || ''}" ${field.required ? 'required' : ''}>
                    </div>
                `;
            case 'checkbox':
                return `
                    <div class="form-check mb-3">
                        <input class="form-check-input" type="checkbox" ${field.checked ? 'checked' : ''}>
                        <label class="form-check-label">${field.label}</label>
                    </div>
                `;
            case 'select':
                return `
                    <div class="mb-3">
                        <label class="form-label">${field.label}${field.required ? ' <span class="text-danger">*</span>' : ''}</label>
                        <select class="form-select" ${field.required ? 'required' : ''}>
                            <option value="">Select...</option>
                            ${(field.options || []).map(opt => `<option value="${opt.value}">${opt.label}</option>`).join('')}
                        </select>
                    </div>
                `;
            default:
                return '';
        }
    }
    
    function showAlert(type, message) {
        const alertDiv = document.createElement('div');
        alertDiv.className = `alert alert-${type} alert-dismissible fade show position-fixed top-0 start-50 translate-middle-x mt-3`;
        alertDiv.style.zIndex = '9999';
        alertDiv.innerHTML = `
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;
        document.body.appendChild(alertDiv);
        
        setTimeout(() => alertDiv.remove(), 3000);
    }
});
