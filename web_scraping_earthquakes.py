import requests #make a get request to a web server
from bs4 import BeautifulSoup #parse the page
from geopy.geocoders import Nominatim #get coordinates of locations
from math import sin, cos, sqrt, atan2, radians, pi # math stuff
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.basemap import Basemap
import datetime as dt
import matplotlib.dates as mdates
import plotly
plotly.tools.set_credentials_file(username='YOURUSERNAME', api_key='YOURAPIKEY') #you need to create a free account on plotly
import plotly.plotly as py
from plotly.graph_objs import *
import webbrowser
from datetime import datetime
from time import sleep
import sys


#print info about earthquake
def printinfo (magnitude,time,day,location,depth):
    return 'There was an earthquake of magnitude %s at %s (UTC) %s in %s. Depth was %s' % ( magnitude,time, day, location, depth)

#get lat and long of a place
def get_location_lat_long (locate):
    geolocator = Nominatim()
    location = geolocator.geocode(locate)
    return ((location.latitude, location.longitude))

#calculate distance between places
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

data = {
    'magnitude' : [],
    'time' : [],
    'day' : [],
    'location' : [],
    'depth' : [],
    'latitude' : [],
    'longitude' : [],
}
while True:
    try:
        town = input("Enter name of town you want to get info: ")
        locate = get_location_lat_long(town)
        if  town.isdigit():
            raise ValueError
        break
    except:
        print ('Ops! It looks like the place you have typed it\'s not in the database or you may have typed it incorrectly. Please type it again')

while True:
    try:
        radius_to_search = input("In what range of "  + town + " you want to search for earthquakes? (radius in km) ")
        if radius_to_search.isdigit():
            break
        else:
            raise ValueError
    except:
        print ('Ops something went wrong! Try again')

while True:
    try:
        print ('Which period are you interested on? ')
        print ('Insert the day you want to start from (YYYY-MM-DD): ')
        start = input('from: ')
        end = input('to: ')
        startday = datetime.strptime(start, "%Y-%m-%d")
        endday = datetime.strptime(end, "%Y-%m-%d")
        if startday > endday:
            raise ValueError
        break
    except:
        print ('Ops! It looks like you are starting from the past! Try again!')

for i in range(24):      # Number of pages plus one 
    url = "http://info.terremoti.ingv.it/events?starttime=2016-09-07+00%3A00%3A00&endtime=2017-09-07+23%3A59%3A59&last_nd=90&minmag=2&maxmag=10&mindepth=-10&maxdepth=1000&minlat=-90&maxlat=90&minlon=-180&maxlon=180&minversion=100&limit=30&orderby=ot-desc&tdmt_flag=-1&lat=0&lon=0&maxradiuskm=-1&wheretype=area&box_search=Mondo&timezone=UTC&page={}".format(i) #90 days
    sys.stdout.write('\r')
    sys.stdout.write("scanning [%-23s] \r" % ('='*i))
    sys.stdout.flush()
    sleep(0.25)
    page =  requests.get(url)
    soup = BeautifulSoup(page.content,'html.parser')
    all_links = soup.find_all("a")
    all_tables = soup.find_all("table")
    right_table = soup.find_all('table' , class_='table table-condensed table-hover')
    for table in right_table:
        for row in table.findAll('tr'):
            Info=[]
            cells = row.findAll('td')
            for i in cells:
                Info.append(i.find(text=True))
            if len(Info) > 0 :
                magnitude =  str(Info[1][-3:])
                time = str(Info[0][-9:])
                day = str(Info[0][:11])
                location = str(Info[2])
                depth = str(Info[3])
                latitude =  str(Info[4])
                longitude = str(Info[5])
                data['magnitude'].append(magnitude)
                data['time'].append(time)
                data['day'].append(day)
                data['location'].append(location)
                data['depth'].append(depth)
                data['latitude'].append(latitude)
                data['longitude'].append(longitude)
                df = pd.DataFrame(data)
                df.latitude = df.latitude.astype(float)
                df.longitude = df.longitude.astype(float)


df['magnitude'] = df['magnitude'].astype('float')
df['latitude'] = df['latitude'].astype('float')
df['longitude'] = df['longitude'].astype('float')
df['depth'] = df['depth'].astype('int')
df['location'] = df['location'].astype('str')
df['day'] = pd.to_datetime(df['day'])
df['time'] = pd.to_datetime(df['time']).dt.time
df_lat = df.latitude.tolist()
df_long = df.longitude.tolist()


area = []
for i in range(len(df_lat)):
    distance_between_towns = calculate_distance(df_lat[i],locate[0], df_long[i], locate[1])
    area.append(calculate_area(distance_between_towns))
    
areatosearch = calculate_area(int(radius_to_search))
Area = pd.Series(area)
df['Area'] = Area.values


df = df[(df['location'].str.contains(town,case=False)) | (df['Area'] <= areatosearch)]
df = df[((df['day']<=endday) & (df['day']>=startday))]
df = df.sort_values(by='day', ascending=False)

lon_list = df.longitude.tolist()
lat_list = df.latitude.tolist()
locat_list = df.location.tolist()
df['day'] = df['day'].dt.date #dropping the time bit (00:00:00)
dates =df.day.tolist()
magn = df.magnitude.tolist()
dep = df.depth.tolist()
Time = df.time.tolist()
Areas = df.Area.tolist()
message = [str(m)+', Mag '+str(n)+ ', Depth ' + str(d) + ' Km, Day ' + str(g)  for m,n,d,g in zip(locat_list,magn,dep,dates)]
c=-1
for i in locat_list:
    c=c+1
    print (printinfo(str(magn[c]), str(Time[c]),str(dates[c]), locat_list[c],str(dep[c])))
    

#generating interactive plot                                                                                                                                                   
latmap = round(locate[0],2)
lonmap = round(locate[1],2)

mapbox_access_token = 'YOUR_TOKEN_HERE' #use your mapbox_access_token here

datamap = Data([
    Scattermapbox(
        lat=lat_list,
        lon=lon_list,
        mode='markers',
        marker=Marker(
            size=8,
            color = magn,
            colorscale = 'Jet',
            showscale=True,
            cmax=8,
            cmin=2
        ),
        text=message,
    )
])

layout = Layout(
    autosize=True,
    hovermode='closest',
    mapbox=dict(
        accesstoken=mapbox_access_token,
        bearing=0,
        center=dict(
            lat=latmap,
            lon=lonmap
        ),
 pitch=0,
        zoom=10
    ),
)

fig = dict(data=datamap, layout=layout)
py.iplot(fig, filename='Map')

#opening web page with plot                                                                                                                                                   \
                                                                                                                                                                               
#url = 'https://plot.ly/~francolz/0'                                                                                                                                            
url = 'your_url'
# MacOS                                                                                                                                                                       
chrome_path = 'open -a /Applications/Google\ Chrome.app %s'                                                                                                                    
webbrowser.get(chrome_path).open(url)  


