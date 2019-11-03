#!/usr/bin/python3.4
import requests
import pprint
from requests import get
import json


#variable = sys.argv

#I'm not sure what this does exactly
pp = pprint.PrettyPrinter(indent=4)

#read in the location of the weather to be looked up Accuweather location ID
#https://www.accuweather.com
location_file_handle = open("location.txt", "r")
location_read_in = location_file_handle.read()
location_file_handle.close()
location = location_read_in.rstrip("\n\r")

#read in the API key of the application up Accuweather location ID
#https://www.accuweather.com
apiKey_file_handle = open("apiKey.txt", "r")
apiKey_read_in = apiKey_file_handle.read()
apiKey_file_handle.close()
apiKey = apiKey_read_in.rstrip("\n\r")

#Create the string to make the REST API call
API_current_weather = 'http://dataservice.accuweather.com/currentconditions/v1/' + location + '?apikey=' + apiKey
print(API_current_weather)

#Create the string to make the REST API call
API_forcast_weather = 'http://dataservice.accuweather.com//forecasts/v1/daily/1day/' + location + '?apikey=' + apiKey + '&details=true'
print(API_forcast_weather)

#Make API call to get the current weather
current_w = requests.get(API_current_weather)

#Make API call to get the forecasted weather
forecast_w = requests.get(API_forcast_weather)

#Print API call status codes to verify the request was returned successfully
print('Current weather API call returned status code of: ' + str(current_w.status_code))
print('Forecast weather API call returned status code of: ' + str(forecast_w.status_code))

#Write The API status code to file for current weather call
cw = open("Current_Weather_Status.txt", "w")
cw.write(str(current_w.status_code))

#Write API call status code to file for forecast weather call
fw = open("Forecast_Weather_Status.txt", "w")
fw.write(str(forecast_w.status_code))

#write weather forcast to file
with open('Weather_Forcast.txt', 'w') as outfile:
    json.dump(forecast_w.json(), outfile, indent=4)

#write current weather to file
with open('Current Weather.txt', 'w') as outfile:
    json.dump(current_w.json(), outfile, indent=4)



