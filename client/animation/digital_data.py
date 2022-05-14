#!/usr/bin/env python3
"""! Digital data animation."""
from src.animate import Animate
from src.localtime import Localtime
from src.weather import Weather
from src.text import Text


class DigitalData(Animate):
    """! Digital data animation class.
    @image html digital_data.DigitalData.png width=256px
    Animation showing:
    @li Time in hours, minutes and seconds in 24h format.
    @li Month, with 3 letters.
    @li Day of the month, with 2 digits.
    @li Year, with 4 digits.
    @li Day of the week, with 3 letters.
    @li Temperature, in degrees Celcius
    @li Relative humidity, in percent.
    @li Air quality index (AQI), in qualitative 5-level system.

    To fit all this data on the 32x32 display a very small font is used: a 5x3
    pixel font, which is the smallest that remains easily readable.

    To configure the animation for local data pass the relevant keyword arguments:
    @arg @c key OpenWeatherMap API key.
    @arg @c city The city for which the temperature, humidy and AQI will be requested.
    @arg @c timezone Time timezone for which the time will be displayed.

    @sa #client::src::localtime::Localtime
    @sa #client::src::weather::Weather
    """

    def __init__(self, shape: tuple, *args: list, **kwargs: dict):
        super().__init__(shape)
        self.__fontpath = "client/font/small_5x3.ttf"
        self.__fontsize = 8

        self.__localtime = Localtime(timezone=kwargs["timezone"], update_rate=1.0)
        self.__weather = Weather(kwargs["key"], kwargs["city"])

    def draw(self):
        self._screen[:] = 0
        months = [
            "Jan",
            "Feb",
            "Mar",
            "Apr",
            "May",
            "Jun",
            "Jul",
            "Aug",
            "Sep",
            "Oct",
            "Nov",
            "Dec",
        ]
        weekdays = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        date_suffixes = ["th", "st", "nd", "rd"]

        date_suffix = date_suffixes[0]
        if self.__localtime.day % 10 in [1, 2, 3] and self.__localtime.day not in [
            11,
            12,
            13,
        ]:  # pragma: no cover
            date_suffix = date_suffixes[self.__localtime.day % 10]

        text = Text(self.__fontpath, self.__fontsize)

        text.write(
            self._screen,
            f"{self.__localtime.hour:02d}:{self.__localtime.minute:02d}:"
            f"{self.__localtime.second:02d}",
            color=(0xFF, 0xFF, 0xFF),
            offset=(3, -1),
        )
        text.write(
            self._screen,
            f"{months[self.__localtime.month - 1]}",
            color=(0xFF, 0xFF, 0xFF),
            offset=(0, 5),
        )
        text.write(
            self._screen,
            f"{self.__localtime.day}{date_suffix}",
            color=(0xFF, 0xFF, 0xFF),
            offset=(17, 5),
            wrap=Text.WRAP_NONE,
        )
        text.write(
            self._screen,
            f"{self.__localtime.year}",
            color=(0xFF, 0xFF, 0xFF),
            offset=(0, 11),
        )
        text.write(
            self._screen,
            weekdays[self.__localtime.weekday],
            color=(0xFF, 0xFF, 0xFF),
            offset=(19, 11),
            wrap=Text.WRAP_NONE,
        )
        text.write(
            self._screen,
            f"{self.__weather.temperature:3.0f}C{self.__weather.humidity:3.0f}%",
            color=(0xFF, 0xFF, 0xFF),
            offset=(0, 17),
            wrap=Text.WRAP_NONE,
        )
        text.write(
            self._screen,
            f"AQI {self.__weather.aqi_text}",
            color=(0xFF, 0xFF, 0xFF),
            offset=(0, 23),
        )
        yield self._screen
