/**
 * Business Custom Fields JavaScript for Services AI
 * Handles custom field management functionality
 */

document.addEventListener('DOMContentLoaded', function() {
    // Elements
    const addFieldForm = document.getElementById('addFieldForm');
    const deleteFieldForm = document.getElementById('deleteFieldForm');
    const deleteFieldId = document.getElementById('deleteFieldId');
    const confirmDeleteBtn = document.getElementById('confirmDeleteBtn');
    const fieldType = document.getElementById('fieldType');
    const selectOptionsContainer = document.getElementById('selectOptionsContainer');
    
    // Show/hide select options based on field type
    if (fieldType) {
        fieldType.addEventListener('change', function() {
            if (this.value === 'select') {
                selectOptionsContainer.style.display = 'block';
            } else {
                selectOptionsContainer.style.display = 'none';
            }
        });
    }
    
    // Delete field confirmation
    const deleteFieldBtns = document.querySelectorAll('.delete-field-btn');
    if (deleteFieldBtns.length > 0) {
        deleteFieldBtns.forEach(btn => {
            btn.addEventListener('click', function() {
                const fieldId = this.getAttribute('data-field-id');
                if (fieldId && deleteFieldId) {
                    deleteFieldId.value = fieldId;
                    const deleteModal = new bootstrap.Modal(document.getElementById('deleteFieldModal'));
                    deleteModal.show();
                }
            });
        });
    }
    
    // Confirm delete
    if (confirmDeleteBtn && deleteFieldForm) {
        confirmDeleteBtn.addEventListener('click', function() {
            deleteFieldForm.submit();
        });
    }
    
    // Edit field functionality
    const editFieldBtns = document.querySelectorAll('.edit-field-btn');
    if (editFieldBtns.length > 0) {
        editFieldBtns.forEach(btn => {
            btn.addEventListener('click', function() {
                const fieldId = this.getAttribute('data-field-id');
                if (fieldId) {
                    fetchFieldDetails(fieldId);
                }
            });
        });
    }
    
    // Reset to industry defaults confirmation
    const resetFieldsBtn = document.getElementById('resetFieldsBtn');
    if (resetFieldsBtn) {
        resetFieldsBtn.addEventListener('click', function(e) {
            e.preventDefault();
            if (confirm('Are you sure you want to reset to industry defaults? This will remove all custom fields and replace them with the default fields for your industry.')) {
                window.location.href = '/business/custom-fields/reset/';
            }
        });
    }
    
    // Reorder fields mode
    const reorderFieldsBtn = document.getElementById('reorderFieldsBtn');
    if (reorderFieldsBtn) {
        reorderFieldsBtn.addEventListener('click', function(e) {
            e.preventDefault();
            toggleReorderMode();
        });
    }
    
    // Fetch field details for editing
    function fetchFieldDetails(fieldId) {
        // Show loading state
        const modal = new bootstrap.Modal(document.getElementById('addFieldModal'));
        modal.show();
        
        // Update modal title to indicate editing
        const modalTitle = document.getElementById('addFieldModalLabel');
        if (modalTitle) {
            modalTitle.textContent = 'Edit Custom Field';
        }
        
        // Update form action
        if (addFieldForm) {
            addFieldForm.action = addFieldForm.action.replace('add_custom_field', 'update_custom_field');
            
            // Set field ID
            document.getElementById('fieldId').value = fieldId;
            
            // Fetch field details via AJAX
            fetch(`/business/custom-field/${fieldId}/details/`)
                .then(response => {
                    if (!response.ok) {
                        throw new Error('Network response was not ok');
                    }
                    return response.json();
                })
                .then(data => {
                    // Populate form fields with field data
                    document.getElementById('fieldName').value = data.name;
                    document.getElementById('fieldType').value = data.field_type;
                    
                    // Handle select options
                    if (data.field_type === 'select' && data.options && data.options.choices) {
                        selectOptionsContainer.style.display = 'block';
                        document.getElementById('selectOptions').value = data.options.choices.join('\n');
                    } else {
                        selectOptionsContainer.style.display = 'none';
                    }
                    
                    document.getElementById('fieldPlaceholder').value = data.placeholder || '';
                    document.getElementById('fieldHelpText').value = data.help_text || '';
                    document.getElementById('fieldDisplayOrder').value = data.display_order;
                    document.getElementById('fieldRequired').checked = data.required;
                    document.getElementById('fieldActive').checked = data.is_active;
                })
                .catch(error => {
                    console.error('Error fetching field details:', error);
                    alert('Error loading field details. Please try again.');
                });
        }
    }
    
    // Toggle reorder mode
    function toggleReorderMode() {
        const table = document.getElementById('customFieldsTable');
        const tbody = table.querySelector('tbody');
        
        if (table.classList.contains('reorder-mode')) {
            // Exit reorder mode
            table.classList.remove('reorder-mode');
            
            // Remove drag handles
            document.querySelectorAll('.reorder-handle').forEach(handle => {
                handle.remove();
            });
            
            // Save new order
            saveFieldOrder();
            
            // Update button text
            reorderFieldsBtn.innerHTML = '<i class="fas fa-sort me-2"></i>Reorder Fields';
        } else {
            // Enter reorder mode
            table.classList.add('reorder-mode');
            
            // Add drag handles to each row
            const rows = tbody.querySelectorAll('tr[data-field-id]');
            rows.forEach(row => {
                const firstCell = row.querySelector('td:first-child');
                const handle = document.createElement('div');
                handle.className = 'reorder-handle me-2';
                handle.innerHTML = '<i class="fas fa-grip-vertical"></i>';
                firstCell.insertBefore(handle, firstCell.firstChild);
            });
            
            // Initialize drag and drop
            initDragAndDrop();
            
            // Update button text
            reorderFieldsBtn.innerHTML = '<i class="fas fa-check me-2"></i>Save Order';
        }
    }
    
    // Initialize drag and drop
    function initDragAndDrop() {
        const tbody = document.querySelector('#customFieldsTable tbody');
        if (tbody) {
            new Sortable(tbody, {
                handle: '.reorder-handle',
                animation: 150,
                ghostClass: 'sortable-ghost',
                chosenClass: 'sortable-chosen',
                onEnd: function(evt) {
                    // Update display order values
                    const rows = tbody.querySelectorAll('tr[data-field-id]');
                    rows.forEach((row, index) => {
                        const orderCell = row.querySelector('td:nth-child(4)');
                        if (orderCell) {
                            orderCell.textContent = index;
                        }
                    });
                }
            });
        }
    }
    
    // Save field order
    function saveFieldOrder() {
        const rows = document.querySelectorAll('#customFieldsTable tbody tr[data-field-id]');
        const orderData = [];
        
        rows.forEach((row, index) => {
            orderData.push({
                id: row.getAttribute('data-field-id'),
                order: index
            });
        });
        
        // Send order data to server
        fetch('/business/custom-fields/reorder/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCsrfToken()
            },
            body: JSON.stringify({ fields: orderData })
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            if (data.success) {
                // Show success message
                alert('Field order updated successfully');
            } else {
                throw new Error(data.error || 'Unknown error');
            }
        })
        .catch(error => {
            console.error('Error saving field order:', error);
            alert('Error saving field order. Please try again.');
        });
    }
    
    // Get CSRF token
    function getCsrfToken() {
        return document.querySelector('[name=csrfmiddlewaretoken]').value;
    }
});
