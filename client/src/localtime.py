#!/usr/bin/env python3
"""! Local time object."""
from datetime import datetime
import pytz

class Localtime:
    """! Local time class."""
    __time = None

    def __init__(self, timezone: str="GMT"):
        """! Constructor.
        @param timezone Timezone
        """
        self.__timezone = pytz.timezone(timezone)
        self.update()

    def update(self):
        """! Update the current time."""
        self.__time = datetime.now(self.__timezone)

    def set_time(self, stamp: float):
        """! Update the current time.
        @param stamp POSIX timestamp.
        """
        self.__time = datetime.fromtimestamp(stamp)
        print(self.__time)

    @property
    def hour(self) -> int:
        """! Return the current hour in 24h format.
        @return Current hour.
        """
        return self.__time.hour

    @property
    def minute(self) -> int:
        """! Return the current minute from  0 to 59.
        @return Current minute.
        """
        return self.__time.minute

    @property
    def second(self) -> int:
        """! Return the current second from 0 to 59.
        @return Current second.
        """
        return self.__time.second

    @property
    def millisecond(self) -> int:
        """! Return the current millisecond from 0 to 999.
        @return Current millisecond.
        """
        return self.__time.microsecond // 1000

    @property
    def month(self) -> int:
        """! Return the current month from 0 to 11.
        @return Current month.
        """
        return self.__time.month

    @property
    def day(self) -> int:
        """! Return the current day of the month from 0 to 31.
        @return Current day of the month.
        """
        return self.__time.day

    @property
    def year(self) -> int:
        """! Return the current year.
        @return Current year.
        """
        return self.__time.year

    @property
    def weekday(self) -> int:
        """! Return the current day of the week from 0 to 6, 0 representing
        Monday.
        @return Current day of the week.
        """
        return self.__time.weekday()
