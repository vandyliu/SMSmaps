from flask import Flask
from dotenv import load_dotenv

from maps import directions

load_dotenv()
app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"