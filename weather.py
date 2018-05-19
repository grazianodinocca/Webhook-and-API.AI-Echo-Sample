from flask import Flask,request,make_response
import os,json
import pyowm
import os

app = Flask(__name__)
owmapikey=os.environ.get('OWMApiKey') #or provide your key here
owm = pyowm.OWM(owmapikey)

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
        return "nord"
    if wind>0 or wind<90:
        return "nord-est"
    if wind==90:
        return "est"
    if wind>90 or wind<180:
        return "sud-est"
    if wind==180:
        return "sud"
    if wind>180 or wind<270:
        return "sud-ovest"
    if wind==270:
        return "ovest"
    if wind>270 or wind<360:
        return "nord-ovest"
    
#processing the request from dialogflow
def processRequest(req):
    
    result = req.get("result")
    parameters = result.get("parameters")
    city = parameters.get("geo-city")
    observation = owm.weather_at_place(city)
    w = observation.get_weather()
    latlon_res = observation.get_location()
    description = w.get_detailed_status()
    lat=str(latlon_res.get_lat())
    lon=str(latlon_res.get_lon())
    wind_res=w.get_wind()
    wind_speed=str(wind_res.get('speed'))
    wind=str(processWindDegrees(wind_res.get('deg')))
        
    
    humidity=str(w.get_humidity())
    
    celsius_result=w.get_temperature('celsius')
    temp=str(celsius_result.get('temp'))
    temp_min_celsius=str(celsius_result.get('temp_min'))
    temp_max_celsius=str(celsius_result.get('temp_max'))
    
    fahrenheit_result=w.get_temperature('fahrenheit')
    temp_min_fahrenheit=str(fahrenheit_result.get('temp_min'))
    temp_max_fahrenheit=str(fahrenheit_result.get('temp_max'))
    speech = description + " a " + city + " con "+temp+"°C. Umidità al "+humidity+"% con venti da " +wind+ " a "+wind_speed+" km/h."
    
    return {
        "speech": speech,
        "displayText": speech,
        "source": "dialogflow-weather-by-dinocca-graziano"
        }
    
if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    print("Starting app on port %d" % port)
    app.run(debug=False, port=port, host='0.0.0.0')
