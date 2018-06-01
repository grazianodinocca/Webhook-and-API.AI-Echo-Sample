from flask import Flask,request,make_response
import os,json
import pyowm
import os
import random
from config import (_TEMP_LIMITS, _DEFAULT_TEMP_UNIT, WWO_API_KEY,
                    MAX_FORECAST_LEN)

from responses import (
    LIST_YES,
    LIST_NO,
    LIST_COLD,
    LIST_CHILLY,
    LIST_WARM,
    LIST_HOT,
    WEATHER_CURRENT,
    WEATHER_DATE,
    WEATHER_WEEKDAY,
    WEATHER_DATE_TIME,
    WEATHER_TIME_PERIOD,
    WEATHER_TIME_PERIOD_DEFINED,
    WEATHER_DATE_PERIOD_WEEKEND,
    WEATHER_DATE_PERIOD,
    WEATHER_ACTIVITY_YES,
    WEATHER_ACTIVITY_NO,
    RESPONSE_WEATHER_CONDITION,
    RESPONSE_WEATHER_OUTFIT)
from entities import (WINTER_ACTIVITY, SUMMER_ACTIVITY, DEMI_ACTIVITY,
                              CONDITION_DICT, UNSUPPORTED, COLD_WEATHER,
                              WARM_WEATHER, HOT_WEATHER, RAIN, SNOW, SUN)

app = Flask(__name__)
owmapikey=os.environ.get('OWMApiKey') #or provide your key here
owm = pyowm.OWM(owmapikey, language='it')

#geting and sending response to dialogflow
@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)

    print("Request:")
    print(json.dumps(req, indent=4))
    
    res = processRequest(req)

    res = json.dumps(res, indent=4)
    print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r

def processWindDegrees(wind):
    if wind==0:
        return "Nord"
    if wind>0 or wind<90:
        return "Nord-Est"
    if wind==90:
        return "Est"
    if wind>90 or wind<180:
        return "Sud-Est"
    if wind==180:
        return "Sud"
    if wind>180 or wind<270:
        return "Sud-Ovest"
    if wind==270:
        return "Ovest"
    if wind>270 or wind<360:
        return "Nord-Ovest"
      
def datetime(time):
    time.replace("T"," ")
    time.replace("Z","")
    return time
  
def processWeather(req):
    result = req.get("result")
    parameters = result.get("parameters")
    city = parameters.get("geo-city")
    observation = owm.weather_at_place(city)
    w = observation.get_weather()
    latlon_res = observation.get_location()
    print(w.get_status())
    description = w.get_detailed_status()
    description = description[0].upper()+description[1:]
    lat=str(latlon_res.get_lat())
    lon=str(latlon_res.get_lon())
    wind_res=w.get_wind()
    wind_speed=str(int(round(wind_res.get('speed'))))
    wind=str(processWindDegrees(wind_res.get('deg')))
    humidity=str(w.get_humidity())
    celsius_result=w.get_temperature('celsius')
    temp=str(int(round(celsius_result.get('temp'))))
    temp_min_celsius=str(celsius_result.get('temp_min'))
    temp_max_celsius=str(celsius_result.get('temp_max'))    
    fahrenheit_result=w.get_temperature('fahrenheit')
    temp_min_fahrenheit=str(fahrenheit_result.get('temp_min'))
    temp_max_fahrenheit=str(fahrenheit_result.get('temp_max'))
    string = description + " a " + city + " con "+temp+"°C. Umidità al "+humidity+"% con venti da " +wind+ " a "+wind_speed+" km/h."
    return string 

def processWeatherOutfit(req):
    result = req.get("result")
    parameters = result.get("parameters")
    city = parameters.get("geo-city")
    if city=="":
        string = "Per andare dove?"
        return string
    else:
        outfit = parameters.get("outfit")
        fc = owm.three_hours_forecast(city)
        time = parameters.get("date-time")
        time = datetime(time)
        print(time)
        fc.get_weather_at(time)
        observation = owm.weather_at_place(city)
        w = observation.get_weather()
        celsius_result=w.get_temperature('celsius')
        print(fc.will_have_rain())
        min_temp=int(round(celsius_result.get('temp_min')))
        max_temp=int(round(celsius_result.get('temp_max')))
        if outfit in COLD_WEATHER:
            answer = random.choice(LIST_YES) if min_temp < _TEMP_LIMITS[
                'chilly']['C'] else random.choice(LIST_NO)
        elif outfit in WARM_WEATHER:
            answer = random.choice(LIST_YES) if max_temp < _TEMP_LIMITS[
                'warm']['C'] else random.choice(LIST_NO)
        elif outfit in HOT_WEATHER:
            answer =random.choice(LIST_YES) if max_temp < _TEMP_LIMITS[
                'hot']['C'] else random.choice(LIST_NO)
        elif outfit in RAIN:
            answer = random.choice(LIST_YES) if fc.will_have_rain() else random.choice(LIST_NO)
        elif outfit in SNOW:
            answer = random.choice(LIST_YES) if fc.will_have_snow() else random.choice(LIST_NO)
        elif outfit in SUN:
            answer = random.choice(LIST_YES) if fc.will_have_sun() else random.choice(LIST_NO)
        else:
            answer = "Non penso di aver capito bene cosa vorresti indossare."
        return answer
    
#processing the request from dialogflow
def processRequest(req):
    
    result = req.get("result")
    parameters = result.get("parameters")
    action = result.get("action")
    
    if action=="weather":
        speech = processWeather(req)

    if action=="weather.outfit":
        speech = processWeatherOutfit(req)
            
    return {
        "speech": speech,
        "displayText": speech,
        "source": "dialogflow-weather-by-dinocca-graziano"
            }

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    print("Starting app on port %d" % port)
    app.run(debug=False, port=port, host='0.0.0.0')
