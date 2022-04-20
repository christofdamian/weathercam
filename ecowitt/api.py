import requests

class Ecowitt:
    data = None

    def __init__(self, application_key=None, api_key=None, mac=None, temp_unitid=2, call_back="all"):
        response = requests.get(f"https://api.ecowitt.net/api/v3/device/real_time", params = {
            "application_key": application_key,
            "api_key": api_key,
            "mac": mac,
            "temp_unitid": temp_unitid,
            "call_back": call_back,
        })
        self.data = response.json()["data"]

    def outdoor_temperature_value(self):
        return self.data["outdoor"]["temperature"]["value"]
