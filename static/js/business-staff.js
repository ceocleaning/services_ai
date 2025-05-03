// Staff Management JavaScript
document.addEventListener('DOMContentLoaded', function() {
    // Handle toggle staff status
    const statusToggles = document.querySelectorAll('.toggle-staff-status');
    statusToggles.forEach(toggle => {
        toggle.addEventListener('change', function() {
            const staffId = this.dataset.staffId;
            const isActive = this.checked;
            
            // Send AJAX request to update staff status
            fetch('/business/update_staff_status/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken')
                },
                body: JSON.stringify({
                    staff_id: staffId,
                    is_active: isActive
                })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    // Show success message
                    showToast('Staff status updated successfully', 'success');
                    
                    // Update UI if needed
                    const staffCard = this.closest('.staff-card');
                    const statusIndicator = staffCard.querySelector('.status-indicator');
                    
                    if (isActive) {
                        statusIndicator.classList.add('active');
                        statusIndicator.classList.remove('inactive');
                    } else {
                        statusIndicator.classList.add('inactive');
                        statusIndicator.classList.remove('active');
                    }
                } else {
                    // Show error message
                    showToast('Error updating staff status: ' + data.message, 'error');
                    // Revert toggle state
                    this.checked = !isActive;
                }
            })
            .catch(error => {
                console.error('Error:', error);
                showToast('An error occurred while updating staff status', 'error');
                // Revert toggle state
                this.checked = !isActive;
            });
        });
    });
    
    // Initialize form validation for add staff form
    const addStaffForm = document.getElementById('addStaffForm');
    if (addStaffForm) {
        addStaffForm.addEventListener('submit', function(event) {
            if (!this.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            this.classList.add('was-validated');
        });
    }
    
    // Staff Role Management
    
    // Edit role button click
    const editRoleButtons = document.querySelectorAll('.edit-role-btn');
    const editRoleModal = document.getElementById('editRoleModal');
    
    if (editRoleButtons.length && editRoleModal) {
        editRoleButtons.forEach(button => {
            button.addEventListener('click', function() {
                const roleId = this.dataset.roleId;
                const roleName = this.dataset.roleName;
                const roleDescription = this.dataset.roleDescription;
                const roleActive = this.dataset.roleActive === 'true';
                
                // Set form values
                document.getElementById('editRoleId').value = roleId;
                document.getElementById('editRoleName').value = roleName;
                document.getElementById('editRoleDescription').value = roleDescription;
                document.getElementById('editRoleActive').checked = roleActive;
                
                // Show modal
                const modal = new bootstrap.Modal(editRoleModal);
                modal.show();
            });
        });
    }
    
    // Delete role button click
    const deleteRoleButtons = document.querySelectorAll('.delete-role-btn');
    
    if (deleteRoleButtons.length) {
        deleteRoleButtons.forEach(button => {
            button.addEventListener('click', function() {
                const roleId = this.dataset.roleId;
                const roleName = this.dataset.roleName;
                
                if (confirm(`Are you sure you want to delete the role "${roleName}"? This may affect staff members assigned to this role.`)) {
                    // Send AJAX request to delete role
                    fetch('/business/staff-role/delete/', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                            'X-CSRFToken': getCookie('csrftoken')
                        },
                        body: JSON.stringify({
                            role_id: roleId
                        })
                    })
                    .then(response => response.json())
                    .then(data => {
                        if (data.success) {
                            // Show success message
                            showToast('Role deleted successfully', 'success');
                            // Reload page to update role list
                            window.location.reload();
                        } else {
                            // Show error message
                            showToast('Error deleting role: ' + data.message, 'error');
                        }
                    })
                    .catch(error => {
                        console.error('Error:', error);
                        showToast('An error occurred while deleting role', 'error');
                    });
                }
            });
        });
    }
    
    // Function to get CSRF token from cookies
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    
    // Function to show toast notifications
    function showToast(message, type = 'info') {
        // Check if Bootstrap toast is available
        if (typeof bootstrap !== 'undefined' && bootstrap.Toast) {
            // Create toast element
            const toastEl = document.createElement('div');
            toastEl.className = `toast align-items-center text-white bg-${type === 'error' ? 'danger' : type} border-0`;
            toastEl.setAttribute('role', 'alert');
            toastEl.setAttribute('aria-live', 'assertive');
            toastEl.setAttribute('aria-atomic', 'true');
            
            toastEl.innerHTML = `
                <div class="d-flex">
                    <div class="toast-body">
                        ${message}
                    </div>
                    <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast" aria-label="Close"></button>
                </div>
            `;
            
            // Add to container or body
            let toastContainer = document.querySelector('.toast-container');
            if (!toastContainer) {
                toastContainer = document.createElement('div');
                toastContainer.className = 'toast-container position-fixed bottom-0 end-0 p-3';
                document.body.appendChild(toastContainer);
            }
            
            toastContainer.appendChild(toastEl);
            
            // Initialize and show toast
            const toast = new bootstrap.Toast(toastEl, {
                autohide: true,
                delay: 5000
            });
            toast.show();
            
            // Remove toast element after it's hidden
            toastEl.addEventListener('hidden.bs.toast', function() {
                toastEl.remove();
            });
        } else {
            // Fallback to alert if Bootstrap is not available
            if (type === 'error') {
                alert('Error: ' + message);
            } else {
                alert(message);
            }
        }
    }
});
