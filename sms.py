import os
from twilio.base.exceptions import TwilioRestException
from twilio.twiml.messaging_response import MessagingResponse, Body, Media, Message
from twilio.rest import Client

account_sid = os.getenv("TWILIO_ACCOUNT_SID")
auth_token = os.getenv("TWILIO_AUTH_TOKEN")
main_phone_number = '+17786545908'
sms_url = "https://sms-maps.azurewebsites.net/sms"

client = Client(account_sid, auth_token)

incoming_phone_numbers = client.incoming_phone_numbers.list(phone_number=main_phone_number, limit=5)
main_phone_number_resource = incoming_phone_numbers[0]

# client.incoming_phone_numbers(main_phone_number_resource.sid).update(sms_url=sms_url)


assistant = client.autopilot.assistants.create()


def sms_reply(name, to_number, counter):
    """When receiving an SMS, returns image and number of time this number has recently called (within 4 hours)
    Returns:
        str -- xml representation of return message
    """    
    resp = MessagingResponse()
    message = Message()

    message.body('{} has messaged {} {} times.'.format(name, to_number, counter))
    message.media('https://demo.twilio.com/owl.png')

    resp.append(message)
    return str(resp)
