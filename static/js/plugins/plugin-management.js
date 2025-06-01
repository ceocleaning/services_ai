/**
 * Plugin Management JavaScript
 * Enhances the plugin management interface with interactive features
 */

document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Flash message auto-dismiss
    setTimeout(function() {
        const alerts = document.querySelectorAll('.alert-dismissible:not(.alert-warning):not(.alert-danger)');
        alerts.forEach(function(alert) {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        });
    }, 5000);

    // Plugin toggle status handler
    const toggleForms = document.querySelectorAll('form[data-plugin-toggle]');
    toggleForms.forEach(function(form) {
        form.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const formData = new FormData(form);
            const url = form.getAttribute('action');
            
            fetch(url, {
                method: 'POST',
                body: formData,
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    const toggleBtn = form.querySelector('button');
                    if (data.enabled) {
                        toggleBtn.classList.remove('btn-success');
                        toggleBtn.classList.add('btn-warning');
                        toggleBtn.innerHTML = '<i class="fas fa-pause-circle"></i> Disable';
                    } else {
                        toggleBtn.classList.remove('btn-warning');
                        toggleBtn.classList.add('btn-success');
                        toggleBtn.innerHTML = '<i class="fas fa-play-circle"></i> Enable';
                    }
                    
                    // Update status badge
                    const statusBadge = document.querySelector('.plugin-status-badge');
                    if (statusBadge) {
                        if (data.enabled) {
                            statusBadge.classList.remove('bg-danger');
                            statusBadge.classList.add('bg-success');
                            statusBadge.textContent = 'Enabled';
                        } else {
                            statusBadge.classList.remove('bg-success');
                            statusBadge.classList.add('bg-danger');
                            statusBadge.textContent = 'Disabled';
                        }
                    }
                    
                    // Show success message
                    showToast('Success', data.message, 'success');
                } else {
                    showToast('Error', data.message || 'An error occurred', 'danger');
                }
            })
            .catch(error => {
                console.error('Error:', error);
                showToast('Error', 'An unexpected error occurred', 'danger');
            });
        });
    });
    
    // Permission toggle handler
    const permissionForms = document.querySelectorAll('form[data-permission-toggle]');
    permissionForms.forEach(function(form) {
        form.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const formData = new FormData(form);
            const url = form.getAttribute('action');
            
            fetch(url, {
                method: 'POST',
                body: formData,
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    const toggleBtn = form.querySelector('button');
                    if (data.enabled) {
                        toggleBtn.classList.remove('btn-secondary');
                        toggleBtn.classList.add('btn-success');
                        toggleBtn.textContent = 'Enabled';
                    } else {
                        toggleBtn.classList.remove('btn-success');
                        toggleBtn.classList.add('btn-secondary');
                        toggleBtn.textContent = 'Disabled';
                    }
                    
                    showToast('Success', data.message, 'success');
                } else {
                    showToast('Error', data.message || 'An error occurred', 'danger');
                }
            })
            .catch(error => {
                console.error('Error:', error);
                showToast('Error', 'An unexpected error occurred', 'danger');
            });
        });
    });
    
    // Helper function to show toast notifications
    function showToast(title, message, type) {
        const toastContainer = document.getElementById('toast-container');
        if (!toastContainer) {
            const container = document.createElement('div');
            container.id = 'toast-container';
            container.className = 'position-fixed bottom-0 end-0 p-3';
            container.style.zIndex = '11';
            document.body.appendChild(container);
        }
        
        const toastId = 'toast-' + Date.now();
        const toastHTML = `
            <div id="${toastId}" class="toast" role="alert" aria-live="assertive" aria-atomic="true">
                <div class="toast-header bg-${type} text-white">
                    <strong class="me-auto">${title}</strong>
                    <button type="button" class="btn-close btn-close-white" data-bs-dismiss="toast" aria-label="Close"></button>
                </div>
                <div class="toast-body">
                    ${message}
                </div>
            </div>
        `;
        
      
        toastContainer.insertAdjacentHTML('beforeend', toastHTML);
        
        const toastElement = document.getElementById(toastId);
        const toast = new bootstrap.Toast(toastElement, {
            autohide: true,
            delay: 5000
        });
        
        toast.show();
    }
    
    // File upload enhancements
    const fileInput = document.getElementById('id_plugin_file');
    if (fileInput) {
        const fileLabel = document.querySelector('label[for="id_plugin_file"]');
        const originalLabelText = fileLabel ? fileLabel.textContent : 'Choose file';
        
        fileInput.addEventListener('change', function() {
            if (fileLabel) {
                if (fileInput.files.length > 0) {
                    fileLabel.textContent = fileInput.files[0].name;
                } else {
                    fileLabel.textContent = originalLabelText;
                }
            }
        });
        
        // Add drag and drop functionality
        const uploadZone = document.querySelector('.plugin-upload-zone');
        if (uploadZone) {
            uploadZone.addEventListener('dragover', function(e) {
                e.preventDefault();
                e.stopPropagation();
                this.classList.add('border-primary');
                this.classList.add('bg-light');
            });
            
            uploadZone.addEventListener('dragleave', function(e) {
                e.preventDefault();
                e.stopPropagation();
                this.classList.remove('border-primary');
                this.classList.remove('bg-light');
            });
            
            uploadZone.addEventListener('drop', function(e) {
                e.preventDefault();
                e.stopPropagation();
                this.classList.remove('border-primary');
                this.classList.remove('bg-light');
                
                if (e.dataTransfer.files.length) {
                    fileInput.files = e.dataTransfer.files;
                    
                    // Trigger change event
                    const event = new Event('change', { bubbles: true });
                    fileInput.dispatchEvent(event);
                }
            });
            
            uploadZone.addEventListener('click', function() {
                fileInput.click();
            });
        }
    }
});
