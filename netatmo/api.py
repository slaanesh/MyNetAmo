import os
import logging
import requests
import json
import time

class Client:
    access_token = None
    access_token_end = 0
    refresh_token = None
    scope = None

    def __init__(self):
        self.get_tokens()

    def get_tokens(self, params=None):
        logging.info("fetch access token...")

        payload = {
            'client_id': os.getenv("CLIENT_ID"),
            'client_secret': os.getenv("CLIENT_SECRET")
        }

        if params:
            payload.update(params)
        else:
            payload.update({
                'grant_type': 'password',
                'username': os.getenv("USER"),
                'password': os.getenv("PASSWORD"),
                'scope': 'read_station'
            })

        try:
            response = requests.post("https://api.netatmo.com/oauth2/token", data=payload)
            response.raise_for_status()
            tokens = response.json()

            self.access_token_end = int(time.time()) + tokens['expires_in']
            self.access_token = tokens["access_token"]
            self.refresh_token = tokens["refresh_token"]
            self.scope = tokens["scope"]

            logging.info("Received access token: %s" % self.access_token)
            logging.info("Received refresh token: %s" % self.refresh_token)
        except requests.exceptions.HTTPError as error:
            logging.warning(error.response.text)

    def refresh_tokens(self):
        if time.time() >= self.access_token_end:
            logging.info("refreshing token...")
            params = {
                'grant_type': 'refresh_token',
                'refresh_token': self.refresh_token
            }
            self.get_tokens(params)

    def get_weather_data(self):
        logging.info("Get weather data...")

        self.refresh_tokens()

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

        self.refresh_tokens()

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
