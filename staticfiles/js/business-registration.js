document.addEventListener('DOMContentLoaded', function() {
    // DOM Elements
    const form = document.getElementById('businessRegistrationForm');
    const steps = document.querySelectorAll('.form-step');
    const stepIndicators = document.querySelectorAll('.step');
    const progressBar = document.querySelector('.progress-bar');
    const nextButtons = document.querySelectorAll('.next-step');
    const prevButtons = document.querySelectorAll('.prev-step');
    const submitButton = document.getElementById('submit_button');
    const currentStepInput = document.getElementById('current_step');
    const industrySelect = document.getElementById('industry');
    const agreeTermsButton = document.getElementById('agreeTerms');
    const termsCheckbox = document.getElementById('terms_agree');
    
    // Form Data Storage
    let formData = {};
    
    // Current Step Tracking
    let currentStep = 1;
    const totalSteps = steps.length;
    
    // Initialize
    loadIndustries();
    setupEventListeners();
    
    // Function to set up event listeners
    function setupEventListeners() {
        // Next button clicks
        nextButtons.forEach(button => {
            button.addEventListener('click', () => {
                if (validateStep(currentStep)) {
                    saveStepData(currentStep);
                    goToStep(currentStep + 1);
                }
            });
        });
        
        // Previous button clicks
        prevButtons.forEach(button => {
            button.addEventListener('click', () => {
                goToStep(currentStep - 1);
            });
        });
        
        // Industry selection change - no special handling needed now
        
        // Terms agreement
        if (agreeTermsButton) {
            agreeTermsButton.addEventListener('click', () => {
                termsCheckbox.checked = true;
                termsCheckbox.dispatchEvent(new Event('change'));
            });
        }
        
        // Form submission
        if (form) {
            form.addEventListener('submit', handleFormSubmit);
        }
    }
    
    // Function to validate the current step
    function validateStep(step) {
        const currentStepElement = document.getElementById(`step${step}`);
        const inputs = currentStepElement.querySelectorAll('input[required], select[required], textarea[required]');
        
        let isValid = true;
        
        inputs.forEach(input => {
            if (!input.value.trim()) {
                input.classList.add('is-invalid');
                isValid = false;
            } else {
                input.classList.remove('is-invalid');
            }
        });
        
        // Special validation for step 4 (terms agreement)
        if (step === 4 && !termsCheckbox.checked) {
            termsCheckbox.classList.add('is-invalid');
            isValid = false;
        }
        
        return isValid;
    }
    
    // Function to save data from the current step
    function saveStepData(step) {
        const currentStepElement = document.getElementById(`step${step}`);
        const inputs = currentStepElement.querySelectorAll('input, select, textarea');
        
        inputs.forEach(input => {
            if (input.name && input.name !== 'csrfmiddlewaretoken') {
                formData[input.name] = input.value;
            }
        });
        
        // Save to session storage as backup
        sessionStorage.setItem('business_registration_data', JSON.stringify(formData));
    }
    
    // Function to navigate to a specific step
    function goToStep(step) {
        // Hide all steps
        steps.forEach(stepElement => {
            stepElement.style.display = 'none';
        });
        
        // Show the current step
        document.getElementById(`step${step}`).style.display = 'block';
        document.getElementById(`step${step}`).classList.add('fade-in');
        
        // Update step indicators
        stepIndicators.forEach((indicator, index) => {
            const stepNum = index + 1;
            
            if (stepNum < step) {
                indicator.classList.add('completed');
                indicator.classList.remove('active');
            } else if (stepNum === step) {
                indicator.classList.add('active');
                indicator.classList.remove('completed');
            } else {
                indicator.classList.remove('active', 'completed');
            }
        });
        
        // Update progress bar
        const progress = ((step - 1) / (totalSteps - 1)) * 100;
        progressBar.style.width = `${progress}%`;
        progressBar.setAttribute('aria-valuenow', progress);
        
        // Update current step input
        currentStepInput.value = step;
        currentStep = step;
        
        // If on the final review step, populate the review data
        if (step === 4) {
            populateReviewData();
        }
    }
    
    // Function to load industries from the API
    function loadIndustries() {
        fetch('/business/api/industries/')
            .then(response => response.json())
            .then(data => {
                if (data.industries && data.industries.length > 0) {
                    data.industries.forEach(industry => {
                        const option = document.createElement('option');
                        option.value = industry.id;
                        option.textContent = industry.name;
                        industrySelect.appendChild(option);
                    });
                }
            })
            .catch(error => {
                console.error('Error loading industries:', error);
            });
    }
    
    // Industry fields loading removed as requested - fields will be shown in bookings form instead
    
    // Function to populate the review data on the final step
    function populateReviewData() {
        const reviewDataContainer = document.querySelector('.review-data');
        reviewDataContainer.innerHTML = '';
        
        // Business Information
        const businessInfoSection = document.createElement('div');
        businessInfoSection.className = 'review-section';
        
        const businessInfoTitle = document.createElement('h5');
        businessInfoTitle.innerHTML = '<i class="fas fa-building"></i> Business Information';
        businessInfoSection.appendChild(businessInfoTitle);
        
        const businessInfoFields = [
            { label: 'Business Name', key: 'business_name' },
            { label: 'Description', key: 'business_description' },
            { label: 'Website', key: 'website' }
        ];
        
        businessInfoFields.forEach(field => {
            if (formData[field.key]) {
                const item = createReviewItem(field.label, formData[field.key]);
                businessInfoSection.appendChild(item);
            }
        });
        
        reviewDataContainer.appendChild(businessInfoSection);
        
        // Industry Information
        const industrySection = document.createElement('div');
        industrySection.className = 'review-section';
        
        const industryTitle = document.createElement('h5');
        industryTitle.innerHTML = '<i class="fas fa-industry"></i> Industry Information';
        industrySection.appendChild(industryTitle);
        
        // Get industry name from select
        const industryName = industrySelect.options[industrySelect.selectedIndex].text;
        const industryItem = createReviewItem('Industry', industryName);
        industrySection.appendChild(industryItem);
        
        // Industry-specific fields removed as requested
        
        reviewDataContainer.appendChild(industrySection);
        
        // Contact Information
        const contactSection = document.createElement('div');
        contactSection.className = 'review-section';
        
        const contactTitle = document.createElement('h5');
        contactTitle.innerHTML = '<i class="fas fa-address-card"></i> Contact Information';
        contactSection.appendChild(contactTitle);
        
        const contactFields = [
            { label: 'Phone Number', key: 'phone_number' },
            { label: 'Email', key: 'email' },
            { label: 'Address', key: 'address' },
            { label: 'City', key: 'city' },
            { label: 'State', key: 'state' },
            { label: 'ZIP Code', key: 'zip_code' }
        ];
        
        contactFields.forEach(field => {
            if (formData[field.key]) {
                const item = createReviewItem(field.label, formData[field.key]);
                contactSection.appendChild(item);
            }
        });
        
        reviewDataContainer.appendChild(contactSection);
        
        // Setup edit buttons
        setupEditButtons();
    }
    
    // Helper function to create a review item
    function createReviewItem(label, value) {
        const item = document.createElement('div');
        item.className = 'review-item';
        
        const labelElement = document.createElement('div');
        labelElement.className = 'review-label';
        labelElement.textContent = label;
        
        const valueElement = document.createElement('div');
        valueElement.className = 'review-value';
        valueElement.textContent = value;
        
        item.appendChild(labelElement);
        item.appendChild(valueElement);
        
        return item;
    }
    
    // Function to handle form submission
    function handleFormSubmit(event) {
        event.preventDefault();
        
        if (!validateStep(currentStep)) {
            return;
        }
        
        // Save data from the final step
        saveStepData(currentStep);
        
        // Disable submit button and show loading state
        submitButton.disabled = true;
        submitButton.innerHTML = '<span class="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>Processing...';
        
        // Send data to the server
        fetch('/business/api/register/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
            },
            body: JSON.stringify(formData)
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            if (data.success) {
                // Clear form data from session storage
                sessionStorage.removeItem('business_registration_data');
                
                // Redirect to the dashboard or success page
                window.location.href = data.redirect_url || '/business/dashboard/';
            } else {
                // Show error message
                throw new Error(data.message || 'An error occurred during registration.');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            
            // Re-enable submit button
            submitButton.disabled = false;
            submitButton.innerHTML = 'Complete Registration';
            
            // Show error message
            const errorAlert = document.createElement('div');
            errorAlert.className = 'alert alert-danger mt-3';
            errorAlert.textContent = error.message || 'An error occurred during registration. Please try again.';
            
            const formContainer = document.querySelector('.business-registration');
            formContainer.insertBefore(errorAlert, form);
            
            // Remove error message after 5 seconds
            setTimeout(() => {
                errorAlert.remove();
            }, 5000);
        });
    }
    
    // Function to setup edit buttons in review section
    function setupEditButtons() {
        const editButtons = document.querySelectorAll('.edit-info');
        
        editButtons.forEach(button => {
            button.addEventListener('click', () => {
                const stepToGo = parseInt(button.getAttribute('data-step'));
                if (stepToGo >= 1 && stepToGo <= 3) {
                    goToStep(stepToGo);
                }
            });
        });
    }
    
    // Try to restore form data from session storage
    const savedData = sessionStorage.getItem('business_registration_data');
    if (savedData) {
        try {
            formData = JSON.parse(savedData);
            
            // Populate form fields with saved data
            Object.keys(formData).forEach(key => {
                const input = document.querySelector(`[name="${key}"]`);
                if (input) {
                    input.value = formData[key];
                }
            });
            
            // If industry is selected, load industry fields
            if (formData.industry) {
                loadIndustryFields(formData.industry);
            }
        } catch (error) {
            console.error('Error restoring form data:', error);
        }
    }
});
