# webscraping-earthquake
This is a simple python project that reads live earthquakes data from the INGV (CENTRO NAZIONALE TERREMOTI) website and gives you info about particular areas you may be interested on.
In particular, the tool asks the user to input a location, a time range and the radius of the area around the chosen location the user wants to look at, prints out a message about recorded sismic activities for that area and plots the results on a plotly interactive map that pops up on your browser.

Map plot caveat:
You need to have a free plotly account and use you credentials here 
plotly.tools.set_credentials_file(username='YOUR_USER_NAME', api_key='YUOR_API_KEY') when importing plotly and your mapbox access token to generate the plot.

You can sign up to plotly here https://plot.ly/feed/ and here https://www.mapbox.com/signin/ to mapbox.

## Installation ##
*Item 1


