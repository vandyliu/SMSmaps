import json
import shutil

from dotenv import load_dotenv
from flask import Flask, request

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

    return client.parse(res)

@app.route("/sms", methods=['GET', 'POST'])
def reply():
    return sms_reply()

if __name__ == "__main__":
    app.run(debug=True)
