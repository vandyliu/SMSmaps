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


def valid_text(text_message, counter):
    if ";" not in text_message:
        return None
    locations = text_message.split(";")
    if len(locations) != 2:
        return None
    return True

def sms_reply(string):
    resp = MessagingResponse()
    message = Message()
    message.body(string)
    resp.append(message)
    return str(resp)

def send_image(dest_num, url):
    print("sendingimage")
    # resp = MessagingResponse()
    # message = Message()
    # message.media(url)
    # resp.append(message)
    print(main_phone_number)
    print(dest_num)
    client.messages.create(from_=main_phone_number,to=dest_num, media_url=url)
    return
