# Retell Tools - Updated Book Appointment Schema

## Overview
The `book_appointment` tool now supports **dynamic service items** with flexible field types. Instead of hardcoding specific fields like `bedrooms`, `bathroom`, etc., you can now pass any service item using its `identifier`.

---

## Updated Schema

### **Required Fields**
```json
{
  "name": "string",              // Customer name
  "phone": "string",             // Customer phone
  "type_of_service": "string",   // Service name
  "appointment_date_time": "string",  // Date and time
  "business_id": "string"        // Business ID
}
```

### **Optional Fields**
- `email`: Customer email address
- **Any service item identifier**: Dynamic based on your business configuration

---

## Service Items - How They Work

### **Key Concept**
Each service item has an `identifier` (e.g., `number_of_bedrooms`, `has_pets`, `cleaner_product`). You pass the identifier as a key in the JSON with the appropriate value.

### **Field Types**

#### 1. **Number Fields**
Used for quantities (bedrooms, bathrooms, square feet, etc.)

```json
{
  "number_of_bedrooms": 3,
  "number_of_bathrooms": 2,
  "square_feet": 1500
}
```

**How it's processed**:
- Value is used as quantity for pricing
- Stored in `number_value` field in database
- Example: 3 bedrooms × $10 = $30

---

#### 2. **Boolean Fields**
Used for yes/no questions (has pets, needs driveway cleaning, etc.)

```json
{
  "has_pets": true,
  "driveway_cleaning": false
}
```

**Accepted values**:
- `true`, `false` (boolean)
- `"yes"`, `"no"` (string)
- `1`, `0` (number)
- `"y"`, `"n"` (string)

**How it's processed**:
- Converted to "yes" or "no"
- Stored in `boolean_value` field
- Pricing based on option_pricing configuration

---

#### 3. **Select Fields**
Used for dropdown options (cleaner product, property size, etc.)

```json
{
  "cleaner_product": "best cleaner",
  "property_size": "large"
}
```

**How it's processed**:
- Value must match one of the configured options
- Stored in `select_value` field
- Pricing based on selected option

---

#### 4. **Text Fields**
Used for text input (address, special instructions, etc.)

```json
{
  "service_address": "123 Main St, Apt 4B",
  "special_instructions": "Please call before arriving"
}
```

**How it's processed**:
- Stored as-is in `text_value` field
- Can have fixed pricing or be free

---

#### 5. **Textarea Fields**
Used for longer text input (detailed notes, requirements, etc.)

```json
{
  "additional_notes": "Large property with multiple levels. Please bring extra equipment."
}
```

**How it's processed**:
- Stored as-is in `textarea_value` field
- Can have fixed pricing or be free

---

## Example Requests

### **Example 1: Standard Cleaning with Number Fields**

```json
{
  "name": "John Doe",
  "email": "john@example.com",
  "phone": "+1234567890",
  "type_of_service": "Standard Cleaning",
  "number_of_bedrooms": 3,
  "number_of_bathrooms": 2,
  "appointment_date_time": "2025-10-15 14:00",
  "business_id": "bus_123456"
}
```

**Result**: Books Standard Cleaning with 3 bedrooms and 2 bathrooms

---

### **Example 2: Cleaning with Boolean and Select Fields**

```json
{
  "name": "Jane Smith",
  "email": "jane@example.com",
  "phone": "+1987654321",
  "type_of_service": "Deep Cleaning",
  "number_of_bedrooms": 2,
  "has_pets": true,
  "driveway_cleaning": false,
  "cleaner_product": "best cleaner",
  "appointment_date_time": "tomorrow at 2pm",
  "business_id": "bus_123456"
}
```

**Result**: Books Deep Cleaning with 2 bedrooms, pets, no driveway, best cleaner

---

### **Example 3: Service with Text Fields**

```json
{
  "name": "Bob Johnson",
  "phone": "+1555123456",
  "type_of_service": "Lawn Care",
  "service_address": "456 Oak Avenue",
  "square_feet": 500,
  "special_instructions": "Please avoid the flower bed on the left side",
  "appointment_date_time": "2025-10-20 09:00",
  "business_id": "bus_123456"
}
```

**Result**: Books Lawn Care with address and special instructions

---

### **Example 4: Mixed Field Types**

```json
{
  "name": "Alice Williams",
  "email": "alice@example.com",
  "phone": "+1444555666",
  "type_of_service": "Home Repair",
  "service_type": "electrical",
  "number_of_rooms": 2,
  "emergency_service": false,
  "service_address": "789 Pine Street, Unit 12",
  "problem_description": "Two outlets in bedroom not working. Possible circuit breaker issue.",
  "appointment_date_time": "2025-10-18 15:30",
  "business_id": "bus_123456"
}
```

**Result**: Books Home Repair with all customization details

