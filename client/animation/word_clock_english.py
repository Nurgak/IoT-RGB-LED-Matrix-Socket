#!/usr/bin/env python3
"""! English word clock animation."""
import numpy as np
from src.animate import Animate
from src.localtime import Localtime
from src.text import Text


class WordClockEnglish(Animate):
    """! English word clock class.
    @image html media/WordClockEnglish.png "WordClockEnglish animation example" width=256px
    Animation generating time written in English.
    """
    def __init__(self, shape: tuple, *args: list, **kwargs: dict):
        """! Constructor.
        @param shape Screen shape: height, width and color channels, for example:
        <tt>(32, 32, 3)</tt>.
        @param args Non-Keyword Arguments, not used.
        @param kwargs Keyword Arguments, takes @p timezone as the argument to set
        the correct local time.
        """
        self.__shape = shape
        self.__localtime = Localtime(timezone=kwargs["timezone"])

    @staticmethod
    def __get_word(number):
        assert 0 < number < 60, f"Number {number} out of range ]0, 60[."
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
            "twenty"
        ]
        if 0 < number <= 20:
            text = numbers[number]
        elif 20 < number < 30:
            text = f"twenty {WordClockEnglish.__get_word(number - 20)}"
        else:
            text = "half"
        return text

    @staticmethod
    def get_time(localtime):
        """! Get the requested time in English.
        @return Time in English.
        """
        hour = localtime.hour if localtime.hour < 13 else localtime.hour - 12
        if hour == 0:
            hour = 12

        output = "It is "
        if localtime.minute == 0 and localtime.hour == 0:
            output += "midnight"
        elif localtime.minute == 0 and localtime.hour == 12:
            output += "midday"
        elif localtime.minute == 0:
            output += f"{WordClockEnglish.__get_word(hour)} o'clock"
        elif localtime.minute <= 30:
            output += f"{WordClockEnglish.__get_word(localtime.minute)} past " \
                f"{WordClockEnglish.__get_word(hour)}"
        else:
            hour = hour + 1 if hour < 12 else 1
            output += f"{WordClockEnglish.__get_word(60 - localtime.minute)} to " \
                f"{WordClockEnglish.__get_word(hour)}"
        return output

    def draw(self):
        """! Draw one frame of the animation."""
        time_text = self.get_time(self.__localtime)
        screen = np.zeros(self.__shape, dtype=np.uint8)
        text = Text("./font/small_5x3.ttf", 8)
        text.write(screen, time_text, wrap=Text.WRAP_NORMAL)
        yield screen
