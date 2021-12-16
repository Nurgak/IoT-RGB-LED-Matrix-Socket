#!/usr/bin/env python3
"""! Local time object."""
import logging
from time import sleep
from threading import Thread
import pendulum


class Localtime(Thread):
    """! The local time class provides convenience functions for the various animations needing to
    keep time.

    The instance updates itself asychronously from the animation at the requested update rate. If
    the update rate is set to 0 the automatic update is disabled. This is useful when testing for a
    particular time.

    @sa https://docs.python.org/3/library/datetime.html
    """

    __time = None

    def __init__(self, timezone: str = "GMT", update_rate: float = 30.0):
        """! Constructor.
        @param timezone Timezone string, list of possible timezones.
        @param update_rate Rate at which the time is updated, in Hz.
        @sa https://en.wikipedia.org/wiki/List_of_tz_database_time_zones#List
        """
        super().__init__(target=self.__run, kwargs={"rate": update_rate}, daemon=True)
        self.__timezone = timezone

        self.update()
        if update_rate > 0:
            self.start()

        logging.debug("[%s] %s", self.__class__.__name__, self)

    def __str__(self) -> str:
        """! Return a string format of the time.
        @return Current time in ISO8601 format.
        """
        return self.__time.to_iso8601_string()

    def __run(self, **kwargs):
        while True:
            sleep(1.0 / kwargs["rate"])
            self.update()  # pragma: no cover

    def update(self):
        """! Update the current time."""
        self.__time = pendulum.now(self.__timezone)

    def set_time(self, stamp: float):
        """! Set the instance time.
        @param stamp POSIX timestamp.
        """
        self.__time = pendulum.from_timestamp(stamp, tz=self.__timezone)

    @property
    def hour(self) -> int:
        """! Return the current hour.
        @return Current hour, in 24h format.
        """
        return self.__time.hour

    @property
    def minute(self) -> int:
        """! Return the current minute.
        @return Current minute, from  0 to 59.
        """
        return self.__time.minute

    @property
    def second(self) -> int:
        """! Return the current second.
        @return Current second, from 0 to 59.
        """
        return self.__time.second

    @property
    def millisecond(self) -> int:
        """! Return the current millisecond.
        @return Current millisecond, from 0 to 999.
        """
        return self.__time.microsecond // 1000

    @property
    def month(self) -> int:
        """! Return the current month.
        @return Current month, from 0 to 11.
        """
        return self.__time.month

    @property
    def day(self) -> int:
        """! Return the current day of the month.
        @return Current day of the month, from 0 to 31.
        """
        return self.__time.day

    @property
    def year(self) -> int:
        """! Return the current year.
        @return Current year, with 4 digits.
        """
        return self.__time.year

    @property
    def weekday(self) -> int:
        """! Return the current day of the week.
        @return Current day of the week, from 0 to 6, 0 representing Monday.
        """
        return self.__time.day_of_week
