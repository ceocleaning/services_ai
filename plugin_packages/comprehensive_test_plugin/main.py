"""
Comprehensive Test Plugin
Tests all available hooks in the plugin system
Tests dependency management with requests and numpy
"""

from plugins.hooks import hookimpl
from datetime import datetime
import json

# Test dependencies - these will be installed automatically
import requests
import numpy as np


class ComprehensiveTestPlugin:
    """
    A comprehensive test plugin that implements all available hooks
    to verify the plugin architecture works correctly.
    """
    
    def __init__(self):
        self.hook_call_count = {}
    
    def _log_hook_call(self, hook_name, details=""):
        """Log hook execution"""
        self.hook_call_count[hook_name] = self.hook_call_count.get(hook_name, 0) + 1
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[TEST PLUGIN] [{timestamp}] Hook '{hook_name}' called (#{self.hook_call_count[hook_name]})")
        if details:
            print(f"[TEST PLUGIN]   Details: {details}")
    
    # ==================== LEAD HOOKS ====================
    
    @hookimpl
    def lead_created(self, lead, context, api):
        """Hook: Lead Created"""
        self._log_hook_call('lead_created', f"Lead: {lead.get_full_name()}")
        
        # Send notification
        api.send_notification(
            message=f"✅ Test Plugin: New lead created - {lead.get_full_name()}",
            notification_type="success"
        )
    
    @hookimpl
    def lead_updated(self, lead, previous_state, context, api):
        """Hook: Lead Updated"""
        self._log_hook_call('lead_updated', f"Lead: {lead.get_full_name()}")
        
        api.send_notification(
            message=f"📝 Test Plugin: Lead updated - {lead.get_full_name()}",
            notification_type="info"
        )
    
    @hookimpl
    def lead_deleted(self, lead_id, lead_data, context, api):
        """Hook: Lead Deleted"""
        self._log_hook_call('lead_deleted', f"Lead ID: {lead_id}")
        
        api.send_notification(
            message=f"🗑️ Test Plugin: Lead deleted - ID: {lead_id}",
            notification_type="warning"
        )
    
    # ==================== BOOKING HOOKS ====================
    
    @hookimpl
    def booking_created(self, booking, context, api):
        """Hook: Booking Created"""
        self._log_hook_call('booking_created', f"Booking ID: {booking.id}")
        
        api.send_notification(
            message=f"📅 Test Plugin: New booking created - {booking.booking_date}",
            notification_type="success"
        )
    
    @hookimpl
    def booking_updated(self, booking, previous_state, context, api):
        """Hook: Booking Updated"""
        self._log_hook_call('booking_updated', f"Booking ID: {booking.id}")
        
        api.send_notification(
            message=f"📝 Test Plugin: Booking updated - {booking.booking_date}",
            notification_type="info"
        )
    
    @hookimpl
    def booking_deleted(self, booking_id, booking_data, context, api):
        """Hook: Booking Deleted"""
        self._log_hook_call('booking_deleted', f"Booking ID: {booking_id}")
        
        api.send_notification(
            message=f"🗑️ Test Plugin: Booking deleted - ID: {booking_id}",
            notification_type="warning"
        )
    
    @hookimpl
    def booking_confirmed(self, booking, context, api):
        """Hook: Booking Confirmed"""
        self._log_hook_call('booking_confirmed', f"Booking ID: {booking.id}")
        
        api.send_notification(
            message=f"✅ Test Plugin: Booking confirmed - {booking.booking_date}",
            notification_type="success"
        )
    
    @hookimpl
    def booking_cancelled(self, booking, reason, context, api):
        """Hook: Booking Cancelled"""
        self._log_hook_call('booking_cancelled', f"Booking ID: {booking.id}, Reason: {reason}")
        
        api.send_notification(
            message=f"❌ Test Plugin: Booking cancelled - Reason: {reason}",
            notification_type="error"
        )
    
    # ==================== INVOICE HOOKS ====================
    
    @hookimpl
    def invoice_created(self, invoice, context, api):
        """Hook: Invoice Created"""
        self._log_hook_call('invoice_created', f"Invoice ID: {invoice.id}")
        
        api.send_notification(
            message=f"💰 Test Plugin: New invoice created - ID: {invoice.id}",
            notification_type="success"
        )
    
    @hookimpl
    def invoice_updated(self, invoice, previous_state, context, api):
        """Hook: Invoice Updated"""
        self._log_hook_call('invoice_updated', f"Invoice ID: {invoice.id}")
        
        api.send_notification(
            message=f"📝 Test Plugin: Invoice updated - ID: {invoice.id}",
            notification_type="info"
        )
    
    @hookimpl
    def invoice_paid(self, invoice, payment_info, context, api):
        """Hook: Invoice Paid"""
        self._log_hook_call('invoice_paid', f"Invoice ID: {invoice.id}")
        
        api.send_notification(
            message=f"💵 Test Plugin: Invoice paid - ID: {invoice.id}",
            notification_type="success"
        )
    
    # ==================== USER HOOKS ====================
    
    @hookimpl
    def user_registered(self, user, context, api):
        """Hook: User Registered"""
        self._log_hook_call('user_registered', f"User: {user.username}")
        
        api.send_notification(
            message=f"👤 Test Plugin: New user registered - {user.username}",
            notification_type="success"
        )
    
    @hookimpl
    def user_login(self, user, context, api):
        """Hook: User Login"""
        self._log_hook_call('user_login', f"User: {user.username}")
        
        # Don't send notification for login (too frequent)
        pass
    
    @hookimpl
    def user_logout(self, user, context, api):
        """Hook: User Logout"""
        self._log_hook_call('user_logout', f"User: {user.username}")
        
        # Don't send notification for logout
        pass
    
    # ==================== BUSINESS HOOKS ====================
    
    @hookimpl
    def business_created(self, business, context, api):
        """Hook: Business Created"""
        self._log_hook_call('business_created', f"Business: {business.name}")
        
        api.send_notification(
            message=f"🏢 Test Plugin: New business created - {business.name}",
            notification_type="success"
        )
    
    @hookimpl
    def business_updated(self, business, previous_state, context, api):
        """Hook: Business Updated"""
        self._log_hook_call('business_updated', f"Business: {business.name}")
        
        api.send_notification(
            message=f"📝 Test Plugin: Business updated - {business.name}",
            notification_type="info"
        )
    
    # ==================== COMMUNICATION HOOKS ====================
    
    @hookimpl
    def email_sent(self, recipient, subject, template, context, api):
        """Hook: Email Sent"""
        self._log_hook_call('email_sent', f"To: {recipient}, Subject: {subject}")
    
    @hookimpl
    def sms_sent(self, phone, message, context, api):
        """Hook: SMS Sent"""
        self._log_hook_call('sms_sent', f"To: {phone}")
    
    # ==================== REPORTING HOOKS ====================
    
    @hookimpl
    def report_generated(self, report_type, data, context, api):
        """Hook: Report Generated"""
        self._log_hook_call('report_generated', f"Type: {report_type}")
        
        api.send_notification(
            message=f"📊 Test Plugin: Report generated - {report_type}",
            notification_type="info"
        )
    
    # ==================== API HOOKS ====================
    
    @hookimpl
    def api_request(self, endpoint, method, data, context, api):
        """Hook: API Request (before processing)"""
        self._log_hook_call('api_request', f"{method} {endpoint}")
        
        # Can modify request data here
        return None  # Return None to not modify
    
    @hookimpl
    def api_response(self, endpoint, method, response_data, context, api):
        """Hook: API Response (after processing)"""
        self._log_hook_call('api_response', f"{method} {endpoint}")
        
        # Can modify response data here
        return None  # Return None to not modify
    
    # ==================== UI HOOKS ====================
    
    @hookimpl
    def dashboard_widget(self, plugin_id, context, api):
        """Hook: Dashboard Widget"""
        self._log_hook_call('dashboard_widget', f"Plugin ID: {plugin_id}")
        
        # Return HTML for dashboard widget
        total_calls = sum(self.hook_call_count.values())
        
        widget_html = f"""
        <div class="card border-primary mb-3">
            <div class="card-header bg-primary text-white">
                <i class="fas fa-plug me-2"></i>Test Plugin Status
            </div>
            <div class="card-body">
                <h5 class="card-title">Plugin Architecture Test</h5>
                <p class="card-text">
                    <strong>Total Hook Calls:</strong> {total_calls}<br>
                    <strong>Unique Hooks Called:</strong> {len(self.hook_call_count)}<br>
                    <strong>Status:</strong> <span class="badge bg-success">Active</span>
                </p>
                <details>
                    <summary class="btn btn-sm btn-outline-primary">View Hook Statistics</summary>
                    <ul class="list-group mt-2">
        """
        
        for hook_name, count in sorted(self.hook_call_count.items()):
            widget_html += f'<li class="list-group-item d-flex justify-content-between align-items-center">{hook_name}<span class="badge bg-primary rounded-pill">{count}</span></li>'
        
        widget_html += """
                    </ul>
                </details>
            </div>
        </div>
        """
        
        return widget_html
    
    @hookimpl
    def inject_head(self, plugin_id, context, api):
        """Hook: Inject Head Content"""
        self._log_hook_call('inject_head', f"Plugin ID: {plugin_id}")
        
        return """
        <!-- Test Plugin Custom Styles -->
        <style>
            .test-plugin-badge {
                position: fixed;
                bottom: 10px;
                left: 10px;
                background: #28a745;
                color: white;
                padding: 5px 10px;
                border-radius: 5px;
                font-size: 12px;
                z-index: 1000;
                box-shadow: 0 2px 5px rgba(0,0,0,0.2);
            }
        </style>
        """
    
    @hookimpl
    def inject_footer(self, plugin_id, context, api):
        """Hook: Inject Footer Content"""
        self._log_hook_call('inject_footer', f"Plugin ID: {plugin_id}")
        
        return """
        <!-- Test Plugin Badge -->
        <div class="test-plugin-badge">
            <i class="fas fa-check-circle"></i> Test Plugin Active
        </div>
        """
    
    # ==================== PLUGIN LIFECYCLE HOOKS ====================
    
    @hookimpl
    def plugin_installed(self, plugin_id, plugin_info, api):
        """Hook: Plugin Installed"""
        self._log_hook_call('plugin_installed', f"Plugin ID: {plugin_id}")
        
        print("[TEST PLUGIN] ✅ Plugin successfully installed!")
        print(f"[TEST PLUGIN]    Name: {plugin_info.get('name')}")
        print(f"[TEST PLUGIN]    Version: {plugin_info.get('version')}")
    
    @hookimpl
    def plugin_uninstalled(self, plugin_id, api):
        """Hook: Plugin Uninstalled"""
        self._log_hook_call('plugin_uninstalled', f"Plugin ID: {plugin_id}")
        
        print("[TEST PLUGIN] 👋 Plugin uninstalled. Goodbye!")
        print(f"[TEST PLUGIN]    Total hooks called during lifetime: {sum(self.hook_call_count.values())}")
    
    # ==================== DATA HOOKS ====================
    
    @hookimpl
    def data_export(self, export_type, start_date, end_date, context, api):
        """Hook: Data Export"""
        self._log_hook_call('data_export', f"Type: {export_type}, From: {start_date}, To: {end_date}")
        
        # Return additional data to include in export
        return [
            {
                'plugin': 'Comprehensive Test Plugin',
                'export_timestamp': datetime.now().isoformat(),
                'total_hook_calls': sum(self.hook_call_count.values()),
                'hooks_called': list(self.hook_call_count.keys())
            }
        ]
    
    @hookimpl
    def settings_page(self, plugin_id, context, api):
        """Hook: Settings Page"""
        self._log_hook_call('settings_page', f"Plugin ID: {plugin_id}")
        
        # Return custom settings page HTML
        return """
        <div class="card">
            <div class="card-header">
                <h4>Test Plugin Settings</h4>
            </div>
            <div class="card-body">
                <div class="alert alert-info">
                    <i class="fas fa-info-circle me-2"></i>
                    This is a custom settings page rendered by the plugin!
                </div>
                <h5>Plugin Statistics</h5>
                <p>This plugin has been designed to test all available hooks in the system.</p>
                <div class="alert alert-success">
                    <strong>✅ All hooks are working correctly!</strong>
                </div>
            </div>
        </div>
        """
    
    @hookimpl
    def register_routes(self, plugin_id, api):
        """Hook: Register Routes"""
        self._log_hook_call('register_routes', f"Plugin ID: {plugin_id}")
        
        # Import Django modules for views
        from django.shortcuts import render
        from django.http import JsonResponse, HttpResponse
        
        # Define custom view functions
        def test_page_view(request):
            """Custom test page view - Tests dependencies"""
            # Test numpy
            test_array = np.array([10, 20, 30, 40, 50])
            
            html = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <title>Comprehensive Test Plugin</title>
                <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
                <style>
                    body {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); min-height: 100vh; padding: 40px 0; }}
                    .card {{ border-radius: 15px; box-shadow: 0 10px 30px rgba(0,0,0,0.3); }}
                </style>
            </head>
            <body>
                <div class="container">
                    <div class="card">
                        <div class="card-body p-5">
                            <h1 class="text-center mb-4">🎉 Comprehensive Test Plugin</h1>
                            <p class="text-center text-muted">Testing all plugin features including dependencies!</p>
                            
                            <div class="row mt-4">
                                <div class="col-md-4">
                                    <div class="card bg-primary text-white">
                                        <div class="card-body text-center">
                                            <h3>{len(self.hook_call_count)}</h3>
                                            <p>Total Hooks</p>
                                        </div>
                                    </div>
                                </div>
                                <div class="col-md-4">
                                    <div class="card bg-success text-white">
                                        <div class="card-body text-center">
                                            <h3>{sum(self.hook_call_count.values())}</h3>
                                            <p>Total Calls</p>
                                        </div>
                                    </div>
                                </div>
                                <div class="col-md-4">
                                    <div class="card bg-info text-white">
                                        <div class="card-body text-center">
                                            <h3>v1.0.0</h3>
                                            <p>Version</p>
                                        </div>
                                    </div>
                                </div>
                            </div>
                            
                            <div class="mt-4">
                                <h4>📦 Dependencies Test</h4>
                                <div class="alert alert-success">
                                    <strong>NumPy:</strong> v{np.__version__}<br>
                                    <strong>Test Array:</strong> {test_array.tolist()}<br>
                                    <strong>Sum:</strong> {np.sum(test_array)}<br>
                                    <strong>Mean:</strong> {np.mean(test_array)}<br>
                                    <strong>Requests:</strong> v{requests.__version__}
                                </div>
                            </div>
                            
                            <div class="mt-4">
                                <h4>🔗 Available Routes</h4>
                                <ul class="list-group">
                                    <li class="list-group-item">
                                        <strong>Main Page:</strong> /plugin/comprehensive-test-plugin/
                                    </li>
                                    <li class="list-group-item">
                                        <strong>API Endpoint:</strong> /plugin/comprehensive-test-plugin/api/
                                    </li>
                                    <li class="list-group-item">
                                        <strong>Dashboard:</strong> /plugin/comprehensive-test-plugin/dashboard/
                                    </li>
                                </ul>
                            </div>
                        </div>
                    </div>
                </div>
            </body>
            </html>
            """
            return HttpResponse(html)
        
        def test_api_view(request):
            """Custom API endpoint - Tests dependencies"""
            # Test numpy
            test_array = np.array([1, 2, 3, 4, 5])
            numpy_info = {
                'version': np.__version__,
                'array_sum': int(np.sum(test_array)),
                'array_mean': float(np.mean(test_array))
            }
            
            # Test requests (make a simple API call)
            requests_info = {
                'version': requests.__version__,
                'available': True
            }
            
            return JsonResponse({
                'status': 'success',
                'plugin': 'Comprehensive Test Plugin',
                'total_hooks': len(self.hook_call_count),
                'total_calls': sum(self.hook_call_count.values()),
                'hook_stats': self.hook_call_count,
                'dependencies': {
                    'numpy': numpy_info,
                    'requests': requests_info
                },
                'message': 'Plugin API is working! Dependencies loaded successfully!'
            })
        
        def test_dashboard_view(request):
            """Custom dashboard view"""
            user_name = request.user.get_full_name() or request.user.username
            
            # Build hook stats table
            hook_stats_rows = ""
            for hook_name, count in sorted(self.hook_call_count.items()):
                hook_stats_rows += f"""
                <tr>
                    <td>{hook_name}</td>
                    <td><span class="badge bg-primary">{count}</span></td>
                </tr>
                """
            
            html = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <title>Plugin Dashboard</title>
                <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
            </head>
            <body>
                <div class="container mt-5">
                    <h1>📊 Plugin Dashboard</h1>
                    <p class="text-muted">Welcome, {user_name}!</p>
                    
                    <div class="row mt-4">
                        <div class="col-md-6">
                            <div class="card">
                                <div class="card-body">
                                    <h5>Total Hooks: {len(self.hook_call_count)}</h5>
                                    <h5>Total Calls: {sum(self.hook_call_count.values())}</h5>
                                </div>
                            </div>
                        </div>
                    </div>
                    
                    <div class="mt-4">
                        <h4>Hook Execution Stats</h4>
                        <table class="table table-striped">
                            <thead>
                                <tr>
                                    <th>Hook Name</th>
                                    <th>Call Count</th>
                                </tr>
                            </thead>
                            <tbody>
                                {hook_stats_rows}
                            </tbody>
                        </table>
                    </div>
                </div>
            </body>
            </html>
            """
            return HttpResponse(html)
        
        # Return list of custom routes
        # Format: (url_pattern, view_function, name)
        # Note: Routes will be prefixed with 'plugin/{plugin-name}/' automatically
        return [
            ('', test_page_view, 'test_plugin_page'),  # /plugin/comprehensive-test-plugin/
            ('api/', test_api_view, 'test_plugin_api'),  # /plugin/comprehensive-test-plugin/api/
            ('dashboard/', test_dashboard_view, 'test_plugin_dashboard'),  # /plugin/comprehensive-test-plugin/dashboard/
        ]
    
    @hookimpl
    def modify_booking_form(self, plugin_id, form, context, api):
        """Hook: Modify Booking Form"""
        self._log_hook_call('modify_booking_form', f"Plugin ID: {plugin_id}")
        
        # Can modify form fields here
        return None  # Return None to not modify


# Export the plugin class
plugin = ComprehensiveTestPlugin()
