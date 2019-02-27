import os
import logging
import requests
import json

class Client:
    access_token = None
    refresh_token = None
    scope = None

    def __init__(self, access_token=False):
        self.access_token = access_token

        if not access_token:
            self.get_tokens()

    def get_tokens(self):
        logging.info("fetch access token...")

        payload = {'grant_type': 'password',
                   'username': os.getenv("USER"),
                   'password': os.getenv("PASSWORD"),
                   'client_id': os.getenv("CLIENT_ID"),
                   'client_secret': os.getenv("CLIENT_SECRET"),
                   'scope': 'read_station'}
        try:
            response = requests.post("https://api.netatmo.com/oauth2/token", data=payload)
            response.raise_for_status()
            tokens = response.json()
            self.access_token = tokens["access_token"]
            self.refresh_token = tokens["refresh_token"]
            self.scope = tokens["scope"]
            logging.info("Received access token: %s" % self.access_token)

        except requests.exceptions.HTTPError as error:
            logging.warning(error.response.text)

    def get_devices(self):
        logging.info("get devices...")

        params = {
            'access_token': self.access_token
        }
        try:
            response = requests.post("https://api.netatmo.com/api/devicelist", params=params)
            response.raise_for_status()
            data = response.json()["body"]
            json.dumps(data)
        except requests.exceptions.HTTPError as error:
            logging.warning(error.response.text)

    def get_weather_data(self):
        logging.info("Get weather data...")

        params = {
            'access_token': self.access_token
        }

        try:
            response = requests.post("https://api.netatmo.com/api/getstationsdata", params=params)
            response.raise_for_status()
            return response.json()["body"]
        except requests.exceptions.HTTPError as error:
            logging.warning(error.response.text)

    def get_thermostats_data(self):
        logging.info("get thermostats data...")

        params = {
            'access_token': self.access_token
        }

        try:
            response = requests.post("https://api.netatmo.com/api/getthermostatsdata", params=params)
            response.raise_for_status()
            data = response.json()["body"]
            json.dumps(data)
        except requests.exceptions.HTTPError as error:
            logging.warning(errorn.response.text)
