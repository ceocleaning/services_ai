// bookings-create-booking.js - Enhance Create Booking page

document.addEventListener('DOMContentLoaded', function() {
    // Optionally, enhance form UX (e.g., dynamic field toggling, validation)
    const form = document.getElementById('create-booking-form');
    if (!form) return;

    // Example: Highlight required fields on submit if empty
    form.addEventListener('submit', function(e) {
        let valid = true;
        form.querySelectorAll('[required]').forEach(function(input) {
            if (!input.value) {
                input.classList.add('is-invalid');
                valid = false;
            } else {
                input.classList.remove('is-invalid');
            }
        });
        if (!valid) {
            e.preventDefault();
        }
    });

    // Remove highlight on input
    form.querySelectorAll('[required]').forEach(function(input) {
        input.addEventListener('input', function() {
            if (input.value) {
                input.classList.remove('is-invalid');
            }
        });
    });
});
