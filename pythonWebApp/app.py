import os
import requests
import json
import datetime
from flask import Flask, render_template, request
from os import listdir
from os.path import isfile, join

app = Flask(__name__)

bg = os.environ['BG_COLOR']


@app.route('/', methods=["GET"])
def index():
    """On our first function, the user first enters a static site, with only the GET method,
    all this function does is render that first static site or render an error site"""
    try:
        return render_template('webtemp.html', bg=bg)
    except:
        return render_template('errors.html')


@app.route('/', methods=["POST", "GET"])
def parse():
    """Here the major backend happens, we define that we need to receive a city parameter from the webtemp site
    then we insert the name of the city into the api's url, in order to receive a json with updated info
    on that city/region"""

    try:
        city = request.form.get('city')
        url = f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{city}/next7days?unitGroup=metric&key=KRXL6NZ2BB6ZH9DXQLAC83G9X&contentType=json"
        data = requests.get(url).json()
    except:
        return render_template('errors.html')
    """Here we define 3 lists which will store info about day temp, night temp and humidity for the next 7 days"""
    days = []
    nights = []
    humidity = []
    for z in range(7):
        days.append(data['days'][z]['hours'][11]['temp'])
        nights.append(data['days'][z]['hours'][23]['temp'])
        humidity.append(data['days'][z]['humidity'])

    sevendays = {
        'days': days,
        'nights': nights,
        'humidity': humidity
    }
    """Here we define a dictionary which will filter the vast amount of info we receive on query"""
    weather = {
        'location': data['resolvedAddress'],
        'description': data['description'],
        'temperature': data['days'][0]['temp'],
        'humidity': data['days'][0]['humidity']
    }

    with open(f"static/history/{datetime.date.today()}:{city}.json",
              "w+") as outfile:
        json.dump(weather, outfile, indent=4)
        json.dump(sevendays, outfile, indent=4)

    """And lastly we return a rendered page with the results, and we return the lists and dictionary for use
    in the html files"""

    return render_template('index.html', weather=weather, days=days, nights=nights, humidity=humidity, bg=bg)


@app.route('/download', methods=["POST", "GET"])
def download():
    path = "static/history"
    history = [f for f in listdir(path) if isfile(join(path, f))]
    return render_template('download.html', history=history, bg=bg)
