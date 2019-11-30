import os
import googlemaps
from datetime import datetime
import json
import requests

from maps import helpers as mh

import re

key = os.getenv("GOOGLE_API_KEY")
gmaps = googlemaps.Client(key=key)

def directions(origin, destination, mode, language, arrival_time, departure_time):
    """returns raw direction object from google maps directions api
    
    Arguments:
        origin {string} -- Starting Location eg. Starbucks near UBC Bookstore
        destination {string} -- Ending Location
        mode {string} -- method of travel, defaults to "driving"
                         "transit" "walking" "driving" or "bicycling"
        language {string} -- language to return in, defaults to "EN". eg. "zh-CN", "fr-CA"
                             see https://developers.google.com/maps/faq#languagesupport
        arrival_time {integer} -- Specifies the desired time of arrival.
                                  Seconds since midnight, January 1, 1970 UTC
        departure_time {integer} -- Specifies the desired time of departure.
                                    Seconds since midnight, January 1, 1970 UTC
    
    Returns:
        [dict] -- [raw directions object]
    """    
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
        return res[0]

def parse(res):
    """converts raw direction dict from google maps api to readible format
    
    Arguments:
        res {dict} -- raw direction dict from google maps api
    
    Returns:
        [dict] -- readible directions format
    """    
    instructions = []
    lat = res["legs"][0]["end_location"]["lat"]
    lng = res["legs"][0]["end_location"]["lng"]

    for step in res["legs"][0]["steps"]:
        instruction = re.sub('<[^<]+?>', '', step["html_instructions"])
        instructions.append(instruction)
        if "steps" in step:
            for step2 in step["steps"]:
                instruction = re.sub('<[^<]+?>', '', step2["html_instructions"])
                instructions.append(instruction)

    return {
        "instructions": instructions,
        "travel_length": res["legs"][0]["duration"]["text"],
        "arrival_time": res["legs"][0].get("arrival_time", {}).get("text", None),
        "departure_time": res["legs"][0].get("departure_time", {}).get("text", None),
        "end_address": res["legs"][0]["end_address"],
        "start_address": res["legs"][0]["start_address"],
        "distance": res["legs"][0]["distance"]["text"],
        "duration": res["legs"][0]["duration"]["text"],
        "destination_url": f'http://www.google.com/maps/place/{lat},{lng}'
    }

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
