#!/usr/bin/env python3
"""! Obtain weather information script."""
from time import sleep
from threading import Thread
import logging
import numpy as np
import requests


class Weather(Thread):
    """! Fetches weather data from OpenWeatherMap API, when provided with a valid key.

    @pre This script requires one to have an account with OpenWeatherMap and provide the API key so
    it can fetch the data.

    The update rate can be set when instantizing the class, by default it is set to 5 minutes. The
    API allows up to 60 calls/minute and 1 million calls/month, on the free plan. With a 5 minute
    interval these thresholds are never reached.

    @note There are two separate calls: one for the weather and another for the air quality.

    @sa https://openweathermap.org
    @sa https://openweathermap.org/api/air-pollution
    """
    __weather = []
    __air_pollution = []

    def __init__(
        self,
        key: str,
        location: str,
        update_delay: int = 5 * 60,
    ):
        """! Constructor.
        @param key The OpenWeatherMap API key.
        @param location Location name, e.g. @c Tokyo.
        @param update_delay Time between update requests, in seconds.
        """
        super().__init__(target=self.__run, kwargs={"delay": update_delay}, daemon=True)

        self.__key = key
        self.__location = location

        if self.update():
            self.start()

        logging.debug("[%s] %s", self.__class__.__name__, self)

    def __str__(self) -> str:
        """! Return a string format of the weather information.
        @return Current weather and air pollution JSON arrays.
        """
        return f"{self.__weather}, {self.__air_pollution}"

    def __run(self, **kwargs):
        while True:
            sleep(kwargs["delay"])
            self.update()  # pragma: no cover

    def update(self) -> bool:
        """! Update weather and air pollution data.
        @return State of the update operation: @c True if successful, @c False
        otherwise.
        """
        success = True
        url = (
            "https://api.openweathermap.org/data/2.5/weather?q="
            f"{self.__location}&units=metric&appid={self.__key}"
        )
        try:
            req = requests.get(url)
        except requests.exceptions.SSLError as error:  # pragma: no cover
            success = False
            logging.error("[%s] %s", self.__class__.__name__, error)

        self.__weather = req.json()
        if not req.ok:
            success = False
            logging.warning(
                "[%s] %s", self.__class__.__name__, self.__weather["message"]
            )

        latitude = self.__weather["coord"]["lat"] if "coord" in self.__weather else 0
        longitude = self.__weather["coord"]["lon"] if "coord" in self.__weather else 0

        url = (
            "https://api.openweathermap.org/data/2.5/air_pollution?lat="
            f"{latitude}&lon={longitude}&units=metric&appid={self.__key}"
        )
        try:
            req = requests.get(url)
        except requests.exceptions.SSLError as error:  # pragma: no cover
            success = False
            logging.error("[%s] %s", self.__class__.__name__, error)

        self.__air_pollution = req.json()
        if not req.ok:
            success = False
            logging.warning(
                "[%s] %s", self.__class__.__name__, self.__air_pollution["message"]
            )

        return success

    @property
    def temperature(self) -> float:
        """! Return current temperature for the configured location.
        @return Tempereature in degrees Celcius, or `np.nan` if unknown.
        """
        return self.__weather["main"]["temp"] if "main" in self.__weather else np.nan

    @property
    def humidity(self) -> float:
        """! Return current relative humidity for the configured location.
        @return Relative humidity in percent, from 0 to 100, or `np.nan` if unknown.
        """
        return self.__weather["main"]["humidity"] if "main" in self.__weather else np.nan

    @property
    def aqi(self) -> int:
        """! Return the air quality index for the configured location.
        Possible values range from 0-5:
        @arg @c 0 Unknown.
        @arg @c 1 Good.
        @arg @c 2 Fair.
        @arg @c 3 Moderate.
        @arg @c 4 Poor.
        @arg @c 5 Very Poor.

        @return The air quality index from 0 to 5.

        @sa https://openweathermap.org/api/air-pollution#fields
        @sa https://en.wikipedia.org/wiki/Air_quality_index#CAQI
        """
        return (
            self.__air_pollution["list"][0]["main"]["aqi"]
            if "list" in self.__air_pollution
            else 0
        )

    @property
    def aqi_text(self) -> str:
        """! Return the air quality as text for the configured location.
        @return The air quality as a qualitative text:
        @arg @c N/A.
        @arg @c Good
        @arg @c Fair
        @arg @c Mod.
        @arg @c Poor
        @arg @c Bad

        @sa aqi
        """
        return ["N/A", "Good", "Fair", "Mod.", "Poor", "Bad"][self.aqi]
