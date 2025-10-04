/**
 * Manage Service Item JavaScript
 * Handles both Add and Edit functionality for service items
 */

document.addEventListener('DOMContentLoaded', function() {
    // Elements
    const fieldTypeRadios = document.querySelectorAll('input[name="field_type"]');
    const booleanPricingSection = document.getElementById('booleanPricingSection');
    const selectPricingSection = document.getElementById('selectPricingSection');
    const numberPricingSection = document.getElementById('numberPricingSection');
    const selectOptionsContainer = document.getElementById('selectOptionsWithPricing');
    const addOptionBtn = document.getElementById('addOptionBtn');
    
    // Boolean pricing elements
    const yesPriceRadios = document.querySelectorAll('input[name="yes_price_type"]');
    const noPriceRadios = document.querySelectorAll('input[name="no_price_type"]');
    const yesPriceValue = document.getElementById('yesPriceValue');
    const noPriceValue = document.getElementById('noPriceValue');
    
    // Number pricing elements
    const priceTypeRadios = document.querySelectorAll('input[name="price_type"]');
    const priceValue = document.getElementById('priceValue');
    
    // Handle field type changes
    if (fieldTypeRadios.length > 0) {
        fieldTypeRadios.forEach(radio => {
            radio.addEventListener('change', function() {
                if (this.checked) {
                    handleFieldTypeChange(this.value);
                }
            });
        });
        
        // Set initial state
        const checkedFieldType = document.querySelector('input[name="field_type"]:checked');
        if (checkedFieldType) {
            handleFieldTypeChange(checkedFieldType.value);
        }
    }
    
    // Handle boolean pricing radio changes
    if (yesPriceRadios.length > 0) {
        yesPriceRadios.forEach(radio => {
            radio.addEventListener('change', function() {
                togglePriceInput(yesPriceValue, this.value);
            });
        });
    }
    
    if (noPriceRadios.length > 0) {
        noPriceRadios.forEach(radio => {
            radio.addEventListener('change', function() {
                togglePriceInput(noPriceValue, this.value);
            });
        });
    }
    
    // Handle number pricing radio changes
    if (priceTypeRadios.length > 0) {
        priceTypeRadios.forEach(radio => {
            radio.addEventListener('change', function() {
                togglePriceInput(priceValue, this.value);
            });
        });
    }
    
    // Add option button
    if (addOptionBtn) {
        addOptionBtn.addEventListener('click', function() {
            addSelectOptionRow();
        });
    }
    
    // Load existing data if editing
    const itemId = document.getElementById('itemId');
    if (itemId && itemId.value) {
        loadServiceItemData(itemId.value);
    }
    
    // Helper Functions
    
    /**
     * Handle field type change
     */
    function handleFieldTypeChange(fieldType) {
        // Hide all pricing sections
        if (booleanPricingSection) booleanPricingSection.style.display = 'none';
        if (selectPricingSection) selectPricingSection.style.display = 'none';
        if (numberPricingSection) numberPricingSection.style.display = 'none';
        
        // Show appropriate section
        if (fieldType === 'boolean') {
            if (booleanPricingSection) booleanPricingSection.style.display = 'block';
        } else if (fieldType === 'select') {
            if (selectPricingSection) selectPricingSection.style.display = 'block';
        } else if (fieldType === 'number') {
            if (numberPricingSection) numberPricingSection.style.display = 'block';
        }
    }
    
    /**
     * Toggle price input based on free/paid selection
     */
    function togglePriceInput(inputElement, priceType) {
        if (!inputElement) return;
        
        if (priceType === 'free') {
            inputElement.value = '0';
            inputElement.disabled = true;
            inputElement.closest('.col-md-6, .col-md-2')?.style.setProperty('opacity', '0.5');
        } else {
            inputElement.disabled = false;
            inputElement.closest('.col-md-6, .col-md-2')?.style.setProperty('opacity', '1');
        }
    }
    
    /**
     * Add a new select option row
     */
    function addSelectOptionRow(optionName = '', priceType = 'free', priceValue = 0) {
        if (!selectOptionsContainer) return;
        
        const optionIndex = selectOptionsContainer.children.length;
        const uniqueId = `option_${Date.now()}_${optionIndex}`;
        
        const rowHtml = `
            <div class="option-pricing-card mb-3 p-3" data-option-index="${optionIndex}">
                <div class="row align-items-center">
                    <div class="col-md-4">
                        <label class="form-label small">Option Name</label>
                        <input type="text" class="form-control" name="option_name[]" placeholder="Option name" value="${optionName}" required>
                    </div>
                    <div class="col-md-6">
                        <label class="form-label small">Price Type</label>
                        <div class="price-type-radio-group">
                            <div class="custom-radio-wrapper">
                                <input type="radio" 
                                       id="${uniqueId}_free" 
                                       name="option_price_type_${uniqueId}" 
                                       value="free" 
                                       class="custom-radio-input option-price-radio"
                                       data-row-index="${optionIndex}"
                                       ${priceType === 'free' ? 'checked' : ''}>
                                <label for="${uniqueId}_free" class="custom-radio-label">
                                    <span class="custom-radio-icon"><i class="fas fa-gift"></i></span>
                                    <span class="custom-radio-text">Free</span>
                                </label>
                            </div>
                            <div class="custom-radio-wrapper">
                                <input type="radio" 
                                       id="${uniqueId}_paid" 
                                       name="option_price_type_${uniqueId}" 
                                       value="paid" 
                                       class="custom-radio-input option-price-radio"
                                       data-row-index="${optionIndex}"
                                       ${priceType === 'paid' ? 'checked' : ''}>
                                <label for="${uniqueId}_paid" class="custom-radio-label">
                                    <span class="custom-radio-icon"><i class="fas fa-dollar-sign"></i></span>
                                    <span class="custom-radio-text">Paid</span>
                                </label>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-2">
                        <label class="form-label small">Price Value</label>
                        <div class="input-group">
                            <span class="input-group-text">$</span>
                            <input type="number" class="form-control option-price-value" name="option_price_value[]" min="0" step="0.01" value="${priceValue}" placeholder="0.00" data-row-index="${optionIndex}">
                        </div>
                    </div>
                </div>
                <button type="button" class="btn btn-sm btn-outline-danger mt-2" onclick="this.closest('.option-pricing-card').remove()">
                    <i class="fas fa-trash me-1"></i>Remove Option
                </button>
            </div>
        `;
        
        selectOptionsContainer.insertAdjacentHTML('beforeend', rowHtml);
        
        // Get the newly added row
        const newRow = selectOptionsContainer.lastElementChild;
        const radios = newRow.querySelectorAll('.option-price-radio');
        const priceInput = newRow.querySelector('.option-price-value');
        
        // Create a hidden input to store the selected price type for this row
        const hiddenInput = document.createElement('input');
        hiddenInput.type = 'hidden';
        hiddenInput.name = 'option_price_type[]';
        hiddenInput.className = 'option-price-type-hidden';
        hiddenInput.value = priceType;
        newRow.appendChild(hiddenInput);
        
        // Add event listeners to radio buttons
        radios.forEach(radio => {
            radio.addEventListener('change', function() {
                const rowIndex = this.dataset.rowIndex;
                const priceInputForRow = newRow.querySelector(`.option-price-value[data-row-index="${rowIndex}"]`);
                const hiddenInputForRow = newRow.querySelector('.option-price-type-hidden');
                
                // Update hidden input value
                if (hiddenInputForRow) {
                    hiddenInputForRow.value = this.value;
                }
                
                if (priceInputForRow) {
                    if (this.value === 'free') {
                        priceInputForRow.value = '0';
                        priceInputForRow.disabled = true;
                        priceInputForRow.closest('.col-md-2').style.opacity = '0.5';
                    } else {
                        priceInputForRow.disabled = false;
                        priceInputForRow.closest('.col-md-2').style.opacity = '1';
                    }
                }
            });
        });
        
        // Set initial state
        if (priceType === 'free' && priceInput) {
            priceInput.disabled = true;
            priceInput.closest('.col-md-2').style.opacity = '0.5';
        }
    }
    
    /**
     * Load service item data for editing
     */
    function loadServiceItemData(itemId) {
        fetch(`/business/api/service-items/${itemId}/`)
            .then(response => {
                if (!response.ok) throw new Error('Failed to load item data');
                return response.json();
            })
            .then(data => {
                // Populate basic fields
                document.getElementById('itemName').value = data.name;
                document.getElementById('itemDescription').value = data.description || '';
                
                // Set service offering
                if (data.service_offering_id) {
                    const serviceRadio = document.getElementById(`serviceOffering_${data.service_offering_id}`);
                    if (serviceRadio) serviceRadio.checked = true;
                }
                
                // Set field type
                if (data.field_type) {
                    const fieldTypeId = `fieldType${data.field_type.charAt(0).toUpperCase() + data.field_type.slice(1)}`;
                    const fieldTypeRadio = document.getElementById(fieldTypeId);
                    if (fieldTypeRadio) {
                        fieldTypeRadio.checked = true;
                        handleFieldTypeChange(data.field_type);
                    }
                }
                
                // Handle option pricing
                if (data.option_pricing) {
                    if (data.field_type === 'boolean') {
                        loadBooleanPricing(data.option_pricing);
                    } else if (data.field_type === 'select' && data.field_options) {
                        loadSelectPricing(data.field_options, data.option_pricing);
                    }
                } else if (data.field_type === 'number') {
                    // Load number pricing
                    if (data.price_type === 'free') {
                        document.getElementById('priceTypeFree').checked = true;
                    } else {
                        document.getElementById('priceTypePaid').checked = true;
                    }
                    document.getElementById('priceValue').value = data.price_value;
                }
                
                // Set additional settings
                document.getElementById('durationMinutes').value = data.duration_minutes;
                document.getElementById('maxQuantity').value = data.max_quantity;
                
                // Set is_optional
                if (data.is_optional) {
                    document.getElementById('itemOptional').checked = true;
                } else {
                    document.getElementById('itemRequired').checked = true;
                }
                
                // Set is_active
                if (data.is_active) {
                    document.getElementById('itemActive').checked = true;
                } else {
                    document.getElementById('itemInactive').checked = true;
                }
            })
            .catch(error => {
                console.error('Error loading service item:', error);
                alert('Failed to load service item data. Please try again.');
            });
    }
    
    /**
     * Load boolean pricing data
     */
    function loadBooleanPricing(optionPricing) {
        const yesConfig = optionPricing.yes || {};
        const noConfig = optionPricing.no || {};
        
        // Set Yes pricing
        if (yesConfig.price_type === 'paid') {
            document.getElementById('yesPricePaid').checked = true;
        } else {
            document.getElementById('yesPriceFree').checked = true;
        }
        yesPriceValue.value = yesConfig.price_value || 0;
        togglePriceInput(yesPriceValue, yesConfig.price_type || 'free');
        
        // Set No pricing
        if (noConfig.price_type === 'paid') {
            document.getElementById('noPricePaid').checked = true;
        } else {
            document.getElementById('noPriceFree').checked = true;
        }
        noPriceValue.value = noConfig.price_value || 0;
        togglePriceInput(noPriceValue, noConfig.price_type || 'free');
    }
    
    /**
     * Load select pricing data
     */
    function loadSelectPricing(fieldOptions, optionPricing) {
        selectOptionsContainer.innerHTML = '';
        fieldOptions.forEach(option => {
            const optionKey = option.toLowerCase();
            const optionConfig = optionPricing[optionKey] || { price_type: 'free', price_value: 0 };
            addSelectOptionRow(option, optionConfig.price_type, optionConfig.price_value);
        });
    }
});
