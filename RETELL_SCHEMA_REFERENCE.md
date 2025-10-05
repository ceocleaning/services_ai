# Retell Tools Schema - Quick Reference

## Book Appointment Schema

### **Services Available**
1. **Deep Cleaning** - $150.00 (100 minutes)
   - No customization options
   - Just book the service

2. **Standard Cleaning** - $100.00 (60 minutes)
   - Has 3 customization options (see below)

---

## Service Items for Standard Cleaning

### 1. **Bedroom** (Required)
- **Identifier**: `bedroom`
- **Type**: Number
- **Pricing**: $10.00 per bedroom
- **Duration**: +30 minutes per bedroom
- **Example**: `"bedroom": 3`

### 2. **Driveway Cleaning** (Optional)
- **Identifier**: `do_you_want_driveway_cleaned`
- **Type**: Boolean (Yes/No)
- **Pricing**: 
  - Yes = $10.00
  - No = Free
- **Example**: `"do_you_want_driveway_cleaned": true`

### 3. **Cleaner Product** (Required)
- **Identifier**: `select_cleaner_product`
- **Type**: Select (Dropdown)
- **Options**:
  - `"best cleaner"` = $10.00
  - `"better cleaner"` = $20.00
- **Example**: `"select_cleaner_product": "best cleaner"`

---

## Example Requests

### **Example 1: Standard Cleaning with All Options**
```json
{
  "name": "John Doe",
  "email": "john@example.com",
  "phone": "+1234567890",
  "type_of_service": "Standard Cleaning",
  "bedroom": 3,
  "do_you_want_driveway_cleaned": true,
  "select_cleaner_product": "best cleaner",
  "appointment_date_time": "2025-10-15 14:00",
  "business_id": "bus_430967"
}
```

**Calculation**:
- Base: $100.00
- 3 Bedrooms: 3 × $10 = $30.00
- Driveway: $10.00
- Best Cleaner: $10.00
- **Total: $150.00**
- **Duration: 60 + (3 × 30) = 150 minutes**

---

### **Example 2: Standard Cleaning Minimal**
```json
{
  "name": "Jane Smith",
  "phone": "+1987654321",
  "type_of_service": "Standard Cleaning",
  "bedroom": 1,
  "do_you_want_driveway_cleaned": false,
  "select_cleaner_product": "better cleaner",
  "appointment_date_time": "tomorrow at 2pm",
  "business_id": "bus_430967"
}
```

**Calculation**:
- Base: $100.00
- 1 Bedroom: $10.00
- No Driveway: $0.00
- Better Cleaner: $20.00
- **Total: $130.00**
- **Duration: 60 + 30 = 90 minutes**

---

### **Example 3: Deep Cleaning (No Options)**
```json
{
  "name": "Bob Johnson",
  "email": "bob@example.com",
  "phone": "+1555123456",
  "type_of_service": "Deep Cleaning",
  "appointment_date_time": "2025-10-20 09:00",
  "business_id": "bus_430967"
}
```

**Calculation**:
- Base: $150.00
- **Total: $150.00**
- **Duration: 100 minutes**

---

## Field Mapping

| JSON Field | Identifier | Type | Required | Pricing |
|-----------|-----------|------|----------|---------|
| `bedroom` | `bedroom` | number | Yes (for Standard) | $10/unit |
| `do_you_want_driveway_cleaned` | `do_you_want_driveway_cleaned` | boolean | No | Yes=$10, No=Free |
| `select_cleaner_product` | `select_cleaner_product` | string | Yes (for Standard) | best=$10, better=$20 |

---

## Date/Time Format Examples

The API accepts human-readable formats:
- `"2025-10-15 14:00"` - Explicit date and time
- `"tomorrow at 2pm"` - Relative date
- `"next Monday at 3pm"` - Relative with day
- `"October 20th at 9am"` - Natural language
- `"10/20/2025 at 10:00"` - US format

All formats are converted to `YYYY-MM-DD HH:MM` internally.

---

## Response Format

