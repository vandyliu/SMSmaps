import requests

def get_origin(res):
    """returns dict of location with lat and lng fields
    
    Arguments:
        res {dict} -- google maps response
    
    Returns:
        dict -- start location dict with lat and lng fields
    """
    location = res[0]["legs"][0]["start_location"]
    return location

def get_destination(res):
    """returns dict of location with lat and lng fields
    
    Arguments:
        res {dict} -- google maps response
    
    Returns:
        dict -- end location dict with lat and lng fields
    """
    location = res[0]["legs"][0]["end_location"]
    return location

def get_polygon_path(res):
    """gets polygon path from google maps response
    
    Arguments:
        res {dict} -- google maps response
    
    Returns:
        string -- encoded polygon path
    """
    return res[0]["overview_polyline"]["points"]

def get_latlon(location):
    """gets lat and lng from location dict
    
    Arguments:
        location {dict} -- location dict with lat and lng fields
    
    Returns:
        string -- lat and long as string Eg. "43.23234,41.3423"
    """
    return f"{str(location['lat'])},{str(location['lng'])}"