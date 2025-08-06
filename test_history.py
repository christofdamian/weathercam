#!/usr/bin/env python

import ecowitt.api
import os
from dotenv import load_dotenv

load_dotenv()

ecowitt_application_key = os.environ.get("APPLICATION_KEY")
ecowitt_api_key = os.environ.get("API_KEY")
ecowitt_mac = os.environ.get("MAC")
ecowitt_temp_unitid = int(os.environ.get("TEMP_UNITID"))
ecowitt_wind_speed_unitid = int(os.environ.get("WIND_SPEED_UNITID"))

try:
    ecowitt = ecowitt.api.Ecowitt(
        application_key=ecowitt_application_key,
        api_key=ecowitt_api_key,
        mac=ecowitt_mac,
        temp_unitid=ecowitt_temp_unitid,
        wind_speed_unitid=ecowitt_wind_speed_unitid,
    )
    
    print("Testing device history API...")
    
    # Test with default parameters (last 24 hours)
    history_data = ecowitt.get_device_history()
    print(f"History data retrieved successfully: {len(history_data) if isinstance(history_data, list) else 'Data available'}")
    
    # Test with specific date range
    history_data_custom = ecowitt.get_device_history(
        start_date="2025-08-05",
        end_date="2025-08-06"
    )
    print(f"Custom range history data retrieved: {len(history_data_custom) if isinstance(history_data_custom, list) else 'Data available'}")
    
except Exception as e:
    print(f"Error testing history API: {e}")