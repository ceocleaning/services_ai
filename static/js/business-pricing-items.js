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
    
    // Price type handling - Now using radio buttons
    const priceTypeRadios = document.querySelectorAll('input[name="price_type"]');
    const priceValue = document.getElementById('priceValue');
    const pricePrefix = document.getElementById('pricePrefix');
    const priceSuffix = document.getElementById('priceSuffix');
    const priceRow = pricePrefix ? pricePrefix.closest('.row') : null;
    const maxQuantityRow = document.getElementById('maxQuantity') ? document.getElementById('maxQuantity').closest('.row') : null;
    
    // Edit form elements - Now using radio buttons
    const editPriceTypeRadios = document.querySelectorAll('.edit-price-type-radio');
    const editPriceValue = document.getElementById('editPriceValue');
    const editPricePrefix = document.getElementById('editPricePrefix');
    const editPriceSuffix = document.getElementById('editPriceSuffix');
    const editPriceRow = editPricePrefix ? editPricePrefix.closest('.row') : null;
    const editMaxQuantityRow = document.getElementById('editMaxQuantity') ? document.getElementById('editMaxQuantity').closest('.row') : null;
    
    // Field type handling - Now using radio buttons
    const fieldTypeRadios = document.querySelectorAll('input[name="field_type"]');
    const fieldOptionsContainer = document.getElementById('fieldOptionsContainer');
    const fieldOptions = document.getElementById('fieldOptions');
    
    // Edit field type elements - Now using radio buttons
    const editFieldTypeRadios = document.querySelectorAll('.edit-field-type-radio');
    const editFieldOptionsContainer = document.getElementById('editFieldOptionsContainer');
    const editFieldOptions = document.getElementById('editFieldOptions');
    
    // Handle field type changes in add form - Radio buttons
    if (fieldTypeRadios.length > 0) {
        fieldTypeRadios.forEach(radio => {
            radio.addEventListener('change', function() {
                if (this.checked) {
                    // Update field options visibility
                    updateFieldOptionsVisibility(this.value, fieldOptionsContainer);
                    
                    // If field type is not number, set price type to free and hide price fields
                    if (this.value !== 'number') {
                        // Set free radio button as checked
                        const freeRadio = document.getElementById('priceTypeFree');
                        if (freeRadio) {
                            freeRadio.checked = true;
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
                }
            });
        });
        
        // Set initial state from checked radio
        const checkedFieldType = document.querySelector('input[name="field_type"]:checked');
        if (checkedFieldType) {
            updateFieldOptionsVisibility(checkedFieldType.value, fieldOptionsContainer);
            
            // Set initial price visibility based on field type
            if (checkedFieldType.value !== 'number') {
                const freeRadio = document.getElementById('priceTypeFree');
                if (freeRadio) {
                    freeRadio.checked = true;
                    updatePriceInput('free', pricePrefix, priceSuffix);
                    if (priceRow) priceRow.style.display = 'none';
                    if (maxQuantityRow) maxQuantityRow.style.display = 'none';
                }
            } else {
                if (priceRow) priceRow.style.display = 'flex';
                if (maxQuantityRow) maxQuantityRow.style.display = 'flex';
            }
        }
    }
    
    // Handle field type changes in edit form - Radio buttons
    if (editFieldTypeRadios.length > 0) {
        editFieldTypeRadios.forEach(radio => {
            radio.addEventListener('change', function() {
                if (this.checked) {
                    // Update field options visibility
                    updateFieldOptionsVisibility(this.value, editFieldOptionsContainer);
                    
                    // If field type is not number, set price type to free and hide price fields
                    if (this.value !== 'number') {
                        const editFreeRadio = document.getElementById('editPriceTypeFree');
                        if (editFreeRadio) {
                            editFreeRadio.checked = true;
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
                }
            });
        });
    }
    
    // Update price input based on price type - Radio buttons
    if (priceTypeRadios.length > 0) {
        priceTypeRadios.forEach(radio => {
            radio.addEventListener('change', function() {
                if (this.checked) {
                    updatePriceInput(this.value, pricePrefix, priceSuffix);
                }
            });
        });
        
        // Set initial state from checked radio
        const checkedPriceType = document.querySelector('input[name="price_type"]:checked');
        if (checkedPriceType) {
            updatePriceInput(checkedPriceType.value, pricePrefix, priceSuffix);
        }
    }
    
    // Update edit form price input based on price type - Radio buttons
    if (editPriceTypeRadios.length > 0) {
        editPriceTypeRadios.forEach(radio => {
            radio.addEventListener('change', function() {
                if (this.checked) {
                    updatePriceInput(this.value, editPricePrefix, editPriceSuffix);
                }
            });
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
        
        // Get the parent column that contains the price value field
        const priceValueColumn = priceValueInput.closest('.col-md-6');
        
        // Handle different price types
        switch(type) {
            case 'paid':
                prefixElement.textContent = '$';
                suffixElement.textContent = '';
                priceValueInput.disabled = false;
                priceValueInput.required = true;
                priceValueInput.parentElement.style.display = 'flex';
                // Show the price value column
                if (priceValueColumn) {
                    priceValueColumn.style.display = 'block';
                }
                break;
            case 'free':
                // For free items, hide the price value input and set it to 0
                priceValueInput.value = '0';
                priceValueInput.disabled = true;
                priceValueInput.required = false;
                // Hide the price value column
                if (priceValueColumn) {
                    priceValueColumn.style.display = 'none';
                }
                break;
            default:
                prefixElement.textContent = '$';
                suffixElement.textContent = '';
                priceValueInput.disabled = false;
                priceValueInput.required = true;
                priceValueInput.parentElement.style.display = 'flex';
                // Show the price value column
                if (priceValueColumn) {
                    priceValueColumn.style.display = 'block';
                }
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
                
                // Set service offering radio button
                if (data.service_offering_id) {
                    const serviceRadio = document.getElementById(`editServiceOffering_${data.service_offering_id}`);
                    if (serviceRadio) {
                        serviceRadio.checked = true;
                    }
                }
                
                // Set price type radio button
                if (data.price_type === 'free') {
                    document.getElementById('editPriceTypeFree').checked = true;
                } else {
                    document.getElementById('editPriceTypePaid').checked = true;
                }
                
                document.getElementById('editPriceValue').value = data.price_value;
                document.getElementById('editDurationMinutes').value = data.duration_minutes;
                document.getElementById('editMaxQuantity').value = data.max_quantity;
                
                // Set is_optional radio button
                if (data.is_optional) {
                    document.getElementById('editItemOptional').checked = true;
                } else {
                    document.getElementById('editItemRequired').checked = true;
                }
                
                // Set is_active radio button
                if (data.is_active) {
                    document.getElementById('editItemActive').checked = true;
                } else {
                    document.getElementById('editItemInactive').checked = true;
                }
                
                // Set field type radio button
                if (data.field_type) {
                    const fieldTypeRadio = document.getElementById(`editFieldType${data.field_type.charAt(0).toUpperCase() + data.field_type.slice(1)}`);
                    if (fieldTypeRadio) {
                        fieldTypeRadio.checked = true;
                    }
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
