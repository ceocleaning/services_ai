def send_booking_data_to_integration(booking_data, integration):
    """Send booking data to a specific integration"""
    try:
        results = {
            'success': [],
            'failed': []
        }

        if integration.platform_type == 'workflow':
            # Process booking data to ensure it's in the right format
            processed_data = {}
            
            # Handle datetime fields if they exist
            cleaning_date_field = next((f for f in ['cleaningDateTime', 'cleaningDate', 'appointmentDate', 'booking_date'] 
                                     if f in booking_data), None)
            
            if cleaning_date_field and isinstance(booking_data[cleaning_date_field], datetime):
                cleaning_date = booking_data[cleaning_date_field].date().isoformat()
                cleaning_time = booking_data[cleaning_date_field].time().strftime("%H:%M:%S")
                # Calculate end time (1 hour after start time by default)
                end_time = (booking_data[cleaning_date_field] + timedelta(minutes=60)).time().strftime("%H:%M:%S")
                
                processed_data["cleaningDate"] = cleaning_date
                processed_data["startTime"] = cleaning_time
                processed_data["endTime"] = end_time
            
            # Copy all other fields from booking_data to processed_data
            for key, value in booking_data.items():
                # Skip the already processed datetime field
                if key == cleaning_date_field:
                    continue
                    
                # Handle special types
                if isinstance(value, Decimal):
                    processed_data[key] = float(value)
                elif isinstance(value, datetime):
                    processed_data[key] = value.isoformat()
                else:
                    processed_data[key] = value
            
            # Use the processed data as the payload
            payload = processed_data
            
            try:
                response = requests.post(
                    integration.webhook_url,
                    json=payload,
                    headers={"Content-Type": "application/json"},
                    timeout=30
                )

                # Safely parse JSON response
                response_data = None
                if response.text:
                    try:
                        response_data = response.json()
                    except json.JSONDecodeError:
                        # If response is not valid JSON, use text as is
                        response_data = {"raw_response": response.text}

                if response.status_code in [200, 201]:
                    log_integration_activity(
                        platform=integration,
                        status='success',
                        request_data=payload,
                        response_data=response_data
                    )
                else:
                    log_integration_activity(
                        platform=integration,
                        status='failed',
                        request_data=payload,
                        error_message=response.text
                    )
                
                results['success'].append({
                    'name': integration.name,
                    'response': response.text,
                    'status_code': response.status_code
                })
                
            except requests.RequestException as req_err:
                error_msg = f"Request error: {str(req_err)}"
                log_integration_activity(
                    platform=integration,
                    status='failed',
                    request_data=payload,
                    error_message=error_msg
                )
                
                results['failed'].append({
                    'name': integration.name,
                    'error': error_msg
                })
            
        else:  # direct_api
            # Process booking data to ensure it's in the right format for mapping
            processed_data = {}
            
            for key, value in booking_data.items():
                # Handle special types
                if isinstance(value, Decimal):
                    processed_data[key] = float(value)
                elif isinstance(value, datetime):
                    processed_data[key] = value.isoformat()
                else:
                    processed_data[key] = value
                    
            # Use the create_mapped_payload function from utils.py
            from .utils import create_mapped_payload
            payload = create_mapped_payload(processed_data, integration)
            print("Payload:", payload)
            
            headers = {"Content-Type": "application/json"}
            if integration.auth_type == 'token' and integration.auth_data.get('token'):
                headers['Authorization'] = f"Bearer {integration.auth_data['token']}"
            
            try:
                response = requests.post(
                    integration.base_url,
                    json=payload,
                    headers=headers,
                    timeout=30
                )

                # Safely parse JSON response
                response_data = None
                if response.text:
                    try:
                        response_data = response.json()
                    except json.JSONDecodeError:
                        # If response is not valid JSON, use text as is
                        response_data = {"raw_response": response.text}

                if response.status_code in [200, 201]:
                    log_integration_activity(
                        platform=integration,
                        status='success',
                        request_data=payload,
                        response_data=response_data
                    )
                else:
                    log_integration_activity(
                        platform=integration,
                        status='failed',
                        request_data=payload,
                        error_message=response.text
                    )
                
                results['success'].append({
                    'name': integration.name,
                    'response': response.text,
                    'status_code': response.status_code
                })
                
            except requests.RequestException as req_err:
                error_msg = f"Request error: {str(req_err)}"
                log_integration_activity(
                    platform=integration,
                    status='failed',
                    request_data=payload,
                    error_message=error_msg
                )
                
                results['failed'].append({
                    'name': integration.name,
                    'error': error_msg
                })
        
        return results

    except Exception as e:
        # Log failed integration
        log_integration_activity(
            platform=integration,
            status='failed',
            request_data=payload if 'payload' in locals() else {},
            error_message=str(e)
        )
        
        return {
            'success': [],
            'failed': [{
                'name': integration.name,
                'error': str(e)
            }]
        }
