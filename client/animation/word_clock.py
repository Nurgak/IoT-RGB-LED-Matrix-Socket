#!/usr/bin/env python3
"""! Word clock animations."""
from abc import ABC, abstractmethod
from src.animate import Animate
from src.localtime import Localtime
from src.text import Text


class WordClock(Animate, ABC):
    """! Word clock abstract animation class."""

    def __init__(self, shape: tuple, *args: list, **kwargs: dict):
        super().__init__(shape)
        self.__font = kwargs["font"]
        self.__size = kwargs["size"]
        self.__wrap = kwargs["wrap"]
        self.__localtime = Localtime(timezone=kwargs["timezone"], update_rate=1.0)

    @abstractmethod
    def get_time(self, localtime: object) -> str:  # pragma: no cover
        """! @pure Get the requested time in written characters.
        @return Time in written characters.
        """

    def draw(self):
        time_text = self.get_time(self.__localtime)
        self._screen[:] = 0
        text = Text(self.__font, self.__size)
        text.write(self._screen, time_text, wrap=self.__wrap)
        yield self._screen


class English(WordClock):
    """! English word clock class.
    @image html word_clock.English.png width=256px
    Animation generating time written in English, using a tiny 5x3 pixel font.

    @sa https://fontsup.com/font/small-5x3-regular.html
    """

    def __init__(self, shape: tuple, *args: list, **kwargs: dict):
        kwargs["font"] = "client/font/small_5x3.ttf"
        kwargs["size"] = 8
        kwargs["wrap"] = Text.WRAP_NORMAL
        super().__init__(shape, *args, **kwargs)

    def __get_word(self, number: int):
        assert 0 < number <= 30, f"Number {number} out of range ]0, 30]."
        numbers = [
            0,
            "one",
            "two",
            "three",
            "four",
            "five",
            "six",
            "seven",
            "eight",
            "nine",
            "ten",
            "eleven",
            "twelve",
            "thirteen",
            "fourteen",
            "quarter",
            "sixteen",
            "seventeen",
            "eighteen",
            "nineteen",
            "twenty",
        ]
        if 0 < number <= 20:
            text = numbers[number]
        elif 20 < number < 30:
            text = f"twenty {self.__get_word(number - 20)}"
        else:
            text = "half"
        return text

    def get_time(self, localtime: object):
        hour = localtime.hour if localtime.hour < 13 else localtime.hour - 12
        if hour == 0:
            hour = 12

        output = "It is "
        if localtime.minute == 0 and localtime.hour == 0:
            output += "midnight"
        elif localtime.minute == 0 and localtime.hour == 12:
            output += "midday"
        elif localtime.minute == 0:
            output += f"{self.__get_word(hour)} o'clock"
        elif localtime.minute <= 30:
            output += (
                f"{self.__get_word(localtime.minute)} past " f"{self.__get_word(hour)}"
            )
        else:
            hour = hour + 1 if hour < 12 else 1
            output += (
                f"{self.__get_word(60 - localtime.minute)} to "
                f"{self.__get_word(hour)}"
            )
        return output


class Japanese(WordClock):
    """! Japanese word clock class.
    @image html word_clock.Japanese.png width=256px
    Animation generating time written in Japanese Kanji, using a tiny 8x8 pixel font.

    @sa https://littlelimit.net/misaki.htm
    """

    def __init__(self, shape: tuple, *args: list, **kwargs: dict):
        kwargs["font"] = "client/font/misaki_mincho.ttf"
        kwargs["size"] = 8
        kwargs["wrap"] = Text.WRAP_FORCE
        super().__init__(shape, *args, **kwargs)

    def get_time(self, localtime: object) -> str:
        kanji = ["", "一", "二", "三", "四", "五", "六", "七", "八", "九", "十", "十一", "十二"]

        ampm = "午後" if localtime.hour > 12 else "午前"

        if localtime.hour == 0:
            hour = kanji[12]
        else:
            hour = kanji[(localtime.hour % 12)]

        minute = ""
        if localtime.minute == 30:
            minute = "半"
        elif localtime.minute > 0:
            minute = kanji[localtime.minute % 10] + "分"
            if localtime.minute >= 10:
                minute = "十" + minute
                if localtime.minute >= 20:
                    minute = kanji[localtime.minute // 10] + minute

        return f"今は{ampm}{hour}時{minute}です"
