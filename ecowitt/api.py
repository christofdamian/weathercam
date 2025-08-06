import requests
from datetime import datetime, timedelta

class Ecowitt:
    data = None
    history_data = None

    def __init__(self, application_key=None, api_key=None, mac=None, temp_unitid=2, wind_speed_unitid=7, call_back="all"):
	# see: https://doc.ecowitt.net/web/#/apiv3en?page_id=17
        self.application_key = application_key
        self.api_key = api_key
        self.mac = mac
        self.temp_unitid = temp_unitid
        self.wind_speed_unitid = wind_speed_unitid
        self.call_back = call_back

        response = requests.get(f"https://api.ecowitt.net/api/v3/device/real_time", params = {
            "application_key": application_key,
            "api_key": api_key,
            "mac": mac,
            "temp_unitid": temp_unitid,
            "wind_speed_unitid": wind_speed_unitid,
            "call_back": call_back,
        })
        self.data = response.json()["data"]

    def outdoor_temperature_value(self):
        return self.data["outdoor"]["temperature"]["value"]

    def outdoor_temperature_unit(self):
        return self.data["outdoor"]["temperature"]["unit"]

    def outdoor_humidity_value(self):
        return self.data["outdoor"]["humidity"]["value"]

    def outdoor_humidity_unit(self):
        return self.data["outdoor"]["humidity"]["unit"]

    def wind_speed_value(self):
        return self.data["wind"]["wind_speed"]["value"]

    def wind_speed_unit(self):
        return self.data["wind"]["wind_speed"]["unit"]

    def uvi_value(self):
        return self.data["solar_and_uvi"]["uvi"]["value"]

    def uvi_unit(self):
        return self.data["solar_and_uvi"]["uvi"]["unit"]

    def feels_like_temperature_value(self):
        return self.data["outdoor"]["feels_like"]["value"]

    def feels_like_temperature_unit(self):
        return self.data["outdoor"]["feels_like"]["unit"]

    def pressure_value(self):
        return self.data["pressure"]["relative"]["value"]

    def pressure_unit(self):
        return self.data["pressure"]["relative"]["unit"]

    def solar_value(self):
        return self.data["solar_and_uvi"]["solar"]["value"]

    def solar_unit(self):
        return self.data["solar_and_uvi"]["solar"]["unit"]

    def get_device_history(self, start_date=None, end_date=None, cycle_type="30min"):
        """
        Get device history data from Ecowitt API

        Args:
            start_date: Start date in YYYY-MM-DD format (defaults to 24 hours ago)
            end_date: End date in YYYY-MM-DD format (defaults to now)
            cycle_type: Data interval in minutes (default: 5)

        Returns:
            Dictionary containing historical weather data
        """
        if start_date is None:
            start_date = (datetime.now().replace(microsecond=0) - timedelta(days=7)).isoformat(' ')
        if end_date is None:
            end_date = datetime.now().replace(microsecond=0).isoformat(' ')


        # see: https://doc.ecowitt.net/web/#/apiv3en?page_id=19
        response = requests.get(f"https://api.ecowitt.net/api/v3/device/history", params = {
            "application_key": self.application_key,
            "api_key": self.api_key,
            "mac": self.mac,
            "start_date": start_date,
            "end_date": end_date,
            "cycle_type": cycle_type,
            "temp_unitid": self.temp_unitid,
            "wind_speed_unitid": self.wind_speed_unitid,
            "call_back": self.call_back,
        })

        if response.status_code == 200:
            self.history_data = response.json()["data"]
            return self.history_data
        else:
            raise Exception(f"API request failed with status {response.status_code}: {response.text}")

    def get_history_data(self):
        """
        Get the cached history data
        """
        return self.history_data