---

## How the API Processes Service Items

### **Step 1: Identify Service Items**
```python
# API queries all active service items for the business
service_items = ServiceItem.objects.filter(
    business=business,
    is_active=True
)
```

### **Step 2: Match Request Data**
```python
# For each service item, check if its identifier is in the request
for item in service_items:
    if item.identifier in request_data:
        value = request_data[item.identifier]
        # Process based on field_type
```

### **Step 3: Format Based on Field Type**
```python
if item.field_type == 'number':
    service_items.append({
        'identifier': item.identifier,
        'value': str(value),
        'quantity': 1
    })
elif item.field_type == 'boolean':
    bool_value = 'yes' if value in [True, 'yes', '1', 'y'] else 'no'
    service_items.append({
        'identifier': item.identifier,
        'value': bool_value,
        'quantity': 1
    })
# ... and so on for other types
```

### **Step 4: Pass to BookAppointmentTool**
```python
booking_tool.run(
    date=date_str,
    time=time_str,
    service_name=service_name,
    customer_name=name,
    customer_phone=phone,
    customer_email=email,
    service_items=service_items  # ← Formatted service items
)
```

---

## Benefits of Dynamic Schema

### ✅ **Flexibility**
- No need to update schema when adding new service items
- Works with any business configuration
- Supports unlimited service items

### ✅ **Type Safety**
- API automatically handles field type conversion
- Validates values based on field type
- Prevents type mismatches

### ✅ **Maintainability**
- Single schema works for all businesses
- No hardcoded field names
- Easy to extend

### ✅ **Consistency**
- Same format as SMS agent
- Same format as web booking
- Unified data structure

---

## Migration from Old Schema

### **Old Schema** (Hardcoded):
```json
{
  "bedrooms": 3,
  "bathroom": 2,
  "square_feet": 1500,
  "city": "New York"
}
```

### **New Schema** (Dynamic):
```json
{
  "number_of_bedrooms": 3,
  "number_of_bathrooms": 2,
  "square_feet": 1500,
  "service_address": "123 Main St, New York"
}
```

**Key Differences**:
- Use full identifier names (e.g., `number_of_bedrooms` instead of `bedrooms`)
- Use `service_address` instead of `city` for location
- Can include any service item configured in your system

---

## Finding Service Item Identifiers

### **Method 1: Check System Prompt**
The system prompt includes all service items with their identifiers:
```
• Bedroom Cleaning (identifier: number_of_bedrooms) - $10 per unit
• Driveway Cleaning (identifier: driveway_cleaning)
```

### **Method 2: Query the Database**
```python
from business.models import ServiceItem

items = ServiceItem.objects.filter(
    business_id='bus_123456',
    is_active=True
)

for item in items:
    print(f"{item.name}: {item.identifier}")
```

### **Method 3: Check Admin Panel**
Each service item shows its identifier in the admin interface.

---

## Error Handling

### **Unknown Service Item**
If you pass an identifier that doesn't exist:
```json
{
  "unknown_field": "some value"
}
```
**Result**: Ignored silently (no error, just not processed)

---

### **Invalid Field Type Value**
If you pass wrong type for a field:
```json
{
  "number_of_bedrooms": "abc"  // Should be number
}
```
**Result**: May cause error or be converted to 0

---

### **Missing Required Fields**
If you don't include required fields:
```json
{
  "name": "John Doe"
  // Missing phone, type_of_service, etc.
}
```
**Result**: API returns 400 error with message about missing fields

---

## Best Practices

### ✅ **DO**:
- Use exact identifier names from your service items
- Pass appropriate data types (number for numbers, boolean for yes/no)
- Include all required fields
- Use human-readable date/time formats

### ❌ **DON'T**:
- Don't use shortened names (use `number_of_bedrooms`, not `bedrooms`)
- Don't pass service items that don't exist in your system
- Don't mix up field types (e.g., passing string for number field)
- Don't forget required fields

---

## Testing

### **Test with cURL**:
```bash
curl -X POST http://localhost:8000/ai-agent/api/book-appointment/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test User",
    "phone": "555-1234",
    "type_of_service": "Standard Cleaning",
    "number_of_bedrooms": 2,
    "has_pets": true,
    "cleaner_product": "best cleaner",
    "appointment_date_time": "2025-10-15 14:00",
    "business_id": "bus_123456"
  }'
```

### **Expected Response**:
```json
{
  "success": true,
  "booking_id": "book_309029",
  "message": "BOOKING_CONFIRMED\nBooking ID: book_309029\n..."
}
```

---

## Conclusion

The updated schema provides **maximum flexibility** while maintaining **type safety** and **consistency** across all booking channels (API, SMS, Web). 

**Key Takeaway**: Use service item `identifiers` as keys, and the API handles the rest automatically! 🎉
