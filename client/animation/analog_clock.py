#!/usr/bin/env python3
"""! Analog clock animation."""
import cv2 as cv
import numpy as np
from src.localtime import Localtime
from src.animate import Animate


class AnalogClock(Animate):
    """! Analog clock animation class.
    @image html media/AnalogClock.png "AnalogClock animation example" width=256px
    Animation showing the time on with hour, minute and second hands in red,
    green and blue respecivelty. The center pixels are masked to avoid burn-in
    when the animation is displayed for long time.
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
        self.__color = {
            "background": (0x00, 0x00, 0x00),
            "hour": (0xff, 0x00, 0x00),
            "minute": (0x00, 0xff, 0x00),
            "second": (0x00, 0x00, 0xff)
        }

    def draw(self):
        """! Draw one frame of the animation."""
        self.__localtime.update()
        screen = np.full(self.__shape, self.__color["background"], np.uint8)
        center = (int(screen.shape[0] / 2), int(screen.shape[1] / 2))

        # Configure the second hand.
        hand_second = max(screen.shape[1], screen.shape[0]) * 100
        fraction_millisecond = self.__localtime.millisecond / 1000.0
        fraction_second = (self.__localtime.second + fraction_millisecond) / 60.0
        angle_second = fraction_second * 2 * np.pi - np.pi / 2

        # Configure the minute hand.
        hand_minute = max(screen.shape[1], screen.shape[0]) * 100
        fraction_minute = (self.__localtime.minute + fraction_second) / 60.0
        angle_minute = fraction_minute * 2 * np.pi - np.pi / 2

        # Configure the hour hand.
        hand_hour = max(screen.shape[1], screen.shape[0]) * 100
        fraction_hour = (self.__localtime.hour + fraction_minute) / 12.0
        angle_hour = fraction_hour * 2 * np.pi - np.pi / 2

        # Draw the second hand.
        end_x = int(hand_second * np.cos(angle_second) + center[0])
        end_y = int(hand_second * np.sin(angle_second) + center[1])
        screen = cv.line(screen, center, (end_x, end_y),
            color=self.__color["second"], thickness=1, lineType=cv.LINE_AA)

        # Draw the minute hand.
        end_x = int(hand_minute * np.cos(angle_minute) + center[0])
        end_y = int(hand_minute * np.sin(angle_minute) + center[1])
        screen = cv.line(screen, center, (end_x, end_y),
            color=self.__color["minute"], thickness=1, lineType=cv.LINE_AA)

        # Draw the hour hand.
        end_x = int(hand_hour * np.cos(angle_hour) + center[0])
        end_y = int(hand_hour * np.sin(angle_hour) + center[1])
        screen = cv.line(screen, center, (end_x, end_y),
            color=self.__color["hour"], thickness=1, lineType=cv.LINE_AA)

        # Prevent burn-in with the center always having the same color.
        screen = cv.line(screen, center, center,
            color=(0, 0, 0), thickness=3)

        yield screen
