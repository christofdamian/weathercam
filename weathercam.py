#!/bin/env python

import ecowitt.api

import os
from dotenv import load_dotenv
from jinja2 import Environment, FileSystemLoader, select_autoescape

load_dotenv()

ecowitt_application_key = os.environ.get("APPLICATION_KEY")
ecowitt_api_key = os.environ.get("API_KEY")
ecowitt_mac = os.environ.get("MAC")
ecowitt_temp_unitid = os.environ.get("TEMP_UNITID")

ecowitt = ecowitt.api.Ecowitt(
    application_key = ecowitt_application_key,
    api_key = ecowitt_api_key,
    mac = ecowitt_mac,
    temp_unitid = ecowitt_temp_unitid
    )


jinja2  = Environment(
    loader=FileSystemLoader("templates"),
    autoescape=select_autoescape()
)

for filename in ["weathercam.html"]:
    print(filename)
    template = jinja2.get_template(filename)
    template.stream(temperature=ecowitt.outdoor_temperature_value()).dump("output/" + filename)
