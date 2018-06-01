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
   """Returns a string containing text with a response to the user
    with the weather forecast or a prompt for more information
    Takes the city for the forecast and (optional) dates
    uses the template responses found in weather_responses.py as templates
    """
    parameters = req['queryResult']['parameters']

    print('Dialogflow Parameters:')
    print(json.dumps(parameters, indent=4))

    # validate request parameters, return an error if there are issues
    error, forecast_params = validate_params(parameters)
    if error:
        return error

    # create a forecast object which retrieves the forecast from a external API
    try:
        forecast = Forecast(forecast_params)
    # return an error if there is an error getting the forecast
    except (ValueError, IOError) as error:
        return error

    # If the user requests a datetime period (a date/time range), get the
    # response
    if forecast.datetime_start and forecast.datetime_end:
        response = forecast.get_datetime_period_response()
    # If the user requests a specific datetime, get the response
    elif forecast.datetime_start:
        response = forecast.get_datetime_response()
    # If the user doesn't request a date in the request get current conditions
    else:
        response = forecast.get_current_response()

    return response

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
