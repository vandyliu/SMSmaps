import os
import googlemaps
from datetime import datetime

key = os.getenv("GOOGLE_API_KEY")
gmaps = googlemaps.Client(key=key)