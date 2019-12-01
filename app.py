import json
import shutil
import googlemaps

from dotenv import load_dotenv
from flask import Flask, request, session

from maps import client
from sms import sms_reply, valid_text

load_dotenv()

app = Flask(__name__)

@app.route("/")
def hello():
    return "hello world"

@app.route("/directions/")
def directions_raw():
    mode = request.args.get('mode')
    language = request.args.get('language')
    arrival_time = request.args.get('arrival_time')
    departure_time = request.args.get('departure_time')
    origin = request.args.get('origin')
    destination = request.args.get('destination')

    try:
        res = directions(origin,
                        destination,
                        mode,
                        language,
                        arrival_time,
                        departure_time)
    except googlemaps.exceptions.ApiError:
        return "ERROR"

    return res

def directions(origin, destination, mode="transit", language=None, arrival_time=None, departure_time=None):
    res = client.directions(origin,
                            destination,
                            mode,
                            language,
                            arrival_time,
                            departure_time)
    parsed_data = client.parse(res)
    directions = (
        f'Departure: {parsed_data["departure_time"]}\n'
        f'Arrival: {parsed_data["arrival_time"]}\n'
        f'Total Trip Time: {parsed_data["duration"]}\n'
        f'Total Trip Distance: {parsed_data["distance"]}\n'
        f'Start Address: {parsed_data["start_address"]}\n'
        f'Destination Address: {parsed_data["end_address"]}\n\n'
    )

    directions += client.get_instruction_string(parsed_data["steps"])

    return directions

@app.route("/sms", methods=['GET', 'POST'])
def reply():
    counter = session.get('counter', 0)
    counter += 1
    session['counter'] = counter
    text_message = request.values.get('Body')

    output_string = 'Hey, we can help you find a transit path to where you need to go.\n \
            DM us a text with your current location and where your destination like so:\n \
            <your location> ; <your destination>.'

    if valid_text(text_message, counter):
        locations = text_message.split(";")
        origin = locations[0]
        dest = locations[1]
        directions_string = directions(origin, dest)
        if directions_string != "ERROR":
            output_string = directions_string
            
    return sms_reply(output_string)

if __name__ == "__main__":
    app.run(debug=True)


SECRET_KEY = 'a secret key'
app.config.from_object(__name__)


    