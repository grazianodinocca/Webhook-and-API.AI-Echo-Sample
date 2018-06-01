"""This module defines the text based template responses to be formatted
and sent to users with the proper data
This is meant to be used with the sample weather agent for Dialogflow, located at
https://console.dialogflow.com/api-client/#/agent//prebuiltAgents/Weather
"""

LIST_YES = [
    'Meglio portarlo con te.',
    'Non fa mai male portarlo con sè.',
    'Meglio averlo e non averne di bisogno che non averlo e averne di bisogno.',
    'Considerando il meteo è meglio averlo con sè.'
]

LIST_NO = [
    'No, puoi anche non portarlo.',
    'Non penso sarà necessario...',
    'Potresti anche portarlo ma dubito che ne avrai di bisogno.',
    'A mio parere non ti servirà.'
]

LIST_COLD = [
    'Fa freddissimo a {city}. La temperatura si aggira attorno a {temp}°C.',
    '{temp}°C. Fa molto freddo direi a {city}...',
    'Fa molto freddo a {city}, faresti meglio a non dimenticarti i guanti. Ci sono {temp}°C.',
    'La temperatura è di {temp}°C a {city}.'
]

LIST_CHILLY = [
    'Fa piuttosto freddo a {city}. La temperatura è di {temp}°C.',
    'Ti servirebbe sicuramente una giacca con {temp}°C a {city}.',
    'Non fa molto caldo a {city}. Ci sono {temp}°C.',
    'La temperatura è di {temp}°C a {city}.'
]

LIST_WARM = [
    'La temperatura è ottima a {city}. Si attesta attorno a {temp}°C.',
    'Le temperature si aggirano intorno a valori ottimali a {city} con una media di {temp}°C.',
    'La temperatura è di {temp}°C a {city}.'
]

LIST_HOT = [
    'Oh, a {city} fa molto caldo! Ci sono {temp}°C.',
    'Fa molto caldo a {city}. La temperatura è di {temp}°C.',
    'Le temperature sono molto elevate a {city}, fa un gran caldo.',
    'La temperatura è di {temp}°C a {city}.'
]

WEATHER_CURRENT = [
    'A {city} {descr} con {temperature}°C e venti da {direct} a {speed} km/h.',
    'Adesso la temperatura è di {temperature}°C a {city} con {descr}. Umidità al {umid}%.',
    'Attualmente {descr} con {temperature}°C a {city}. Venti a {speed} km/h provenienti da {direct}.',
    'La temperatura a {place} è di {temperature}°C con {descr} e venti da {direct}.',
    'A {city} {descr} con {temp}°C. Umidità al {umid}% con venti da {direct} a {speed} km/h."
]

WEATHER_DATE = [
    '{day} in {place} it will be around {temperature} and {condition}.',
    '{day} in {place} you can expect it to be around {temperature} and \
    {condition}.',
    '{day} in {place} you can expect {condition}, with temperature around \
    {temperature}.',
    '{day} in {place} it will be {condition}, {temperature}.',
]

WEATHER_WEEKDAY = [
    'On {date} in {place} it will be {condition}, {temperature}.',
    'On {date} in {place} it\'s expected to be {condition}, {temperature}.',
    'The forecast for {date} in {place} is {condition}, {temperature}.',
    '{date} in {place} is expected to be {condition}, {temperature}.'
]

WEATHER_DATE_TIME = [
    '{day} in {place} at {time} it will be around {temperature} and \
    {condition}.',
    '{day} in {place} at {time} you can expect it to be around {temperature} \
    and {condition}.',
    '{day} in {place} at {time} you can expect {condition}, with the \
    temperature around {temperature}.',
    '{day} in {place} at {time} it will be {condition}, {temperature}.',
    'At {time} on {day} in {place} it will be {temperature} and {condition}.'
]

WEATHER_TIME_PERIOD = [
    'It will be {condition} in {city} and around {temp} on period from \
    {time_start} till {time_end}.'
]

WEATHER_TIME_PERIOD_DEFINED = [
    'This {time_period} in {place} it will be {temperature} and {condition}.',
    'This {time_period} in {place} you can expect {condition}, with \
    temperature around {temperature}.',
    'Expect a {condition} {time_period} in {place}, with temperature around \
    {temperature}.',
    'It will be {condition} in {place} and around {temperature} this \
    {time_period}.',
]

WEATHER_DATE_PERIOD_WEEKEND = [
    'On Saturday in {city} it will be {condition_sat}, '
    'with temperatures from {sat_temp_min} to {sat_temp_max}. '
    'And Sunday should be {condition_sun}, '
    'with a low of {sun_temp_min} and a high of {sun_temp_max}.'
]

WEATHER_DATE_PERIOD = [
    'During period from {date_start} till {date_end}'
    ' in {city} you can expect {condition}, '
    'with a low of {degree_list_min} and a high of {degree_list_max}.'
]

WEATHER_ACTIVITY_YES = [
    'What a nice weather for {activity}!'
]

WEATHER_ACTIVITY_NO = [
    'Not the best weather for {activity}.'
]

RESPONSE_WEATHER_CONDITION = [
    'Chance of {condition_original} is {condition} percent.'
]

RESPONSE_WEATHER_OUTFIT = [
    'Chance of {condition_original} is {condition} percent. {answer}'
]
