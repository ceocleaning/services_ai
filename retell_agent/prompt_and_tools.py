from business.models import Business, ServiceOffering, ServiceItem



def get_retell_prompt(business):
    services = ""
    service_offerings = ServiceOffering.objects.filter(business=business)
    for service in service_offerings:
        services += f"- {service.name} - ${service.price}, \n"
    

    service_items = ServiceItem.objects.filter(business=business)
    service_items = ""
    for service_item in service_items:
        service_items += f"- {service_item.name} - ${service_item.price_value if not service_item.price_type == 'free' else "No Charges"}, - {service_item.description} - Optional: {service_item.is_optional} \n"
    
    

    business_address = f"{business.address}, {business.city}, {business.state}, {business.zip_code}"

    default_prompt = f"""
    ###Persona of AI Voice Agent
    Your name is Sarah, Office Assistant for {business.name} from {business_address}. Your role is to book appointment and answer client questions about {business.name}'s services.

    ##Skills:
    - Professional and friendly communication
    - Efficient data collection and processing
    - Knowledgeable about {business.name}'s services and policies
    - Ability to check real-time calendar availability
    - Proficient in making service recommendations based on client needs

    ##Role: To assist clients in scheduling {business.name}'s services seamlessly, ensuring all necessary information is collected and providing recommendations to enhance their experience.

    ##Objective: To facilitate a smooth and efficient booking process, ensuring client satisfaction and optimal scheduling for {business.name}.

    ###Rules to Follow
    Always maintain a courteous and professional tone.
    Ensure clarity in communication; confirm details when necessary.
    Adhere to the data collection sequence outlined in the steps.
    Provide service recommendations based on client inputs.
    Verify calendar availability before confirming appointments.
    Offer alternative time slots if the preferred time is unavailable.
    Thank the client sincerely after booking.


    ##Base Services
    {services}

    ##Service Items
    {service_items}



    ##Business TimeZone
    America/Chicago

    ##Business ID
    {business.id}

    ###Script AI has to Follow
    ##Greeting and Introduction:

    ##Initial Step
    - run {{current_time}} and convert it business timezone in the beginning of the call

    "Good [morning/afternoon/evening]! Thank you for contacting {business.name} in {business_address}. My name is Sarah,. How are you doing today?"
    Check for User's Intent:

    If the user expresses interest in booking a service:
    "Great! To proceed with your booking, may I have your full name, email address, and phone number?"
    Collect Client Information:

    Record the client's full name.
    Record the client's email address.
    Record the client's phone number.


    ##Determine Service Type:
    Ask Which Service client is interested, We offer several services:
    {services}
    Which service would you prefer?"


    ##Ask for Service Items
    - After getting service type ask the user to select service items one by one

    ##Ask for Additional Requests
    - Ask user if they additional requests or notes that we should know

    ##Collect Service Location:
    "Could you please provide the full address where the cleaning service is needed?"
    Record the client's address.

    ##Schedule Appointment:
    "Thank you. Please select your preferred date and time for the service. Our available time slots are from 9:00 AM to 5:00 PM, Central Standard Time (America/Chicago)."
    (wait for response)
    run {{check_availability}}

    If time is unavailable:
    "I'm sorry, but the selected time slot is not available. Here are three alternative options based on our current availability:
    [Alternative Date and Time 1]
    [Alternative Date and Time 2]
    [Alternative Date and Time 3] Please choose one of these, or let me know another time that works for you."

    ##After Collecting Preferred Date and Time:
    {{bookAppointment}} 

    ##Booking Confirmation:
    Upon successful booking, inform the client:
    "Your appointment has been successfully booked for [Confirmed Date and Time]. You will receive a confirmation email shortly."


    ##Closing:

    "Thank you, [Client's Name], for choosing {business.name}. We look forward to providing you with exceptional service. Have a wonderful day!"

    {{end_call}}
    """

    return default_prompt

def get_retell_tools(business):
    custom_tools = [
            {
                "type": "end_call",
                "name": "end_call",
                "description": "End the call with user."
            },
            {
                "type": "custom",
                "name": "check_availability",
                "description": "Check TimeSlot Availability of User Selected DateTime",
                "url": f"https://servicesai.com/api/availability/{business.id}/",
                "execution_message_description": "Checking TimeSlot Availability",
                "timeout_ms": 10000,
                "speak_during_execution": True,
                "speak_after_execution": True,
                "parameters": {
                    "type": "object",
                    "properties": {
                        "cleaningDateTime": {
                            "type": "string",
                            "description": "The ISO 8601 timestamp user selected date time (e.g., '2025-02-26T14:00:00+00:00')."
                        }
                    },
                    "required": ["cleaningDateTime"]
                }
            },
            {
                "type": "custom",
                "name": "send_commercial_link",
                "description": "This function will send email to client if client selects commercial cleaning service",
                "url": "https://servicesai.com/api/send-commercial-form-link/",
                "execution_message_description": "Sending Commercial Cleaning Form Link",
                "timeout_ms": 10000,
                "speak_during_execution": True,
                "speak_after_execution": True,
                "parameters": {
                    "type": "object",
                    "properties": {
                        "name": {
                            "type": "string",
                            "description": "Full Name of the Client"
                        },
                        "business_id": {
                            "type": "string",
                            "description": "Business ID"
                        },
                        "email": {
                            "type": "string",
                            "description": "Email of the Client"
                        }
                    },
                    "required": ["email", "name", "business_id"]
                }
            },
            {
                "type": "custom",
                "name": "bookAppointment",
                "description": "This will be used to book an appointment",
                "url": "https://servicesai.com/api/create-booking/",
                "execution_message_description": "Booking Appointment",
                "timeout_ms": 10000,
                "speak_during_execution": True,
                "speak_after_execution": True,
                "parameters": {
                    "type": "object",
                    "properties": get_book_appointment_tool_properties(business),
                    "required": [
                        "full_name", "email", "phone_number", "address", "city", "state", 
                        "zip_code", "service_type", "appointment_date_time", 
                        "business_id"
                    ]
                }
            }
        ]
    
    return custom_tools




def get_book_appointment_tool_properties(business):
    service_items = ServiceItem.objects.filter(business=business)

    properties = {
                "city": {
                    "type": "string",
                    "description": "The city where the service is booked."
                },
                "appointment_date_time": {
                    "type": "string",
                    "description": "The date and time when the service is scheduled."
                },
                "zip_code": {
                    "type": "string",
                    "description": "The postal code of the booking location."
                },
 
                "state": {
                    "type": "string",
                    "description": "The state or province of the booking location."
                },
                "full_name": {
                    "type": "string",
                    "description": "The full name of the person making the booking."
                },
                "email": {
                    "type": "string",
                    "description": "The email address of the person making the booking."
                },
   
                "address": {
                    "type": "string",
                    "description": "Primary address for the booking."
                },
                "service_type": {
                    "type": "string",
                    "description": "The type of base service selected."
                },
                "phone_number": {
                    "type": "string",
                    "description": "The phone number of the person making the booking."
                },
                "business_id": {
                    "type": "string",
                    "description": "Business ID"
                }
            }

    for service_item in service_items:
        properties[service_item.identifier] = {
            "type": "string",
            "description": f"Response for the {service_item.name} service"
        }

    return properties

