# webscraping-earthquake
This is a simple python project that reads live earthquakes data from the INGV (CENTRO NAZIONALE TERREMOTI) website and gives you info about particular areas you may be interested on.
In particular, the tool asks the user to input a location, a time range and the radius of the area around the chosen location the user wants to look at, prints out a message about recorded sismic activities for that area and plots the results on a plotly interactive map that pops up on your browser.

Map plot caveat:
You need to have a free plotly account and use you credentials here 
plotly.tools.set_credentials_file(username='YOUR_USER_NAME', api_key='YOUR_API_KEY') when importing plotly and your mapbox access token to generate the plot.

You can sign up to plotly here https://plot.ly/feed/ and here https://www.mapbox.com/signin/ to mapbox.

# Installation #
## Download the code
* Clone this repository to your machine
* cd into the webscraping-earthquake folder using `cd webscraping-earthquake`

## Install the requirements ##
* Install the requirements using `pip3 install -r requirements.txt`
  * Make sure you are using Python 3
  
# Usage #
* Get your api key from https://plot.ly/python/getting-started/#installation  and your mapbox access token from https://www.mapbox.com/help/how-access-tokens-work/
* Open this file `~/.plotly/.credentials` with your favourite text editor and check that your plotly api key and username are correct in that file (Note: you need you update your key manually in that file if you generate a new key)
* Open the file `keys.txt` with a text editor and substitute each entries with your plotly username, plotly apy key and mapbox token in this order. Make sure to use just a comma to separete them, no other spaces.
* Run web_scraping_earthquakes.py as `python3 web_scraping_earthquakes.py`

