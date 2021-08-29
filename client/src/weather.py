#!/usr/bin/env python3
"""! Obtain weather information script."""
import logging
import requests


class Weather:
    """! Obtain weather information class."""
    def __init__(self, key: str, location: str):
        """! Constructor.
        @param key The OpenWeatherMap API key.
        @param location Target location.
        """
        self.__key = key
        self.__location = location
        self.update()

    def update(self):
        """! Update weather data."""
        url = "https://api.openweathermap.org/data/2.5/weather?q=" \
            f"{self.__location}&units=metric&appid={self.__key}"
        req = requests.get(url)
        self.__weather = req.json()
        if not req.ok:
            logging.warning("[%s] %s", self.__class__.__name__, self.__weather['message'])

    @property
    def coordinates(self) -> (int, int):
        """! Return location coordinates in latitude/longitude.
        @return Location latitude and longitude.
        """
        latitude = self.__weather["coord"]["lat"] if "coord" in self.__weather else 0
        longitude = self.__weather["coord"]["lon"] if "coord" in self.__weather else 0
        return latitude, longitude

    @property
    def temperature(self):
        """! Return current temperature in degrees Celcius.
        @return Current tempereature.
        """
        temperature = self.__weather["main"]["temp"] if "main" in self.__weather else 0
        return temperature

    @property
    def humidity(self):
        """! Return current relative humidity in percent.
        @return Current humidity.
        """
        humidity = self.__weather["main"]["humidity"] if "main" in self.__weather else 0
        return humidity
