/**
 * Plugin Notification System
 * Listens for SSE events and displays toast notifications
 */

(function() {
    'use strict';

    // Check if user is authenticated
    const userId = document.body.dataset.userId;
    if (!userId) {
        console.log('[Notifications] User not authenticated, skipping SSE connection');
        return;
    }

    console.log('[Notifications] Initializing SSE for user:', userId);

    // Create EventSource connection
    const eventSource = new EventSource(`/events/user-${userId}/`);

    // Handle incoming messages
    eventSource.addEventListener('message', function(e) {
        console.log('[Notifications] Received event:', e.data);
        
        try {
            const data = JSON.parse(e.data);
            showNotification(data);
        } catch (error) {
            console.error('[Notifications] Error parsing event data:', error);
        }
    });

    // Handle connection open
    eventSource.addEventListener('open', function(e) {
        console.log('[Notifications] SSE connection opened');
    });

    // Handle errors
    eventSource.addEventListener('error', function(e) {
        console.error('[Notifications] SSE connection error:', e);
        if (eventSource.readyState === EventSource.CLOSED) {
            console.log('[Notifications] SSE connection closed');
        }
    });

    /**
     * Display a notification
     */
    function showNotification(data) {
        const message = data.message || 'Notification';
        const type = data.type || 'info';
        const plugin = data.plugin || 'Plugin';
        
        console.log(`[Notifications] Showing ${type} notification:`, message);

        // Try to use Bootstrap toast if available
        if (typeof bootstrap !== 'undefined' && bootstrap.Toast) {
            showBootstrapToast(message, type, plugin);
        } 
        // Try to use browser notification API
        else if ('Notification' in window && Notification.permission === 'granted') {
            showBrowserNotification(message, type, plugin);
        }
        // Fallback to alert
        else {
            alert(`[${plugin}] ${message}`);
        }
    }

    /**
     * Show Bootstrap toast notification
     */
    function showBootstrapToast(message, type, plugin) {
        // Create toast container if it doesn't exist
        let toastContainer = document.getElementById('toast-container');
        if (!toastContainer) {
            toastContainer = document.createElement('div');
            toastContainer.id = 'toast-container';
            toastContainer.className = 'toast-container position-fixed top-0 end-0 p-3';
            toastContainer.style.zIndex = '9999';
            document.body.appendChild(toastContainer);
        }

        // Map notification types to Bootstrap classes
        const typeMap = {
            'success': 'bg-success text-white',
            'error': 'bg-danger text-white',
            'warning': 'bg-warning text-dark',
            'info': 'bg-info text-white'
        };
        const bgClass = typeMap[type] || 'bg-primary text-white';

        // Create toast element
        const toastId = 'toast-' + Date.now();
        const toastHtml = `
            <div id="${toastId}" class="toast" role="alert" aria-live="assertive" aria-atomic="true">
                <div class="toast-header ${bgClass}">
                    <i class="fas fa-bell me-2"></i>
                    <strong class="me-auto">${escapeHtml(plugin)}</strong>
                    <small>Just now</small>
                    <button type="button" class="btn-close btn-close-white" data-bs-dismiss="toast" aria-label="Close"></button>
                </div>
                <div class="toast-body">
                    ${escapeHtml(message)}
                </div>
            </div>
        `;

        toastContainer.insertAdjacentHTML('beforeend', toastHtml);

        // Show the toast
        const toastElement = document.getElementById(toastId);
        const toast = new bootstrap.Toast(toastElement, {
            autohide: true,
            delay: 5000
        });
        toast.show();

        // Remove toast element after it's hidden
        toastElement.addEventListener('hidden.bs.toast', function() {
            toastElement.remove();
        });
    }

    /**
     * Show browser notification
     */
    function showBrowserNotification(message, type, plugin) {
        const notification = new Notification(plugin, {
            body: message,
            icon: '/static/images/notification-icon.png', // Update with your icon path
            badge: '/static/images/badge-icon.png'
        });

        notification.onclick = function() {
            window.focus();
            notification.close();
        };
    }

    /**
     * Escape HTML to prevent XSS
     */
    function escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }

    /**
     * Request notification permission (optional)
     */
    function requestNotificationPermission() {
        if ('Notification' in window && Notification.permission === 'default') {
            Notification.requestPermission().then(function(permission) {
                console.log('[Notifications] Permission:', permission);
            });
        }
    }

    // Optionally request notification permission on page load
    // requestNotificationPermission();

})();
