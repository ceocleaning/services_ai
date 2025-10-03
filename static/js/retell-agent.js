/**
 * Retell Agent JavaScript
 * Handles form validation and UI interactions for the Retell Agent module
 */

document.addEventListener('DOMContentLoaded', function() {
    // Form validation
    const forms = document.querySelectorAll('.needs-validation');
    
    Array.from(forms).forEach(form => {
        form.addEventListener('submit', event => {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            
            form.classList.add('was-validated');
        }, false);
    });
    
    // Phone number formatting
    const phoneInput = document.getElementById('retell_phone_number');
    if (phoneInput) {
        phoneInput.addEventListener('input', function(e) {
            let value = e.target.value;
            
            // Ensure it starts with +
            if (value && !value.startsWith('+')) {
                e.target.value = '+' + value;
            }
            
            // Remove non-numeric characters except +
            e.target.value = e.target.value.replace(/[^\d+]/g, '');
        });
    }
    
    // Toast notifications
    const toastElements = document.querySelectorAll('.toast');
    if (toastElements.length > 0) {
        toastElements.forEach(toast => {
            new bootstrap.Toast(toast, {
                autohide: true,
                delay: 5000
            }).show();
        });
    }
    
    // Tooltips initialization
    const tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]');
    if (tooltipTriggerList.length > 0) {
        [...tooltipTriggerList].map(tooltipTriggerEl => new bootstrap.Tooltip(tooltipTriggerEl));
    }
    
    // Confirm delete
    const deleteButtons = document.querySelectorAll('.btn-delete-agent');
    deleteButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            if (!confirm('Are you sure you want to delete this agent?')) {
                e.preventDefault();
            }
        });
    });
});
