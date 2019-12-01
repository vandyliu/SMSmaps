import os
import googlemaps
from datetime import datetime
import json
import requests

from maps import helpers as mh

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

def map_image(res):
    """Gets URL of a google maps image that shows the route
    
    Arguments:
        res {dict} -- google maps response
    
    Returns:
        string -- URL of maps image
    """
    # constants
    MAP_URL = "https://maps.googleapis.com/maps/api/staticmap"
    SIZE = "400x400"

    polygon_path = mh.get_polygon_path(res)
    origin = mh.get_latlon(mh.get_origin(res))
    destination = mh.get_latlon(mh.get_destination(res))
    params = {
        "size": SIZE,
        "path": f"enc:{polygon_path}",
        "markers": [f"color:red|label:X|{destination}", f"size:small|color:blue|{origin}"],
        "key": key
    }
    img_resp = requests.get(url=MAP_URL, params=params)
    return img_resp.url