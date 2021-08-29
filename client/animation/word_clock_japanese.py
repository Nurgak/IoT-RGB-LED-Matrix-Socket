#!/usr/bin/env python3
"""! Japanese word clock animation."""
import numpy as np
from src.animate import Animate
from src.localtime import Localtime
from src.text import Text


class WordClockJapanese(Animate):
    """! Japanese word clock class.
    @image html media/WordClockJapanese.png "WordClockJapanese animation example" width=256px
    Animation generating time written in Japanese.
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
    def get_time(localtime):
        """! Get the requested time in Japanese.
        @return Time in Japanese.
        """
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

    def draw(self):
        """! Draw one frame of the animation."""
        self.__localtime.update()
        time_text = self.get_time(self.__localtime)
        screen = np.zeros(self.__shape, dtype=np.uint8)
        text = Text("./font/misaki_mincho.ttf", 8)
        text.write(screen, time_text, wrap=Text.WRAP_FORCE)
        yield screen
