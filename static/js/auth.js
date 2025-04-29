/**
 * Auth JavaScript for Services AI Authentication Pages
 * Handles authentication specific functionality
 */

document.addEventListener('DOMContentLoaded', function() {
    // Initialize password visibility toggles
    initPasswordToggles();
    
    // Initialize password strength meter
    initPasswordStrengthMeter();
    
    // Initialize form validation
    initFormValidation();
});

/**
 * Initialize password visibility toggles
 */
function initPasswordToggles() {
    const passwordToggles = document.querySelectorAll('.password-toggle');
    
    passwordToggles.forEach(toggle => {
        toggle.addEventListener('click', function() {
            const passwordInput = this.previousElementSibling;
            
            // Toggle password visibility
            if (passwordInput.type === 'password') {
                passwordInput.type = 'text';
                this.innerHTML = '<i class="fas fa-eye-slash"></i>';
            } else {
                passwordInput.type = 'password';
                this.innerHTML = '<i class="fas fa-eye"></i>';
            }
        });
    });
}

/**
 * Initialize password strength meter
 */
function initPasswordStrengthMeter() {
    const passwordInput = document.getElementById('password');
    const strengthMeter = document.querySelector('.password-strength-meter');
    const strengthText = document.querySelector('.password-strength-text');
    
    if (!passwordInput || !strengthMeter) return;
    
    passwordInput.addEventListener('input', function() {
        const strength = calculatePasswordStrength(this.value);
        updateStrengthMeter(strength, strengthMeter, strengthText);
    });
}

/**
 * Calculate password strength
 * @param {string} password - The password to evaluate
 * @returns {string} - Strength level: 'weak', 'medium', 'good', or 'strong'
 */
function calculatePasswordStrength(password) {
    if (!password) return '';
    
    // Calculate password strength
    let strength = 0;
    
    // Length check
    if (password.length >= 8) strength += 1;
    if (password.length >= 12) strength += 1;
    
    // Character variety checks
    if (/[A-Z]/.test(password)) strength += 1;
    if (/[a-z]/.test(password)) strength += 1;
    if (/[0-9]/.test(password)) strength += 1;
    if (/[^A-Za-z0-9]/.test(password)) strength += 1;
    
    // Determine strength level
    if (strength <= 2) return 'weak';
    if (strength <= 4) return 'medium';
    if (strength <= 5) return 'good';
    return 'strong';
}

/**
 * Update the strength meter UI
 * @param {string} strength - Strength level
 * @param {HTMLElement} meter - The meter element
 * @param {HTMLElement} text - The text element
 */
function updateStrengthMeter(strength, meter, text) {
    // Remove all strength classes
    meter.classList.remove('strength-weak', 'strength-medium', 'strength-good', 'strength-strong');
    
    if (!strength) {
        if (text) text.textContent = '';
        return;
    }
    
    // Add appropriate class
    meter.classList.add(`strength-${strength}`);
    
    // Update text if element exists
    if (text) {
        switch (strength) {
            case 'weak':
                text.textContent = 'Weak - Add more characters and variety';
                text.className = 'password-strength-text text-danger small';
                break;
            case 'medium':
                text.textContent = 'Medium - Add special characters';
                text.className = 'password-strength-text text-warning small';
                break;
            case 'good':
                text.textContent = 'Good - Consider a longer password';
                text.className = 'password-strength-text text-info small';
                break;
            case 'strong':
                text.textContent = 'Strong password';
                text.className = 'password-strength-text text-success small';
                break;
        }
    }
}

/**
 * Initialize form validation
 */
function initFormValidation() {
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
}

/**
 * Check if passwords match
 * @param {string} password - The password
 * @param {string} confirmPassword - The confirmation password
 * @returns {boolean} - Whether passwords match
 */
function passwordsMatch(password, confirmPassword) {
    return password === confirmPassword;
}

/**
 * Update password match feedback
 * @param {HTMLElement} confirmPasswordInput - The confirm password input
 * @param {boolean} match - Whether passwords match
 */
function updatePasswordMatchFeedback(confirmPasswordInput, match) {
    if (!confirmPasswordInput.value) {
        confirmPasswordInput.setCustomValidity('');
        return;
    }
    
    if (match) {
        confirmPasswordInput.setCustomValidity('');
    } else {
        confirmPasswordInput.setCustomValidity('Passwords do not match');
    }
}