### **Success Response**:
```json
{
  "success": true,
  "booking_id": "book_309029",
  "message": "BOOKING_CONFIRMED\nBooking ID: book_309029\nService: Standard Cleaning\nDate: 2025-10-15\nTime: 14:00\nDuration: 150 minutes\nTotal Price: $150.0\nStaff: Kashif Mehmood\nCustomizations: 3 bedroom, best cleaner\n\nIMPORTANT: Share the Booking ID book_309029 with the customer..."
}
```

### **Error Response**:
```json
{
  "success": false,
  "booking_id": null,
  "message": "❌ Cannot book appointment at 14:00 on 2025-10-15. Reason: Time slot conflicts with existing booking.\n\nAlternative available times: 15:00, 16:00, 17:00\n\nPlease choose a different time."
}
```

---

## Required vs Optional Fields

### **Always Required**:
- `name`
- `phone`
- `type_of_service`
- `appointment_date_time`
- `business_id`

### **Required for Standard Cleaning**:
- `bedroom`
- `select_cleaner_product`

### **Always Optional**:
- `email`
- `do_you_want_driveway_cleaned`

---

## Validation Rules

### **Service Name**:
- Must be exactly: `"Standard Cleaning"` or `"Deep Cleaning"`
- Case-sensitive
- No variations allowed

### **Bedroom**:
- Must be a positive number
- Typically 1-10
- Cannot be 0 or negative

### **Driveway Cleaning**:
- Accepts: `true`, `false`, `"yes"`, `"no"`, `1`, `0`
- Converted to boolean internally

### **Cleaner Product**:
- Must be exactly: `"best cleaner"` or `"better cleaner"`
- Case-sensitive
- No other values allowed

---

## Common Mistakes

### ❌ **Wrong Service Name**:
```json
{
  "type_of_service": "standard cleaning"  // Wrong: lowercase
}
```
✅ **Correct**: `"type_of_service": "Standard Cleaning"`

---

### ❌ **Wrong Cleaner Product**:
```json
{
  "select_cleaner_product": "Best Cleaner"  // Wrong: capitalized
}
```
✅ **Correct**: `"select_cleaner_product": "best cleaner"`

---

### ❌ **Missing Required Field**:
```json
{
  "type_of_service": "Standard Cleaning",
  // Missing: bedroom and select_cleaner_product
}
```
✅ **Correct**: Include all required fields

---

### ❌ **Wrong Field Name**:
```json
{
  "bedrooms": 3  // Wrong: should be "bedroom" (singular)
}
```
✅ **Correct**: `"bedroom": 3`

---

## Testing Checklist

- [ ] Test Standard Cleaning with all options
- [ ] Test Standard Cleaning with minimal options
- [ ] Test Deep Cleaning (no options)
- [ ] Test with different date/time formats
- [ ] Test with missing required fields (should fail)
- [ ] Test with invalid service name (should fail)
- [ ] Test with invalid cleaner product (should fail)
- [ ] Test with conflicting time slot (should suggest alternatives)

---

## Quick Copy-Paste Templates

### **Standard Cleaning - Full**:
```json
{
  "name": "Customer Name",
  "email": "customer@example.com",
  "phone": "+1234567890",
  "type_of_service": "Standard Cleaning",
  "bedroom": 2,
  "do_you_want_driveway_cleaned": true,
  "select_cleaner_product": "best cleaner",
  "appointment_date_time": "2025-10-15 14:00",
  "business_id": "bus_430967"
}
```

### **Deep Cleaning**:
```json
{
  "name": "Customer Name",
  "phone": "+1234567890",
  "type_of_service": "Deep Cleaning",
  "appointment_date_time": "2025-10-15 14:00",
  "business_id": "bus_430967"
}
```

---

## Summary

✅ **Two services**: Deep Cleaning (simple), Standard Cleaning (customizable)  
✅ **Three service items**: bedroom (number), driveway (boolean), cleaner product (select)  
✅ **Flexible date/time**: Accepts human-readable formats  
✅ **Clear pricing**: All prices shown in descriptions  
✅ **Type-safe**: Enum values for services and cleaner products  

**Your Retell integration is ready to go!** 🎉
