#!/usr/bin/env python

import ecowitt.api

import os
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
    )


jinja2  = Environment(
    loader=FileSystemLoader("templates"),
    autoescape=select_autoescape()
)

for filename in ["weathercam.html"]:
    template = jinja2.get_template(filename)
    template.stream(
        temperature_value=ecowitt.outdoor_temperature_value(),
        temperature_unit=ecowitt.outdoor_temperature_unit(),
        humidity_value=ecowitt.outdoor_humidity_value(),
        humidity_unit=ecowitt.outdoor_humidity_unit(),
        wind_speed_value=ecowitt.wind_speed_value(),
        wind_speed_unit=ecowitt.wind_speed_unit(),
        uvi_value=ecowitt.uvi_value(),
        google_analytics_id=google_analytics_id,    
    ).dump("output/" + filename)
