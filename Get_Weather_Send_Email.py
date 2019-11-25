#!/usr/bin/python3.4
import smtplib
from email.mime.image import MIMEImage
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import random
import requests
import pprint
from requests import get
import logging
import json
import datetime
import time
import sys


"""
Program written by Daryl Allen

daryl.allen.jr@gmail.com

"""
#Set some initial variables, indent spacing of print pretty, get the time and save it to a variable
pp = pprint.PrettyPrinter(indent=4)
now = datetime.datetime.now()

#The purpose of this code is to make a string that can be compared to imported text from the Accuweather output.
#The formatting on text read in from a file is not something I know how to duplicate, so I output my text to a file
#so that it can be imported later in a format similar to other imported text.
bl = open('baseline.txt','w')
bl.write('200')
bl.close()

#Read in the base line status code of 200 created earlier  in the program
test = open('baseline.txt', 'r')
baseline = test.readline()
test.close()

#Read in the Weather Forecast that was produced from the Accuweather script, put into variable called forecast_w
with open('Weather_Forcast.txt') as json_file:
    forecast_w = json.load(json_file)

#Read in the Current Weather that was produced from the Accuweather script, put into variable called current_w
with open('Current Weather.txt') as json_file:
    current_w = json.load(json_file)

#Read in the file that has the status code returned from the API call, put it into variable cw
cw = open("Current_Weather_Status.txt", "r")
currentWeatherStatus = cw.readline()
cw.close()

#Read in the file that has the status code returned from the API call, put it into variable fw
fw = open("Forecast_Weather_Status.txt", "r")
forecastWeatherStatus = fw.readline()
fw.close()


#Check if the current weather API and forcast weather API returned a useable status code of 200
if currentWeatherStatus == baseline and forecastWeatherStatus == baseline:
    #Request object documentation: https://developer.accuweather.com/accuweather-current-conditions-api/apis/get/currentconditions/v1/%7BlocationKey%7D

    #abstract information from the imported JSON and form sentences that explain what the weather will be like
    good_morning_message1 = 'Hello Daryl, today is ' + str(now.strftime('%A, %B %d, %H:%M hours.\n\n'))
    good_morning_message2 = 'Current conditions: ' + str(current_w[0]["Temperature"]["Imperial"]["Value"]) + ' degrees and ' + current_w[0]["WeatherText"]
    good_morning_message3 = '\nForecast high of ' + str(forecast_w["DailyForecasts"][0]["Temperature"]["Maximum"]["Value"]) + ' degrees and low of ' + str(forecast_w["DailyForecasts"][0]["Temperature"]["Minimum"]["Value"]) + ' degrees.'
    good_morning_message4 = '\nConditions predicted to be ' + forecast_w["DailyForecasts"][0]["Day"]["IconPhrase"] + ' during the day and ' + forecast_w["DailyForecasts"][0]["Night"]["IconPhrase"] + ' at night.\n\n'
    good_morning_message5 = 'Sunrise at ' + str(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(forecast_w["DailyForecasts"][0]["Sun"]["EpochRise"])))
    good_morning_message6 = '\nSunset at ' + str(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(forecast_w["DailyForecasts"][0]["Sun"]["EpochSet"]))) + '\n\n'
    good_morning_message7 = 'Note: ' + forecast_w["Headline"]["Text"]
    good_morning_message8 = "\n\nhttp://www.accuweather.com/en/us/denver-co/80203/daily-weather-forecast/347810?lang=en-us"

    #Aggregate my lines of the message into one message that can be packed into an email body
    message = good_morning_message1 + good_morning_message2 + good_morning_message3 + good_morning_message4 + good_morning_message5 + good_morning_message6 + good_morning_message7 + good_morning_message8
else:
    message = "Weather Data could not be retrieved from http://dataservice.accuweather.com/"
    print(message)
    sys.exit()




####################### Get ip address #########################################
#find the public ip address of where this code is running from and store it in a variable
ip = get('https://api.ipify.org').text
###############################################################################

bot_number = str(random.randint(1,3000))

#Read in file containing the email user account for logging in, email user's password, addressee of the email
emailMetadata = open("Email_Metadata.txt", "r")

#email_user account we will be logging into to send the mail, cast it to a string type
email_user = str(emailMetadata.readline())


#email_password for account, cast it to string type
email_password = str(emailMetadata.readline())


#email_send = specify who the email will be sent to
email_send = str(emailMetadata.readline())


#Close the email metatdat file and release the handle
emailMetadata.close()

#write out the email subject line
email_subject = 'Bot# ' + bot_number + "'s Daily Weather and Network update"


#create a sentence that specifies the ip address that the code is running from
ip_and_signature = '\n\nYour home network public IP address is: {}'.format(ip) + '\n\n-Bot# ' + bot_number

#Create the email message body by combining the previous text and the ip addressing.
body = message + ip_and_signature

#construct the message header and body for sending
msg = MIMEMultipart()
msg['To'] = email_send
#msg['Cc'] = cc
msg['From'] = email_user
msg['Subject'] = email_subject
#text.add_header("Content-Disposition", "inline")
msg.attach(MIMEText(body, 'plain'))

#Convert the message header to string data type so that it can be sent
text = msg.as_string()

#Initialize the connection to the mail server
mail = smtplib.SMTP('smtp.gmail.com', 587)

#Start the conversation with the email server
mail.ehlo()

#start the TLS conversation (i.e. encryption)
mail.starttls()

#login to the email account
mail.login(email_user, email_password)


try:
    #mail.sendmail('bot.daryl.allen@gmail.com','To: \nallend43@gmail.com', content)
    mail.sendmail(msg['From'], msg['To'], text)
    print('Mail Sent Sucessfully')
except:
    print('There was an error!')

mail.close()




