#!/usr/bin/env python

import ecowitt.api

import os
import json
from dotenv import load_dotenv
from jinja2 import Environment, FileSystemLoader, select_autoescape

load_dotenv()

ecowitt_application_key = os.environ.get("ECOWITT_APPLICATION_KEY")
ecowitt_api_key = os.environ.get("ECOWITT_API_KEY")
ecowitt_mac = os.environ.get("ECOWITT_MAC")
ecowitt_temp_unitid = int(os.environ.get("ECOWITT_TEMP_UNITID"))
ecowitt_wind_speed_unitid = int(os.environ.get("ECOWITT_WIND_SPEED_UNITID"))

google_analytics_id = os.environ.get("GOOGLE_ANALYTICS_ID")
posthog_id = os.environ.get("POSTHOG_ID")

ecowitt_api = ecowitt.api.Ecowitt(
    application_key=ecowitt_application_key,
    api_key=ecowitt_api_key,
    mac=ecowitt_mac,
    temp_unitid=ecowitt_temp_unitid,
    wind_speed_unitid=ecowitt_wind_speed_unitid,
    call_back="outdoor,wind,pressure,solar_and_uvi"
    )

# Get real-time data
ecowitt_realtime = ecowitt_api.get_real_time_data()

# Get historical temperature and humidity data
try:
    history_data = ecowitt_api.get_device_history()
    temperature_history = []
    humidity_history = []

    if (history_data and
        isinstance(history_data, dict) and
        'outdoor' in history_data):

        # Process temperature data
        if ('temperature' in history_data['outdoor'] and
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

        # Process humidity data
        if ('humidity' in history_data['outdoor'] and
            'list' in history_data['outdoor']['humidity']):
            humidity_list = history_data['outdoor']['humidity']['list']
            for timestamp, humidity_value in humidity_list.items():
                # Convert Unix timestamp to ISO format for JavaScript
                from datetime import datetime
                dt = datetime.fromtimestamp(int(timestamp))
                humidity_history.append({
                    'time': dt.isoformat(),
                    'humidity': float(humidity_value)
                })

        # Sort by timestamp
        temperature_history.sort(key=lambda x: x['time'])
        humidity_history.sort(key=lambda x: x['time'])

except Exception as e:
    print(f"Error getting history data: {e}")
    temperature_history = []
    humidity_history = []

jinja2  = Environment(
    loader=FileSystemLoader("templates"),
    autoescape=select_autoescape()
)

for filename in ["weathercam.html"]:
    template = jinja2.get_template(filename)
    template.stream(
        temperature_value=ecowitt_realtime.outdoor_temperature_value(),
        temperature_unit=ecowitt_realtime.outdoor_temperature_unit(),
        feels_like_value=ecowitt_realtime.feels_like_temperature_value(),
        feels_like_unit=ecowitt_realtime.feels_like_temperature_unit(),
        humidity_value=ecowitt_realtime.outdoor_humidity_value(),
        humidity_unit=ecowitt_realtime.outdoor_humidity_unit(),
        wind_speed_value=ecowitt_realtime.wind_speed_value(),
        wind_speed_unit=ecowitt_realtime.wind_speed_unit(),
        pressure_value=ecowitt_realtime.pressure_value(),
        pressure_unit=ecowitt_realtime.pressure_unit(),
        uvi_value=ecowitt_realtime.uvi_value(),
        solar_value=ecowitt_realtime.solar_value(),
        solar_unit=ecowitt_realtime.solar_unit(),
        google_analytics_id=google_analytics_id,
        posthog_id=posthog_id,
        temperature_history_json=json.dumps(temperature_history),
        humidity_history_json=json.dumps(humidity_history),
    ).dump("output/" + filename)
