import requests

class Ecowitt:
    data = None

    def __init__(self, application_key=None, api_key=None, mac=None, temp_unitid=2, wind_speed_unitid=7, call_back="all"):
	# see: https://doc.ecowitt.net/web/#/apiv3en?page_id=17
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
