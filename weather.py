from flask import Flask,request,make_response
import os,json
import pyowm
import os

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
        string = "In quale città?"
        return string
    else:
        return city
    
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
