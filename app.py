import json
import shutil

from dotenv import load_dotenv
from flask import Flask, request, session

from maps import client
from sms import sms_reply

load_dotenv()

app = Flask(__name__)

@app.route("/")
def hello():
    return "hello world"

@app.route("/directions/raw/")
def directions_raw():
    mode = request.args.get('mode')
    language = request.args.get('language')
    arrival_time = request.args.get('arrival_time')
    departure_time = request.args.get('departure_time')
    origin = request.args.get('origin')
    destination = request.args.get('destination')

    res = client.directions(origin,
                            destination,
                            mode,
                            language,
                            arrival_time,
                            departure_time)

    return res

@app.route("/directions/")
def directions():
    mode = request.args.get('mode')
    language = request.args.get('language')
    arrival_time = request.args.get('arrival_time')
    departure_time = request.args.get('departure_time')
    origin = request.args.get('origin')
    destination = request.args.get('destination')

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

    callers = {
        "+7783788024": "Friend",
        "+6043524722": "Friend",
        "+7788148834": "Friend",
    }

    #Get number
    from_number = request.values.get('From')
    to_number = request.values.get('To')

    if from_number in callers:
        name = callers[from_number]
    else:
        name = "Friend"

    return sms_reply(name, to_number, counter)

if __name__ == "__main__":
    app.run(debug=True)


SECRET_KEY = 'a secret key'
app.config.from_object(__name__)


    