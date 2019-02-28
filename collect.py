#!/usr/bin/env python3

import os
import logging
import time
from datetime import datetime
from netatmo import api

class App:
    netatmo_client = None

    def __init__(self, access_token=False):
        logging.basicConfig(level=logging.INFO, format="[%(asctime)s] %(levelname)s - %(message)s", datefmt='%Y-%m-%d %H:%M:%S')
        self.netatmo_client = api.Client(access_token)

    def dump_weather_data(self):
        data = self.netatmo_client.get_weather_data()["devices"][0]
        logging.info("Using device ID %s" % data["_id"])

        if not data["reachable"]:
            logging.warning("Device not reachable!")
            return

        for data_type in data["data_type"]:
            self.dump_data(data["module_name"], data["dashboard_data"][data_type], data_type, data["dashboard_data"]["time_utc"])

        for module in data["modules"]:
            for data_type in module["data_type"]:
                data_keys = []

                if data_type == "Wind":
                    data_keys.append("WindStrength")
                    data_keys.append("GustStrength")
                else:
                    data_keys.append(data_type)

                for data_key in data_keys:
                    value = module["dashboard_data"].get(data_key, "-")
                    self.dump_data(module["module_name"], value, data_key, module["dashboard_data"]["time_utc"])


    def dump_data(self, name, value, data_type, timestamp):
        symbol = {
            "Temperature": "°C",
            "CO2": "ppm",
            "Humidity": "%",
            "Noise": "dB",
            "Pressure": "mb",
            "Rain": "mm",
            "WindStrength": "km/h",
            "GustStrength": "km/h",
        }.get(data_type, "")

        data_name = {
            "WindStrength": "Wind",
            "GustStrength": "Wind Gust",
        }.get(data_type, data_type)

        logging.info("%s %s: %s %s" % (
            name,
            data_name,
            value,
            symbol)
        )

if __name__ == "__main__":
    app = App(os.getenv("ACCESS_TOKEN"))

    while (True):
        app.dump_weather_data()

        # wait 10mn before the next call
        logging.info("Sleeping for 10mn now...")
        time.sleep(600)
