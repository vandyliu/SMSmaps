from flask import Flask, request, session
from dotenv import load_dotenv
import json

from maps import client

load_dotenv()

from sms import sms_reply
app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"

@app.route("/instructions/")
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

    return client.instructions(res)
@app.route("/sms", methods=['GET', 'POST'])
def reply():
    # Increment the counter
    # counter = session.get('counter', 0)
    # counter += 1
    # session['counter'] = counter

    # callers = {
    #     "+7783788024": "Friend",
    #     "+6043524722": "Friend",
    #     "+7788148834": "Friend",
    # }

    #Get number
    from_number = request.values.get('From')
    to_number = request.values.get('To')

    # if from_number in callers:
    #     name = callers[from_number]
    # else:
    #     name = "Friend"

    return sms_reply('name', to_number, '2')

if __name__ == "__main__":
    app.run(debug=True)


SECRET_KEY = 'a secret key'
app.config.from_object(__name__)


    