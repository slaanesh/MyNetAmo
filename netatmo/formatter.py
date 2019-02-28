def format_symbol(data_type):
    return {
        "Temperature": "°C",
        "CO2": "ppm",
        "Humidity": "%",
        "Noise": "dB",
        "Pressure": "mb",
        "Rain": "mm",
        "WindStrength": "km/h",
        "GustStrength": "km/h",
    }.get(data_type, "")

def format_name(data_type):
    return {
        "WindStrength": "Wind",
        "GustStrength": "Wind Gust",
    }.get(data_type, data_type)
