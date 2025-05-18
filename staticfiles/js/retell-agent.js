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
    
    // Confirm delete
    const deleteButtons = document.querySelectorAll('.btn-outline-danger[onclick]');
    deleteButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            if (!confirm('Are you sure you want to delete this agent?')) {
                e.preventDefault();
            }
        });
    });
    
    // Card hover effects
    const cards = document.querySelectorAll('.card');
    cards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            card.classList.add('shadow-sm');
        });
        
        card.addEventListener('mouseleave', function() {
            card.classList.remove('shadow-sm');
        });
    });
});
