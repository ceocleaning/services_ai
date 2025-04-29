/**
 * Business Profile JavaScript for Services AI
 * Handles profile editing functionality
 */

document.addEventListener('DOMContentLoaded', function() {
    // Elements
    const editProfileBtn = document.getElementById('editProfileBtn');
    const cancelEditBtn = document.getElementById('cancelEditBtn');
    const businessProfileForm = document.getElementById('businessProfileForm');
    const formInputs = businessProfileForm.querySelectorAll('input, textarea');
    const formActions = businessProfileForm.querySelector('.form-actions');
    const logoUploadOverlay = document.getElementById('logoUploadOverlay');
    const logoUpload = document.getElementById('logoUpload');
    const logoPreview = document.getElementById('logoPreview');
    
    // Original values storage
    const originalValues = {};
    
    // Store original values
    formInputs.forEach(input => {
        originalValues[input.name] = input.value;
    });
    
    // Enable edit mode
    if (editProfileBtn) {
        editProfileBtn.addEventListener('click', function() {
            enableEditMode();
        });
    }
    
    // Cancel edit mode
    if (cancelEditBtn) {
        cancelEditBtn.addEventListener('click', function() {
            disableEditMode();
            resetFormValues();
        });
    }
    
    // Logo upload preview
    if (logoUpload) {
        logoUpload.addEventListener('change', function(e) {
            if (this.files && this.files[0]) {
                const reader = new FileReader();
                
                reader.onload = function(e) {
                    // Check if logoPreview is an image or a div
                    if (logoPreview.tagName === 'IMG') {
                        logoPreview.src = e.target.result;
                    } else {
                        // Create an image element to replace the placeholder
                        const img = document.createElement('img');
                        img.src = e.target.result;
                        img.classList.add('business-logo');
                        img.id = 'logoPreview';
                        
                        // Replace the placeholder with the image
                        logoPreview.parentNode.replaceChild(img, logoPreview);
                        
                        // Update the logoPreview reference
                        logoPreview = img;
                    }
                };
                
                reader.readAsDataURL(this.files[0]);
            }
        });
    }
    
    // Form submission
    if (businessProfileForm) {
        businessProfileForm.addEventListener('submit', function(e) {
            // You can add validation here if needed
            
            // Show loading state
            const submitBtn = this.querySelector('button[type="submit"]');
            const originalText = submitBtn.innerHTML;
            submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Saving...';
            submitBtn.disabled = true;
            
            // Form will submit normally, but you could use fetch API for AJAX submission
            // If using AJAX, remember to prevent default form submission
            // e.preventDefault();
            
            // Example of AJAX submission:
            /*
            e.preventDefault();
            
            const formData = new FormData(this);
            
            fetch(this.action, {
                method: 'POST',
                body: formData,
                headers: {
                    'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    // Show success message
                    showNotification('success', 'Profile updated successfully!');
                    disableEditMode();
                    
                    // Update original values
                    formInputs.forEach(input => {
                        originalValues[input.name] = input.value;
                    });
                } else {
                    // Show error message
                    showNotification('error', data.message || 'An error occurred');
                }
            })
            .catch(error => {
                console.error('Error:', error);
                showNotification('error', 'An error occurred while saving');
            })
            .finally(() => {
                // Reset button
                submitBtn.innerHTML = originalText;
                submitBtn.disabled = false;
            });
            */
        });
    }
    
    // Helper functions
    function enableEditMode() {
        // Enable all form inputs except industry
        formInputs.forEach(input => {
            if (input.id !== 'industry') {
                input.disabled = false;
            }
        });
        
        // Show form actions
        formActions.classList.remove('d-none');
        
        // Hide edit button
        editProfileBtn.classList.add('d-none');
        
        // Show logo upload overlay
        if (logoUploadOverlay) {
            logoUploadOverlay.classList.remove('d-none');
        }
        
        // Add edit mode class to form
        businessProfileForm.classList.add('edit-mode');
    }
    
    function disableEditMode() {
        // Disable all form inputs
        formInputs.forEach(input => {
            input.disabled = true;
        });
        
        // Hide form actions
        formActions.classList.add('d-none');
        
        // Show edit button
        editProfileBtn.classList.remove('d-none');
        
        // Hide logo upload overlay
        if (logoUploadOverlay) {
            logoUploadOverlay.classList.add('d-none');
        }
        
        // Remove edit mode class from form
        businessProfileForm.classList.remove('edit-mode');
    }
    
    function resetFormValues() {
        // Reset all form inputs to original values
        formInputs.forEach(input => {
            if (originalValues[input.name] !== undefined) {
                input.value = originalValues[input.name];
            }
        });
        
        // Reset logo preview (would need to store original src)
        // This is simplified - in a real app you'd need to handle this better
        if (logoPreview && logoPreview.tagName === 'IMG' && logoPreview.dataset.originalSrc) {
            logoPreview.src = logoPreview.dataset.originalSrc;
        }
    }
    
    function showNotification(type, message) {
        // Create toast notification
        const toast = document.createElement('div');
        toast.className = `toast align-items-center text-white bg-${type === 'success' ? 'success' : 'danger'} border-0`;
        toast.setAttribute('role', 'alert');
        toast.setAttribute('aria-live', 'assertive');
        toast.setAttribute('aria-atomic', 'true');
        
        toast.innerHTML = `
            <div class="d-flex">
                <div class="toast-body">
                    ${message}
                </div>
                <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast" aria-label="Close"></button>
            </div>
        `;
        
        // Add to container
        const toastContainer = document.querySelector('.toast-container');
        if (toastContainer) {
            toastContainer.appendChild(toast);
        } else {
            // Create container if it doesn't exist
            const newContainer = document.createElement('div');
            newContainer.className = 'toast-container position-fixed bottom-0 end-0 p-3';
            newContainer.appendChild(toast);
            document.body.appendChild(newContainer);
        }
        
        // Initialize and show the toast
        const bsToast = new bootstrap.Toast(toast);
        bsToast.show();
        
        // Remove after hidden
        toast.addEventListener('hidden.bs.toast', function() {
            this.remove();
        });
    }
});
