#!/usr/bin/env python

import ecowitt.api

import os
import json
from dotenv import load_dotenv
from jinja2 import Environment, FileSystemLoader, select_autoescape

load_dotenv()

ecowitt_application_key = os.environ.get("APPLICATION_KEY")
ecowitt_api_key = os.environ.get("API_KEY")
ecowitt_mac = os.environ.get("MAC")
ecowitt_temp_unitid = int(os.environ.get("TEMP_UNITID"))
ecowitt_wind_speed_unitid = int(os.environ.get("WIND_SPEED_UNITID"))

google_analytics_id = os.environ.get("GOOGLE_ANALYTICS_ID")

ecowitt = ecowitt.api.Ecowitt(
    application_key=ecowitt_application_key,
    api_key=ecowitt_api_key,
    mac=ecowitt_mac,
    temp_unitid=ecowitt_temp_unitid,
    wind_speed_unitid=ecowitt_wind_speed_unitid,
    call_back="outdoor,wind,pressure,solar_and_uvi"
    )

# Get historical temperature data
try:
    history_data = ecowitt.get_device_history()
    temperature_history = []
    if (history_data and
        isinstance(history_data, dict) and
        'outdoor' in history_data and
        'temperature' in history_data['outdoor'] and
        'list' in history_data['outdoor']['temperature']):

        temp_list = history_data['outdoor']['temperature']['list']
        for timestamp, temp_value in temp_list.items():
            # Convert Unix timestamp to ISO format for JavaScript
            from datetime import datetime
            dt = datetime.fromtimestamp(int(timestamp))
            temperature_history.append({
                'time': dt.isoformat(),
                'temperature': float(temp_value)
            })

        # Sort by timestamp
        temperature_history.sort(key=lambda x: x['time'])

except Exception as e:
    print(f"Error getting history data: {e}")
    temperature_history = []

jinja2  = Environment(
    loader=FileSystemLoader("templates"),
    autoescape=select_autoescape()
)

for filename in ["weathercam.html"]:
    template = jinja2.get_template(filename)
    template.stream(
        temperature_value=ecowitt.outdoor_temperature_value(),
        temperature_unit=ecowitt.outdoor_temperature_unit(),
        feels_like_value=ecowitt.feels_like_temperature_value(),
        feels_like_unit=ecowitt.feels_like_temperature_unit(),
        humidity_value=ecowitt.outdoor_humidity_value(),
        humidity_unit=ecowitt.outdoor_humidity_unit(),
        wind_speed_value=ecowitt.wind_speed_value(),
        wind_speed_unit=ecowitt.wind_speed_unit(),
        pressure_value=ecowitt.pressure_value(),
        pressure_unit=ecowitt.pressure_unit(),
        uvi_value=ecowitt.uvi_value(),
        solar_value=ecowitt.solar_value(),
        solar_unit=ecowitt.solar_unit(),
        google_analytics_id=google_analytics_id,
        temperature_history_json=json.dumps(temperature_history),
    ).dump("output/" + filename)
