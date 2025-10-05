// bookings-index.js - Enhance the bookings index page

document.addEventListener('DOMContentLoaded', function() {
    // Advanced Filters Toggle
    const toggleAdvancedBtn = document.getElementById('toggleAdvanced');
    const advancedContent = document.getElementById('advancedContent');
    const advancedToggleIcon = document.getElementById('advancedToggleIcon');
    
    if (toggleAdvancedBtn) {
        toggleAdvancedBtn.addEventListener('click', function() {
            if (advancedContent.style.display === 'none') {
                advancedContent.style.display = 'block';
                advancedToggleIcon.classList.remove('fa-chevron-down');
                advancedToggleIcon.classList.add('fa-chevron-up');
            } else {
                advancedContent.style.display = 'none';
                advancedToggleIcon.classList.remove('fa-chevron-up');
                advancedToggleIcon.classList.add('fa-chevron-down');
            }
        });
    }
    
    // Quick Filter Buttons
    const quickFilterBtns = document.querySelectorAll('.quick-filter-btn');
    const statusInput = document.getElementById('status');
    const filterForm = document.getElementById('booking-filter-form');
    
    quickFilterBtns.forEach(btn => {
        btn.addEventListener('click', function() {
            const filterValue = this.getAttribute('data-value');
            
            // Update hidden status input
            if (statusInput) {
                statusInput.value = filterValue;
            }
            
            // Update active state
            quickFilterBtns.forEach(b => b.classList.remove('active'));
            this.classList.add('active');
            
            // Submit form
            if (filterForm) {
                filterForm.submit();
            }
        });
    });
    
    // Date Preset Buttons
    const datePresetBtns = document.querySelectorAll('.date-preset');
    const dateFromInput = document.getElementById('date_from');
    const dateToInput = document.getElementById('date_to');
    
    datePresetBtns.forEach(btn => {
        btn.addEventListener('click', function() {
            const preset = this.getAttribute('data-preset');
            const today = new Date();
            let fromDate, toDate;
            
            switch(preset) {
                case 'today':
                    fromDate = toDate = today;
                    break;
                case 'tomorrow':
                    fromDate = toDate = new Date(today.setDate(today.getDate() + 1));
                    break;
                case 'this_week':
                    fromDate = new Date(today.setDate(today.getDate() - today.getDay()));
                    toDate = new Date(today.setDate(today.getDate() - today.getDay() + 6));
                    break;
                case 'next_week':
                    fromDate = new Date(today.setDate(today.getDate() - today.getDay() + 7));
                    toDate = new Date(today.setDate(today.getDate() - today.getDay() + 13));
                    break;
                case 'this_month':
                    fromDate = new Date(today.getFullYear(), today.getMonth(), 1);
                    toDate = new Date(today.getFullYear(), today.getMonth() + 1, 0);
                    break;
                case 'clear':
                    dateFromInput.value = '';
                    dateToInput.value = '';
                    return;
            }
            
            if (fromDate && dateFromInput) {
                dateFromInput.value = fromDate.toISOString().split('T')[0];
            }
            if (toDate && dateToInput) {
                dateToInput.value = toDate.toISOString().split('T')[0];
            }
        });
    });
    
    // Date range validation
    if (dateFromInput && dateToInput) {
        dateFromInput.addEventListener('change', function() {
            if (dateToInput.value && this.value > dateToInput.value) {
                dateToInput.value = this.value;
            }
        });
        
        dateToInput.addEventListener('change', function() {
            if (dateFromInput.value && this.value < dateFromInput.value) {
                dateFromInput.value = this.value;
            }
        });
    }
    
    // Initialize tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function(tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
    
    // Confirm booking cancellation
    const cancelButtons = document.querySelectorAll('.cancel-booking');
    if (cancelButtons) {
        cancelButtons.forEach(button => {
            button.addEventListener('click', function(e) {
                if (!confirm('Are you sure you want to cancel this booking?')) {
                    e.preventDefault();
                }
            });
        });
    }
    
    // Highlight today's bookings
    const today = new Date().toISOString().split('T')[0];
    document.querySelectorAll('tr[data-date]').forEach(row => {
        if (row.dataset.date === today) {
            row.classList.add('table-primary', 'today-booking');
        }
    });
    
    // Load saved view preference
    const savedView = localStorage.getItem('bookingsViewPreference') || 'list';
    if (savedView === 'card') {
        toggleView('card');
    }
});

// Toggle between list and card view
function toggleView(viewType) {
    const listView = document.getElementById('listView');
    const cardView = document.getElementById('cardView');
    const listViewBtn = document.getElementById('listViewBtn');
    const cardViewBtn = document.getElementById('cardViewBtn');
    
    if (viewType === 'list') {
        listView.style.display = 'block';
        cardView.style.display = 'none';
        listViewBtn.classList.add('active');
        cardViewBtn.classList.remove('active');
        localStorage.setItem('bookingsViewPreference', 'list');
    } else {
        listView.style.display = 'none';
        cardView.style.display = 'block';
        listViewBtn.classList.remove('active');
        cardViewBtn.classList.add('active');
        localStorage.setItem('bookingsViewPreference', 'card');
    }
}
