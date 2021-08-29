#!/usr/bin/env python3
"""! Air pollution fetching script."""
import logging
import requests


class AirPollution:
    """! Air pollution class."""
    def __init__(self, key: str, latitude: float, longitude: float):
        """! Constructor.
        @param key The OpenWeatherMap API key.
        @param latitude Target location latitude.
        @param longitude Target location longitude.
        """
        self.__key = key
        self.__lat = latitude
        self.__lon = longitude
        self.update()

    def update(self):
        """! Update air pollution values."""
        url = "https://api.openweathermap.org/data/2.5/air_pollution?lat=" \
            f"{self.__lat}&lon={self.__lon}&units=metric&appid={self.__key}"
        req = requests.get(url)
        self.__air_pollution = req.json()
        if not req.ok:
            logging.warning("[%s] %s", self.__class__.__name__, self.__air_pollution['message'])

    @property
    def aqi(self) -> int:
        """! Return the air quality index.
        @return The air quality index from 1 to 5.
        """
        # Possible values: 1, 2, 3, 4, 5.
        # Where 1 = Good, 2 = Fair, 3 = Moderate, 4 = Poor, 5 = Very Poor.
        aqi = self.__air_pollution["list"][0]["main"]["aqi"] if \
            "list" in self.__air_pollution else 0
        return aqi
