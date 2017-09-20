from math import sin, cos, sqrt, atan2, radians, pi # math stuff 
from geopy.geocoders import Nominatim #get coordinates of locations 

def printinfo (magnitude,time,day,location,depth):
    return ('There was an earthquake of magnitude %s at %s (UTC) %s in %s.\
    Depth was %s' % ( magnitude,time, day, location, depth))

    #get lat and long of a place                                                                                                                                                         
def get_location_lat_long (locate):
    geolocator = Nominatim()
    location = geolocator.geocode(locate)
    return ((location.latitude, location.longitude))


 #calculate distance between places taken form
 #https://stackoverflow.com/questions/19412462/getting-distance-between-two-points-based-on-latitude-longitude                                                                                                                                                  
def calculate_distance (lat_df,lat,lon_df, lon):
    r_earth = 6373.0
    lat1 = radians(lat_df)
    lat2 = radians(lat)
    long1 = radians(lon_df)
    long2 = radians(lon)
    dlong = long2 - long1
    dlat = lat2 - lat1
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlong / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    distance = r_earth * c
    return distance

def calculate_area (rad):
  	return rad*rad*pi

def read_key(f):
    a = []
    with open(f,'r') as file:
        for line in file:
            for word in line.split(","):
                a.append(word)
            username = a[0]
            api_key = a[1]
            mapbox_token = a[2]
    return a
        
