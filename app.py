from flask import Flask, request
from dotenv import load_dotenv
import json

import googleapi.directions as googleapi
from maps import directions

load_dotenv()

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"

@app.route("/directions/")
def directions():
    mode = request.args.get('mode')
    language = request.args.get('language')
    arrival_time = request.args.get('arrival_time')
    departure_time = request.args.get('departure_time')
    origin = request.args.get('origin')
    destination = request.args.get('destination')

    return googleapi.directions(origin,
                                destination,
                                mode,
                                language,
                                arrival_time,
                                departure_time)