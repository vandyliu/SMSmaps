import os
import googlemaps
from datetime import datetime
import json

key = os.getenv("GOOGLE_API_KEY")
gmaps = googlemaps.Client(key=key)

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
        return res

def instructions(res):
    instructions=[]

    for step in res[0]["legs"][0]["steps"]:
        instructions.append(step["html_instructions"])
        if "steps" in step:
            for step2 in step["steps"]:
                instructions.append(step2["html_instructions"])

    return '\n'.join(instructions)