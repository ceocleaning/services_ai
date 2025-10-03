/**
 * Business Pricing Items JavaScript for Services AI
 * Handles service item management functionality
 */

document.addEventListener('DOMContentLoaded', function() {
    // Elements
    const addServiceItemForm = document.getElementById('addServiceItemForm');
    const editServiceItemForm = document.getElementById('editServiceItemForm');
    const deleteServiceItemForm = document.getElementById('deleteServiceItemForm');
    const deleteItemId = document.getElementById('deleteItemId');
    const confirmDeleteItemBtn = document.getElementById('confirmDeleteItemBtn');
    
    // Price type handling
    const priceType = document.getElementById('priceType');
    const priceValue = document.getElementById('priceValue');
    const pricePrefix = document.getElementById('pricePrefix');
    const priceSuffix = document.getElementById('priceSuffix');
    const priceRow = priceType ? priceType.closest('.row') : null;
    const maxQuantityRow = document.getElementById('maxQuantity') ? document.getElementById('maxQuantity').closest('.row') : null;
    
    // Edit form elements
    const editPriceType = document.getElementById('editPriceType');
    const editPriceValue = document.getElementById('editPriceValue');
    const editPricePrefix = document.getElementById('editPricePrefix');
    const editPriceSuffix = document.getElementById('editPriceSuffix');
    const editPriceRow = editPriceType ? editPriceType.closest('.row') : null;
    const editMaxQuantityRow = document.getElementById('editMaxQuantity') ? document.getElementById('editMaxQuantity').closest('.row') : null;
    
    // Field type handling
    const fieldType = document.getElementById('fieldType');
    const fieldOptionsContainer = document.getElementById('fieldOptionsContainer');
    const fieldOptions = document.getElementById('fieldOptions');
    
    // Edit field type elements
    const editFieldType = document.getElementById('editFieldType');
    const editFieldOptionsContainer = document.getElementById('editFieldOptionsContainer');
    const editFieldOptions = document.getElementById('editFieldOptions');
    
    // Handle field type changes in add form
    if (fieldType) {
        fieldType.addEventListener('change', function() {
            // Update field options visibility
            updateFieldOptionsVisibility(this.value, fieldOptionsContainer);
            
            // If field type is not number, set price type to free and hide price fields
            if (this.value !== 'number') {
                if (priceType) {
                    priceType.value = 'free';
                    updatePriceInput('free', pricePrefix, priceSuffix);
                    
                    // Hide price row and max quantity row
                    if (priceRow) priceRow.style.display = 'none';
                    if (maxQuantityRow) maxQuantityRow.style.display = 'none';
                }
            } else {
                // Show price row and max quantity row
                if (priceRow) priceRow.style.display = 'flex';
                if (maxQuantityRow) maxQuantityRow.style.display = 'flex';
            }
        });
        
        // Set initial state
        updateFieldOptionsVisibility(fieldType.value, fieldOptionsContainer);
        
        // Set initial price visibility based on field type
        if (fieldType.value !== 'number') {
            if (priceType) {
                priceType.value = 'free';
                updatePriceInput('free', pricePrefix, priceSuffix);
                if (priceRow) priceRow.style.display = 'none';
                if (maxQuantityRow) maxQuantityRow.style.display = 'none';
            }
        } else {
            if (priceRow) priceRow.style.display = 'flex';
            if (maxQuantityRow) maxQuantityRow.style.display = 'flex';
        }
    }
    
    // Handle field type changes in edit form
    if (editFieldType) {
        editFieldType.addEventListener('change', function() {
            // Update field options visibility
            updateFieldOptionsVisibility(this.value, editFieldOptionsContainer);
            
            // If field type is not number, set price type to free and hide price fields
            if (this.value !== 'number') {
                if (editPriceType) {
                    editPriceType.value = 'free';
                    updatePriceInput('free', editPricePrefix, editPriceSuffix);
                    
                    // Hide price row and max quantity row
                    if (editPriceRow) editPriceRow.style.display = 'none';
                    if (editMaxQuantityRow) editMaxQuantityRow.style.display = 'none';
                }
            } else {
                // Show price row and max quantity row
                if (editPriceRow) editPriceRow.style.display = 'flex';
                if (editMaxQuantityRow) editMaxQuantityRow.style.display = 'flex';
            }
        });
    }
    
    // Update price input based on price type
    if (priceType) {
        priceType.addEventListener('change', function() {
            updatePriceInput(this.value, pricePrefix, priceSuffix);
        });
        
        // Set initial state
        updatePriceInput(priceType.value, pricePrefix, priceSuffix);
    }
    
    // Update edit form price input based on price type
    if (editPriceType) {
        editPriceType.addEventListener('change', function() {
            updatePriceInput(this.value, editPricePrefix, editPriceSuffix);
        });
    }
    
    // Delete service item confirmation
    const deleteItemBtns = document.querySelectorAll('.delete-item-btn');
    if (deleteItemBtns.length > 0) {
        deleteItemBtns.forEach(btn => {
            btn.addEventListener('click', function() {
                const itemId = this.getAttribute('data-item-id');
                if (itemId && deleteItemId) {
                    deleteItemId.value = itemId;
                    const deleteModal = new bootstrap.Modal(document.getElementById('deleteServiceItemModal'));
                    deleteModal.show();
                }
            });
        });
    }
    
    // Confirm delete
    if (confirmDeleteItemBtn && deleteServiceItemForm) {
        confirmDeleteItemBtn.addEventListener('click', function() {
            deleteServiceItemForm.submit();
        });
    }
    
    // Edit service item functionality
    const editItemBtns = document.querySelectorAll('.edit-item-btn');
    if (editItemBtns.length > 0) {
        editItemBtns.forEach(btn => {
            btn.addEventListener('click', function() {
                const itemId = this.getAttribute('data-item-id');
                if (itemId) {
                    fetchServiceItemDetails(itemId);
                }
            });
        });
    }
    
    // Helper Functions
    
    /**
     * Update price input based on price type
     */
    function updatePriceInput(type, prefixElement, suffixElement) {
        if (!prefixElement || !suffixElement) return;
        
        // Get the price value input element
        const priceValueInput = prefixElement.parentElement.querySelector('input');
        if (!priceValueInput) return;
        
        // Handle different price types
        switch(type) {
            case 'fixed':
                prefixElement.textContent = '$';
                suffixElement.textContent = '';
                priceValueInput.disabled = false;
                priceValueInput.required = true;
                priceValueInput.parentElement.style.display = 'flex';
                break;
            case 'percentage':
                prefixElement.textContent = '';
                suffixElement.textContent = '%';
                priceValueInput.disabled = false;
                priceValueInput.required = true;
                priceValueInput.parentElement.style.display = 'flex';
                break;
            case 'hourly':
                prefixElement.textContent = '$';
                suffixElement.textContent = '/hr';
                priceValueInput.disabled = false;
                priceValueInput.required = true;
                priceValueInput.parentElement.style.display = 'flex';
                break;
            case 'per_unit':
                prefixElement.textContent = '$';
                suffixElement.textContent = '/unit';
                priceValueInput.disabled = false;
                priceValueInput.required = true;
                priceValueInput.parentElement.style.display = 'flex';
                break;
            case 'free':
                // For free items, hide the price value input and set it to 0
                priceValueInput.value = '0';
                priceValueInput.disabled = true;
                priceValueInput.required = false;
                break;
            default:
                prefixElement.textContent = '$';
                suffixElement.textContent = '';
                priceValueInput.disabled = false;
                priceValueInput.required = true;
                priceValueInput.parentElement.style.display = 'flex';
        }
    }
    
    /**
     * Update field options visibility based on field type
     */
    function updateFieldOptionsVisibility(fieldType, optionsContainer) {
        if (!optionsContainer) return;
        
        // Only show options for select field type
        if (fieldType === 'select') {
            optionsContainer.style.display = 'block';
            const optionsInput = optionsContainer.querySelector('input');
            if (optionsInput) {
                optionsInput.required = true;
            }
        } else {
            optionsContainer.style.display = 'none';
            const optionsInput = optionsContainer.querySelector('input');
            if (optionsInput) {
                optionsInput.required = false;
            }
        }
    }
    
    /**
     * Fetch service item details for editing
     */
    function fetchServiceItemDetails(itemId) {
        fetch(`/business/api/service-items/${itemId}/`)
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(data => {
                // Populate the edit form
                document.getElementById('editItemId').value = data.id;
                document.getElementById('editItemName').value = data.name;
                document.getElementById('editItemDescription').value = data.description || '';
                document.getElementById('editPriceType').value = data.price_type;
                document.getElementById('editPriceValue').value = data.price_value;
                document.getElementById('editDurationMinutes').value = data.duration_minutes;
                document.getElementById('editMaxQuantity').value = data.max_quantity;
                document.getElementById('editItemOptional').checked = data.is_optional;
                document.getElementById('editItemActive').checked = data.is_active;
                
                // Set field type and options
                if (data.field_type) {
                    document.getElementById('editFieldType').value = data.field_type;
                }
                
                // Handle field options for select type
                if (data.field_options && Array.isArray(data.field_options)) {
                    document.getElementById('editFieldOptions').value = data.field_options.join(', ');
                } else if (data.field_options && typeof data.field_options === 'string') {
                    document.getElementById('editFieldOptions').value = data.field_options;
                }
                
                // Update field options visibility
                updateFieldOptionsVisibility(data.field_type || 'text', editFieldOptionsContainer);
                
                // Set price visibility based on field type
                if (data.field_type !== 'number') {
                    if (editPriceRow) editPriceRow.style.display = 'none';
                    if (editMaxQuantityRow) editMaxQuantityRow.style.display = 'none';
                } else {
                    if (editPriceRow) editPriceRow.style.display = 'flex';
                    if (editMaxQuantityRow) editMaxQuantityRow.style.display = 'flex';
                }
                
                // Update price input display
                updatePriceInput(data.price_type, editPricePrefix, editPriceSuffix);
                
                // Show the modal
                const editModal = new bootstrap.Modal(document.getElementById('editServiceItemModal'));
                editModal.show();
            })
            .catch(error => {
                console.error('Error fetching service item details:', error);
                alert('Failed to load service item details. Please try again.');
            });
    }
});
