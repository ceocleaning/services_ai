from business.models import Business, BusinessConfiguration
from retell_agent.models import RetellAgent
from retell import Retell
from leads.models import Lead, LeadStatus
from django.utils import timezone
from dotenv import load_dotenv
import os

load_dotenv()

client = Retell(
    api_key=os.getenv("RETELL_API_KEY"),
)



def make_call_to_lead(lead_id):
    try:
        lead = Lead.objects.get(id=lead_id)
        business = lead.business
     
        business_configuration = BusinessConfiguration.objects.get(business=business)
        retell_agent = RetellAgent.objects.get(business=business)

        lead_details = f"Here are the details about the lead:\nName: {lead.name}\nPhone: {lead.phone_number}\nEmail: {lead.email if lead.email else 'Not provided'}\nAddress: {lead.address1 if lead.address1 else 'Not provided'}\nCity: {lead.city if lead.city else 'Not provided'}\nState: {lead.state if lead.state else 'Not provided'}\nZip Code: {lead.zipCode if lead.zipCode else 'Not provided'}\nProposed Start Time: {lead.proposed_start_datetime.strftime('%B %d, %Y at %I:%M %p') if lead.proposed_start_datetime else 'Not provided'}\nNotes: {lead.notes if lead.notes else 'No additional notes'}"

        if business_configuration.voice_enabled:
            call_response = client.call.create_phone_call(
                    from_number=retell_agent.agent_number,
                    to_number=lead.phone_number,
                    override_agent_id=retell_agent.retell_agent_id,
                    retell_llm_dynamic_variables={
                        'name': lead.name,
                        'details': lead_details
                    }
                )
            
            lead.status = LeadStatus.CONTACTED
            lead.last_contacted = timezone.now()
            lead.save()
            
            print("Call Initiated")
            
            return 0
        
        return -1
    
    except Exception as e:
        print(f"Error making call: {e}")
        return -1

 
    