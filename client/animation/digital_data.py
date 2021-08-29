#!/usr/bin/env python3
"""! Digital data animation."""
import numpy as np
from src.animate import Animate
from src.localtime import Localtime
from src.weather import Weather
from src.air_pollution import AirPollution
from src.text import Text


class DigitalData(Animate):
    """! Digital data animation class.
    @image html media/DigitalData.png "DigitalData animation example" width=256px
    Animation showing:
    @li Time in hours, minutes and seconds.
    @li Month.
    @li Day of the month.
    @li Year.
    @li Day of the week.
    @li Temperature.
    @li Humidity.
    @li Air quality index (AQI).

    To configure the animation for local data pass the relevant kewword arguments.
    """
    __updated_flag = True

    def __init__(self, shape: tuple, *args: list, **kwargs: dict):
        """! Constructor.
        @param shape Screen shape: height, width and color channels, for example:
        <tt>(32, 32, 3)</tt>.
        @param args Non-Keyword Arguments, not used.
        @param kwargs Keyword Arguments, takes @p timezone, @p city and
        OpenWeatherMap @p key as the arguments to set the correct local data.
        """
        self.__shape = shape
        self.__fontpath = "./font/small_5x3.ttf"
        self.__fontsize = 8

        self.__localtime = Localtime(timezone=kwargs["timezone"])
        self.__weather = Weather(kwargs["key"], kwargs["city"])
        latitude, longitude = self.__weather.coordinates
        self.__air_pollution = AirPollution(kwargs["key"], latitude=latitude,
            longitude=longitude)

    def draw(self):
        """! Draw one frame of the animation."""
        self.__localtime.update()

        if (self.__localtime.minute % 5) == 0 and not self.__updated_flag:  # pragma: no cover
            self.__weather.update()
            self.__air_pollution.update()
            self.__updated_flag = True
        elif (self.__localtime.minute % 5) != 0 and self.__updated_flag:  # pragma: no cover
            self.__updated_flag = False

        screen = np.zeros(shape=self.__shape, dtype=np.uint8)
        months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep",
            "Oct", "Nov", "Dec"]
        weekdays = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        date_suffixes = ["th", "st", "nd", "rd"]

        date_suffix = date_suffixes[0]
        if self.__localtime.day % 10 in [1, 2, 3] and \
           self.__localtime.day not in [11, 12, 13]:  # pragma: no cover
            date_suffix = date_suffixes[self.__localtime.day % 10]

        text = Text(self.__fontpath, self.__fontsize)

        text.write(screen, f"{self.__localtime.hour:02d}:"\
            f"{self.__localtime.minute:02d}:{self.__localtime.second:02d}",
            color=(0, 0xff, 0), offset=(3, -1))
        text.write(screen, f"{months[self.__localtime.month - 1]} " \
            f"{self.__localtime.day}{date_suffix}",
            color=(0xff, 0, 0), offset=(0, 5))
        text.write(screen, f"{self.__localtime.year}", color=(0xff, 0, 0xff),
            offset=(0, 11))
        text.write(screen, f"{weekdays[self.__localtime.weekday]}",
            color=(0, 0, 0xff), offset=(19, 11),
            wrap=Text.WRAP_NONE)
        text.write(screen, f"{self.__weather.temperature:3.0f}C" \
            f"{self.__weather.humidity:3.0f}%", color=(0, 0xff, 0xff),
            offset=(0, 17), wrap=Text.WRAP_NONE)
        text.write(screen, f"AQI {self.__air_pollution.aqi}",
            color=(0xff, 0xff, 0), offset=(0, 23))
        yield screen
