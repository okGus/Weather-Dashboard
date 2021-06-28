from app import app
from flask import render_template, redirect, request
import requests
from datetime import date, datetime

api_key = ""


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/result', methods=['POST', 'GET'])
def result():
    zip_code = request.form['zipcode']
    
    # current weather
    data = get_weather_data(zip_code, api_key)
    temp = "{0:.2f}".format(data["main"]["temp"])
    feels_like = "{0:.2f}".format(data["main"]["feels_like"])
    weather = data["weather"][0]["main"]
    location = data["name"]

    lat = data["coord"]["lat"]
    lon = data["coord"]["lon"]

    # hourly
    data2 = get_weather_data2(lat, lon, api_key)
    h_temp = []
    for x in range(len(data2["hourly"])):
        temperature = "{0:.2f}".format(data2["hourly"][x]["temp"])
        h_temp.append(temperature)

    h_feels_like = []
    for x in range(len(data2["hourly"])):
        feels = "{0:.2f}".format(data2["hourly"][x]["feels_like"])
        h_feels_like.append(feels)

    h_weather = []
    for x in range(len(data2["hourly"])):
        weath = data2["hourly"][x]["weather"][0]["main"]
        h_weather.append(weath)

    hourly = [] 
    for x in range(len(data2["hourly"])):
        dt = int(data2["hourly"][x]["dt"])
        dt = datetime.utcfromtimestamp(dt).strftime('%H:%M')
        hourly.append(dt)

    # daily
    d_temp = []
    for x in range(len(data2["daily"])):
        temperature = data2["daily"][x]["temp"]["day"]
        d_temp.append(temperature)

    d_feels_like_day = []
    for x in range(len(data2["daily"])):
        feels = data2["daily"][x]["feels_like"]["day"]
        d_feels_like_day.append(feels)

    d_feels_like_night = []
    for x in range(len(data2["daily"])):
        feels = data2["daily"][x]["feels_like"]["night"]
        d_feels_like_night.append(feels)

    d_weather = []
    for x in range(len(data2["daily"])):
        weath = data2["daily"][x]["weather"][0]["main"]
        d_weather.append(weath)

    day = []
    for x in range(len(data2["daily"])):
        dt = int(data2["daily"][x]["dt"])
        dt = datetime.utcfromtimestamp(dt).strftime('%A')
        day.append(dt)

    return render_template('result.html', 
                            location=location, temp=temp,
                            feels_like=feels_like, weather=weather,
                            h_temp=h_temp, h_feels_like=h_feels_like,
                            h_weather=h_weather, hourly=hourly,
                            d_temp=d_temp, d_feels_like_day=d_feels_like_day,
                            d_weather=d_weather, d_feels_like_night=d_feels_like_night,
                            day=day)


def get_weather_data(zip_code, api_key):
    api_url = "http://api.openweathermap.org/" \
        "data/2.5/weather?zip={}&units=metric&appid={}".format(zip_code, api_key)
    r = requests.get(api_url)
    return r.json()

def get_weather_data2(lat, lon, api_key):
    api_url = "https://api.openweathermap.org/" \
        "data/2.5/onecall?lat={}&lon={}&units=metric&appid={}".format(lat,lon, api_key)
    r = requests.get(api_url)
    return r.json()
