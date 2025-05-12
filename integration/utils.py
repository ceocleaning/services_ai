from .models import IntegrationLog

def log_integration_activity(platform, status, request_data, response_data=None, error_message=None):
    """
    Create a log entry for integration activity.
    
    Args:
        platform: The PlatformIntegration instance
        status: String status ('success', 'failed', or 'pending')
        request_data: The data sent to the integration (dict)
        response_data: Optional response data received from the integration (dict or None)
        error_message: Optional error message if the integration failed (str or None)
    
    Returns:
        IntegrationLog: The created log entry
    """
    log_entry = IntegrationLog.objects.create(
        platform=platform,
        status=status,
        request_data=request_data,
        response_data=response_data,
        error_message=error_message
    )
    
    return log_entry 








# Sending Data to External Sources
def create_mapped_payload(booking_data, integration):
    """Create payload based on user-defined field mappings"""
    from .models import DataMapping
    from datetime import date, time, datetime
    import json
    
    # Custom JSON encoder to handle date/time objects
    class CustomJSONEncoder(json.JSONEncoder):
        def default(self, obj):
            if isinstance(obj, (date, time, datetime)):
                return obj.isoformat()
            return super().default(obj)
    
    # Helper function to serialize non-serializable objects
    def serialize_value(value):
        if isinstance(value, (date, time, datetime)):
            return value.isoformat()
        elif isinstance(value, dict):
            return {k: serialize_value(v) for k, v in value.items()}
        elif isinstance(value, list):
            return [serialize_value(item) for item in value]
        return value
    
    mappings = DataMapping.objects.filter(platform=integration)
    payload = {}
    
    # Apply mappings
    for mapping in mappings:
        source_field = mapping.source_field
        source_value = None
        
        # Handle source fields with dot notation (e.g., booking.name)
        if '.' in source_field:
            parts = source_field.split('.')
            current_data = booking_data
            found = True
            
            # Navigate through the nested structure
            for part in parts:
                if isinstance(current_data, dict) and part in current_data:
                    current_data = current_data[part]
                else:
                    found = False
                    break
            
            if found:
                source_value = current_data
        else:
            # Try to get the value directly
            source_value = booking_data.get(source_field)
        
        # Skip if source field doesn't exist
        if source_value is None and not mapping.default_value:
            if mapping.is_required:
                raise ValueError(f"Required field {source_field} not found in booking data")
            continue
            
        # Use default value if source is None
        if source_value is None:
            source_value = mapping.default_value
        
        # Serialize date/time objects
        source_value = serialize_value(source_value)
        
        # Apply type conversion based on field_type
        if mapping.field_type == 'number' and not isinstance(source_value, (int, float)):
            try:
                source_value = float(source_value)
            except (ValueError, TypeError):
                source_value = 0
        elif mapping.field_type == 'boolean' and not isinstance(source_value, bool):
            if isinstance(source_value, str):
                source_value = source_value.lower() in ('true', 'yes', '1', 'on')
            else:
                source_value = bool(source_value)
                
        # Handle nested fields in the output payload
        if mapping.parent_path:
            parts = mapping.parent_path.split('.')
            current = payload
            for part in parts[:-1]:
                if part not in current:
                    current[part] = {}
                current = current[part]
            if parts[-1] not in current:
                current[parts[-1]] = {}
            current[parts[-1]][mapping.target_field] = source_value
        else:
            payload[mapping.target_field] = source_value
    
    return payload



