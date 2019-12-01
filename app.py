import json
import shutil
import googlemaps

from dotenv import load_dotenv
from flask import Flask, request, session

from maps import client
from sms import sms_reply, valid_text, send_image

load_dotenv()

app = Flask(__name__)

@app.route("/")
def hello():
    return "hello world"

@app.route("/directions/")
def directions(origin, destination, mode="transit", language=None, arrival_time=None, departure_time=None):
    try:
        res = client.directions(origin,
                            destination,
                            mode,
                            language,
                            arrival_time,
                            departure_time)
    except googlemaps.exceptions.ApiError:
        return {}
    return res
def parse_directions(res):
    try:
        parsed_data = client.parse(res)
    except KeyError:
        return {}
    if parsed_data.get("departure_time") is None:
        return "NO_PATH"

    directions = (
        f'Departure: {parsed_data.get("departure_time", "n/a")}\n'
        f'Arrival: {parsed_data.get("arrival_time", "n/a")}\n'
        f'Total Trip Time: {parsed_data.get("duration", "n/a")}\n'
        f'Total Trip Distance: {parsed_data.get("distance", "n/a")}\n'
        f'Start Address: {parsed_data.get("start_address", "n/a")}\n'
        f'Destination Address: {parsed_data.get("end_address", "n/a")}\n\n'
    )

    directions += client.get_instruction_string(parsed_data.get("steps", {}))

    return directions

@app.route("/sms", methods=['GET', 'POST'])
def reply():
    counter = session.get('counter', 0)
    counter += 1
    session['counter'] = counter
    text_message = request.values.get('Body')

    output_string = (
        '\n'
        'Hey, we can help you find a transit path to where you need to go.\n'
        'DM us a text with your current location and your destination like so:\n'
        '<your location> ; <your destination>'
    )

    if valid_text(text_message, counter):
        locations = text_message.split(";")
        origin = locations[0]
        dest = locations[1]
        print(origin)
        print(dest)
        res = directions(origin, dest)
        res_l= res[0]
        url = None
        if not res_l:
            url = client.map_image(res_l)
        print(url)
        if url:
            send_image(url)
        directions_string = parse_directions(res)
        if not directions_string:
            output_string = 'Could not determine location(s). Please try again.'
        elif directions_string == "NO_PATH":
            output_string = 'Could not find a route between the two locations. Please try again.'
        else:
            output_string = directions_string
            
    return sms_reply(output_string)

if __name__ == "__main__":
    app.run(debug=True)


SECRET_KEY = 'a secret key'
app.config.from_object(__name__)
    