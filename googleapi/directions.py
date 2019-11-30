import googlemaps
from datetime import datetime

import json

gmaps = googlemaps.Client(key='AIzaSyB4Hh5V4zRygXTFAipMXiWRBz8_rmqNgYg')

# Geocoding an address
geocode_result = gmaps.geocode('1600 Amphitheatre Parkway, Mountain View, CA')

def directions(origin, destination, mode, language, arrival_time, departure_time):
    # Request directions via public transit
    now = datetime.now()
    res = gmaps.directions(origin,
                           destination,
                           mode=mode,
                           departure_time=now,
                           arrival_time=arrival_time,
                           language=language)

    #return(res[0]["legs"][0])

    if not res:
        # empty
        return "Not Found"
    else:
        instructions=[]

        for step in res[0]["legs"][0]["steps"]:
            instructions.append(step["html_instructions"])
            if "steps" in step:
                for step2 in step["steps"]:
                    instructions.append(step2["html_instructions"])

        return '\n'.join(instructions)
