import os
from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client

account_sid = os.getenv("TWILIO_ACCOUNT_SID")
auth_token = os.getenv("TWILIO_AUTH_TOKEN")
main_phone_number = '+17786545908'
sms_url = "https://sms-maps.azurewebsites.net/sms"

client = Client(account_sid, auth_token)
incoming_phone_numbers = client.incoming_phone_numbers.list(phone_number=main_phone_number, limit=5)
main_phone_number_resource = incoming_phone_numbers[0]

client.incoming_phone_numbers(main_phone_number_resource.sid).update(sms_url=sms_url)

def sms_reply():
    """When receiving an SMS, sends return message to caller
    Returns:
        str -- return message
    """    
    resp = MessagingResponse()
    # Add a message
    resp.message("return message here")
    return str(resp)

