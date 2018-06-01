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
  
def processWeather(req):
    result = req.get("result")
    parameters = result.get("parameters")
    city = parameters.get("geo-city")
    observation = owm.weather_at_place(city)
    w = observation.get_weather()
    description = w.get_detailed_status()
    description = description[0].upper()+description[1:]
    wind_res=w.get_wind()
    wind_speed=str(int(round(wind_res.get('speed'))))
    wind=str(processWindDegrees(wind_res.get('deg')))
    humidity=str(w.get_humidity())
    celsius_result=w.get_temperature('celsius')
    temp=str(int(round(celsius_result.get('temp'))))
    string = random.choice(WEATHER_CURRENT)
    return string 

def processWeatherOutfit(req):
    result = req.get("result")
    parameters = result.get("parameters")
    city = parameters.get("geo-city")
    if city=="":
        string = "Non posso darti questo tipo di informazioni senza essere a conoscenza del luogo..."
        return string
    else:
        outfit = parameters.get("outfit")
        fc = owm.three_hours_forecast(city)
        observation = owm.weather_at_place(city)
        w = observation.get_weather()
        celsius_result=w.get_temperature('celsius')
        min_temp=int(round(celsius_result.get('temp_min')))
        max_temp=int(round(celsius_result.get('temp_max')))
        if outfit in COLD_WEATHER:
            answer = random.choice(LIST_YES) if min_temp < _TEMP_LIMITS[
                'chilly']['C'] else random.choice(LIST_NO)
        elif outfit in WARM_WEATHER:
            answer = random.choice(LIST_YES) if max_temp < _TEMP_LIMITS[
                'warm']['C'] else random.choice(LIST_NO)
        elif outfit in HOT_WEATHER:
            answer = random.choice(LIST_YES) if max_temp < _TEMP_LIMITS[
                'hot']['C'] else random.choice(LIST_NO)
        elif outfit in RAIN:
            answer = random.choice(LIST_YES) if fc.will_have_rain() else random.choice(LIST_NO)
        elif outfit in SNOW:
            answer = random.choice(LIST_YES) if fc.will_have_snow() else random.choice(LIST_NO)
        elif outfit in SUN:
            answer = random.choice(LIST_YES) if fc.will_have_sun() else random.choice(LIST_NO)
        else:
            return "Non penso di aver capito bene cosa vorresti indossare."
        return answer
      
def processWeatherTemperature(req):
        result = req.get("result")
        parameters = result.get("parameters")
        city = parameters.get("geo-city")
        if city=="":
            string = "Non posso darti questo tipo di informazioni senza essere a conoscenza del luogo..."
            return string
        else:
            observation = owm.weather_at_place(city)
            w = observation.get_weather()
            celsius_result=w.get_temperature('celsius')
            temp=int(round(celsius_result.get('temp')))
  
            if temp >= _TEMP_LIMITS['hot']['C']:
                answer = random.choice(LIST_HOT)
            elif temp > _TEMP_LIMITS['chilly']['C']:
                answer = random.choice(LIST_WARM)
            elif temp > _TEMP_LIMITS['cold']['C']:
                answer = random.choice(LIST_CHILLY)
            else:
                answer = random.choice(LIST_COLD)
        answer = answer.format(city = city, temp = str(temp))
        return answer
      
#processing the request from dialogflow
def processRequest(req):
    
    result = req.get("result")
    parameters = result.get("parameters")
    action = result.get("action")
    
    if action=="weather":
        speech = processWeather(req)
    elif action=="weather.outfit":
        speech = processWeatherOutfit(req)
    else:
        speech = processWeatherTemperature(req)
            
    return {
        "speech": speech,
        "displayText": speech,
        "source": "dialogflow-weather-by-dinocca-graziano"
            }

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    print("Starting app on port %d" % port)
    app.run(debug=False, port=port, host='0.0.0.0')
