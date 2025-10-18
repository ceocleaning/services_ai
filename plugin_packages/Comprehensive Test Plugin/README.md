# Comprehensive Test Plugin

## 🎯 Purpose

This plugin is designed to **test and verify** that the entire plugin architecture works correctly by implementing **ALL available hooks** in the system.

## ✅ What It Tests

### Lead Hooks (3)
- ✅ `lead_created` - When a new lead is created
- ✅ `lead_updated` - When a lead is updated
- ✅ `lead_deleted` - When a lead is deleted

### Booking Hooks (5)
- ✅ `booking_created` - When a new booking is created
- ✅ `booking_updated` - When a booking is updated
- ✅ `booking_deleted` - When a booking is deleted
- ✅ `booking_confirmed` - When a booking is confirmed
- ✅ `booking_cancelled` - When a booking is cancelled

### Invoice Hooks (3)
- ✅ `invoice_created` - When a new invoice is created
- ✅ `invoice_updated` - When an invoice is updated
- ✅ `invoice_paid` - When an invoice is paid

### User Hooks (3)
- ✅ `user_registered` - When a new user registers
- ✅ `user_login` - When a user logs in
- ✅ `user_logout` - When a user logs out

### Business Hooks (2)
- ✅ `business_created` - When a new business is created
- ✅ `business_updated` - When a business is updated

### Communication Hooks (2)
- ✅ `email_sent` - When an email is sent
- ✅ `sms_sent` - When an SMS is sent

### Reporting Hooks (1)
- ✅ `report_generated` - When a report is generated

### API Hooks (2)
- ✅ `api_request` - Before API request is processed
- ✅ `api_response` - After API response is generated

### UI Hooks (4)
- ✅ `dashboard_widget` - Renders custom dashboard widget
- ✅ `inject_head` - Injects content into page `<head>`
- ✅ `inject_footer` - Injects content into page footer
- ✅ `modify_booking_form` - Modifies booking form fields

### Plugin Lifecycle Hooks (2)
- ✅ `plugin_installed` - When plugin is installed
- ✅ `plugin_uninstalled` - When plugin is uninstalled

### Data Hooks (3)
- ✅ `data_export` - When data is exported
- ✅ `settings_page` - Renders custom settings page
- ✅ `register_routes` - Registers custom URL routes

## 📊 Total Hooks: 30

## 🚀 Installation

1. **Copy plugin to plugin_packages directory** (already done)

2. **Install via Django Admin:**
   - Go to `/admin/plugins/plugin/`
   - Click "Add Plugin"
   - Select `comprehensive_test_plugin` from dropdown
   - Click "Save"

3. **Approve the plugin:**
   - In the plugin list, find "Comprehensive Test Plugin"
   - Change status to "Approved"
   - Enable the plugin

4. **Configure permissions:**
   - Click on the plugin
   - Go to "Permissions" tab
   - Enable all required permissions:
     - `read_leads`
     - `write_leads`
     - `read_bookings`
     - `write_bookings`
     - `read_invoices`
     - `write_invoices`
     - `send_notifications`
     - `access_api`
     - `modify_ui`

## 🧪 Testing

### Test 1: Lead Created
1. Create a new lead
2. **Expected:** 
   - Console log: `[TEST PLUGIN] Hook 'lead_created' called`
   - Toast notification: "✅ Test Plugin: New lead created - [Name]"

### Test 2: Booking Created
1. Create a new booking
2. **Expected:**
   - Console log: `[TEST PLUGIN] Hook 'booking_created' called`
   - Toast notification: "📅 Test Plugin: New booking created - [Date]"

### Test 3: Dashboard Widget
1. Go to dashboard
2. **Expected:**
   - Widget showing "Test Plugin Status"
   - Total hook calls displayed
   - List of all hooks called

### Test 4: UI Injection
1. View any page
2. **Expected:**
   - Green badge in bottom-left: "✓ Test Plugin Active"
   - Custom styles applied

### Test 5: All Other Hooks
- Update a lead → `lead_updated` hook
- Delete a lead → `lead_deleted` hook
- Confirm booking → `booking_confirmed` hook
- Cancel booking → `booking_cancelled` hook
- Create invoice → `invoice_created` hook
- Pay invoice → `invoice_paid` hook
- Register user → `user_registered` hook
- Generate report → `report_generated` hook

## 📝 What to Look For

### In Django Console
```
[TEST PLUGIN] [2025-10-18 17:30:00] Hook 'lead_created' called (#1)
[TEST PLUGIN]   Details: Lead: John Doe
[TEST PLUGIN] [2025-10-18 17:30:05] Hook 'booking_created' called (#1)
[TEST PLUGIN]   Details: Booking ID: 123
```

### In Browser
- Toast notifications for each action
- Dashboard widget with statistics
- Green badge in bottom-left corner
- Custom styles applied

### In Network Tab
- SSE connection to `/events/user-{id}/`
- Events being received for notifications

## ✅ Success Criteria

The plugin architecture is working correctly if:

1. ✅ Plugin installs without errors
2. ✅ All permissions can be enabled
3. ✅ Hooks are called when events occur
4. ✅ Notifications appear in browser
5. ✅ Dashboard widget renders
6. ✅ UI injections work (badge appears)
7. ✅ Console logs show hook executions
8. ✅ No errors in Django console
9. ✅ No errors in browser console

## 🎯 Hook Call Counter

The plugin tracks how many times each hook has been called. View statistics:

1. **Dashboard Widget** - Shows total calls and breakdown
2. **Console Logs** - Each log shows call count: `(#1)`, `(#2)`, etc.
3. **Settings Page** - Custom page shows plugin is working

## 🔧 Settings

The plugin has 3 configurable settings:

1. **Enable Detailed Logging** (boolean)
   - Default: `true`
   - Enables console logging for all hooks

2. **Notification Level** (select)
   - Options: `all`, `important`, `critical`
   - Default: `all`
   - Controls which notifications are sent

3. **Test Mode** (boolean)
   - Default: `true`
   - When enabled, plugin only logs (no modifications)

## 📊 Expected Output

After running through all tests, you should see:

```
[TEST PLUGIN] Plugin Statistics:
  - lead_created: 5 calls
  - lead_updated: 3 calls
  - booking_created: 2 calls
  - booking_confirmed: 1 call
  - invoice_created: 1 call
  - dashboard_widget: 10 calls
  - inject_head: 10 calls
  - inject_footer: 10 calls
  
Total: 42 hook calls across 8 different hooks
```

## 🐛 Troubleshooting

### Plugin not showing up
- Check plugin is in `plugin_packages/comprehensive_test_plugin/`
- Check `plugin.json` is valid JSON
- Check `main.py` has no syntax errors

### Hooks not being called
- Check plugin is **Approved** and **Enabled**
- Check permissions are enabled
- Check signals are firing in your app

### No notifications appearing
- Check `send_notifications` permission is enabled
- Check SSE connection is open (Network tab)
- Check JavaScript console for errors

### No dashboard widget
- Check `modify_ui` permission is enabled
- Check dashboard template includes plugin widgets
- Check console for errors

## 🎉 Success!

If all tests pass, your plugin architecture is working perfectly! 🚀

The system supports:
- ✅ 30 different hooks
- ✅ Real-time notifications via SSE
- ✅ UI modifications and injections
- ✅ Custom dashboard widgets
- ✅ API interception
- ✅ Data export extensions
- ✅ Custom settings pages
- ✅ Permission-based access control

**Your plugin system is production-ready!** 🎊