def send_booking_data(booking):
    """Send booking data to integration webhook"""
    try:
        # Get all active integrations for the business
        integrations = PlatformIntegration.objects.filter(
            business=booking.business,
            is_active=True
        )
        
        if not integrations.exists():
            print(f"No active integrations found for business {booking.business.businessName}")
            return

        results = {
            'workflow': {'success': [], 'failed': []},
            'direct_api': {'success': [], 'failed': []}
        }
        
        print(f"Processing {integrations.count()} integrations for business {booking.business.businessName}")
        
        for integration in integrations:
            try:
                integration_type = 'workflow' if integration.platform_type == 'workflow' else 'direct_api'
                print(f"Processing {integration_type} integration: {integration.name}")
                
                if integration.platform_type == 'workflow':
                    # Extract all fields from the booking object
                    booking_dict = {}
                    
                    # Get all fields from the booking object
                    for field in booking._meta.get_fields():
                        if hasattr(field, 'attname') and not field.is_relation:
                            field_name = field.attname
                            value = getattr(booking, field_name, None)
                            
                            # Handle special types
                            if isinstance(value, Decimal):
                                booking_dict[field_name] = float(value)
                            elif isinstance(value, datetime):
                                booking_dict[field_name] = value.isoformat()
                            elif hasattr(value, 'strftime'):
                                # Handle date and time objects
                                booking_dict[field_name] = value.strftime('%Y-%m-%d') if hasattr(value, 'date') else value.strftime('%H:%M:%S')
                            else:
                                booking_dict[field_name] = value
                    
                    # Use the booking dict as the payload
                    payload = booking_dict
                    
                    print(f"Sending data to workflow webhook: {integration.webhook_url}")
                    # Send to webhook URL
                    response = requests.post(
                        integration.webhook_url,
                        json=payload,
                        headers={"Content-Type": "application/json"},
                        timeout=30
                    )

                    # Log successful integration
                    if response.status_code in [200, 201]:
                        log_integration_activity(
                            platform=integration,
                            status='success',
                            request_data=payload,
                            response_data=response.json() if response.text else None
                        )
                    
                    # Log failed integration
                    else:
                        log_integration_activity(
                            platform=integration,
                            status='failed',
                            request_data=payload,
                            error_message=response.text
                        )
                    
                else:  # direct_api
                    # Create payload using field mappings
                    print(f"Creating mapped payload for {integration.name}")
                    
                    # Extract all fields from the booking object
                    booking_dict = {}
                    
                    # Get all fields from the booking object
                    for field in booking._meta.get_fields():
                        if hasattr(field, 'attname') and not field.is_relation:
                            field_name = field.attname
                            value = getattr(booking, field_name, None)
                            
                            # Handle special types
                            if isinstance(value, Decimal):
                                booking_dict[field_name] = float(value)
                            elif isinstance(value, datetime):
                                booking_dict[field_name] = value.isoformat()
                            elif hasattr(value, 'strftime'):
                                # Handle date and time objects
                                booking_dict[field_name] = value.strftime('%Y-%m-%d') if hasattr(value, 'date') else value.strftime('%H:%M:%S')
                            else:
                                booking_dict[field_name] = value
                    
                    payload = create_mapped_payload(booking_dict, integration)
                    
                    # Send to base URL
                    headers = {"Content-Type": "application/json"}
                    
                    # Add authentication if configured
                    if integration.auth_type == 'token' and integration.auth_data.get('token'):
                        headers['Authorization'] = f"Bearer {integration.auth_data['token']}"
                    
                    print(f"Sending data to API endpoint: {integration.base_url}")
                    response = requests.post(
                        integration.base_url,
                        json=payload,
                        headers=headers,
                        timeout=30
                    )
                
                    # Log successful integration
                    if response.status_code in [200, 201]:
                        log_integration_activity(
                            platform=integration,
                            status='success',
                            request_data=payload,
                            response_data=response.json() if response.text else None
                        )
                    
                    # Log failed integration
                    else:
                        log_integration_activity(
                            platform=integration,
                            status='failed',
                            request_data=payload,
                            error_message=response.text
                        )
                    
                
                results[integration_type]['success'].append({
                    'name': integration.name,
                    'response': response.text,
                    'status_code': response.status_code
                })
                
            except Exception as e:
                error_msg = f"Error sending booking data to {integration.name}: {str(e)}"
                print(error_msg)
                
                # Log failed integration
                log_integration_activity(
                    platform=integration,
                    status='failed',
                    request_data=payload if 'payload' in locals() else {},
                    error_message=str(e)
                )
                
                results[integration_type]['failed'].append({
                    'name': integration.name,
                    'error': str(e)
                })
                continue

        # Print summary
        print("\nIntegration Summary:")
        for int_type in ['workflow', 'direct_api']:
            print(f"\n{int_type.upper()} Integrations:")
            print(f"Success: {len(results[int_type]['success'])} integration(s)")
            print(f"Failed: {len(results[int_type]['failed'])} integration(s)")
            
            if results[int_type]['failed']:
                print("\nFailed integrations:")
                for fail in results[int_type]['failed']:
                    print(f"- {fail['name']}: {fail['error']}")

        return results

    except Exception as e:
        print(f"Error in send_booking_data: {str(e)}")
        raise Exception(f"Error in send_booking_data: {str(e)}")
