"""This module defines the text based template responses to be formatted
and sent to users with the proper data
This is meant to be used with the sample weather agent for Dialogflow, located at
https://console.dialogflow.com/api-client/#/agent//prebuiltAgents/Weather
"""

LIST_YES = [
    'Meglio portarlo con te nel caso.',
    'Non fa mai male portarlo con sè.',
    'Meglio averlo e non averne di bisogno che non averlo e averne di bisogno.',
    'Considerando il meteo forse sì.'
]

LIST_NO = [
    'No, you should be fine without it.',
    'I don\'t think that will be necessary.',
    'You can bring it if you like, but I doubt you\'ll need it.',
    'It seems pretty unlikely you\'ll need that.'
]

LIST_COLD = [
    'Quite cold there.',
    'Pretty freezing, I would say.',
    'Don\'t forget your gloves.'
]

LIST_CHILLY = [
    'Quite chilly.',
    'You\'ll need a jacket for sure.'
]

LIST_WARM = [
    'Temperature is okay.'
]

LIST_HOT = [
    'Oh, that\'s hot!',
    'You\'ll definitely need sunscreen.'
]

WEATHER_CURRENT = [
    'The temperature in {place} now is {temperature} and {condition}.',
    'Right now it\'s {temperature} and {condition} in {place}.',
    'It\'s currently {temperature} and {condition} in {place}.',
    'The temperature in {place} is {temperature} and {condition}.'
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
