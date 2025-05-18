/**
 * Base JavaScript for AI Appointment Assistant
 * Handles common functionality across all pages
 */

document.addEventListener('DOMContentLoaded', function() {
    // Initialize Bootstrap tooltips
    initTooltips();
    
    // Initialize Bootstrap toasts
    initToasts();
    
    // Navbar scroll behavior
    initNavbarScroll();
});

// Dark mode is now set as default in the HTML

/**
 * Initialize Bootstrap tooltips
 */
function initTooltips() {
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function(tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
}

/**
 * Initialize Bootstrap toasts
 */
function initToasts() {
    const toastElList = [].slice.call(document.querySelectorAll('.toast'));
    toastElList.map(function(toastEl) {
        return new bootstrap.Toast(toastEl, {
            autohide: true,
            delay: 5000
        }).show();
    });
}

/**
 * Initialize navbar scroll behavior
 * Adds a shadow and changes background opacity when scrolling
 */
function initNavbarScroll() {
    const navbar = document.querySelector('.navbar');
    
    if (navbar) {
        window.addEventListener('scroll', function() {
            if (window.scrollY > 10) {
                navbar.classList.add('navbar-scrolled');
            } else {
                navbar.classList.remove('navbar-scrolled');
            }
        });
    }
}

/**
 * Utility function to format dates
 * @param {Date} date - The date to format
 * @param {String} format - The format to use (short, medium, long)
 * @returns {String} Formatted date string
 */
function formatDate(date, format = 'medium') {
    if (!date) return '';
    
    const dateObj = new Date(date);
    
    switch (format) {
        case 'short':
            return dateObj.toLocaleDateString();
        case 'long':
            return dateObj.toLocaleDateString(undefined, { 
                weekday: 'long', 
                year: 'numeric', 
                month: 'long', 
                day: 'numeric' 
            });
        case 'time':
            return dateObj.toLocaleTimeString(undefined, { 
                hour: '2-digit', 
                minute: '2-digit' 
            });
        case 'datetime':
            return dateObj.toLocaleDateString() + ' ' + 
                   dateObj.toLocaleTimeString(undefined, { 
                       hour: '2-digit', 
                       minute: '2-digit' 
                   });
        case 'medium':
        default:
            return dateObj.toLocaleDateString(undefined, { 
                year: 'numeric', 
                month: 'short', 
                day: 'numeric' 
            });
    }
}

/**
 * Add a CSS class to an element temporarily
 * @param {HTMLElement} element - The element to add the class to
 * @param {String} className - The class to add
 * @param {Number} duration - Duration in milliseconds
 */
function addTemporaryClass(element, className, duration = 1000) {
    if (!element) return;
    
    element.classList.add(className);
    
    setTimeout(() => {
        element.classList.remove(className);
    }, duration);
}
