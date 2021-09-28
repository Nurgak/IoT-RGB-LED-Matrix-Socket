#!/usr/bin/env python3
"""! Analog clock animation."""
import cv2 as cv
import numpy as np
from src.localtime import Localtime
from src.animate import Animate


class AnalogClock(Animate):
    """! Analog clock animation class.
    @image html analog_clock.AnalogClock.gif width=256px
    Animation showing the time on with hour, minute and second hands in red, green and blue
    respectively. The center pixels are masked to avoid burn-in when the animation is displayed for
    long time.
    The time hands are much larger than the display itself, that is because the coordinates of the
    end of a hand are rounded to an integer, if they lie within the display the movement will be
    very discrete and visible, defeating the purpose of the anti-aliasing. Setting the end
    coordinates way outside the display allow to have more subtle pixel changes, resulting in a
    smoother animation.
    """

    def __init__(self, shape: tuple, *args: list, **kwargs: dict):
        super().__init__(shape)
        self.__localtime = Localtime(timezone=kwargs["timezone"], update_rate=30.0)

    def __get_angles(self):
        # Configure the second hand.
        fraction_millisecond = self.__localtime.millisecond / 1000.0
        fraction_second = (self.__localtime.second + fraction_millisecond) / 60.0
        angle_second = fraction_second * 2 * np.pi - np.pi / 2

        # Configure the minute hand.
        fraction_minute = (self.__localtime.minute + fraction_second) / 60.0
        angle_minute = fraction_minute * 2 * np.pi - np.pi / 2

        # Configure the hour hand.
        fraction_hour = (self.__localtime.hour + fraction_minute) / 12.0
        angle_hour = fraction_hour * 2 * np.pi - np.pi / 2

        return angle_second, angle_minute, angle_hour

    def draw(self):
        self._screen[:] = 0
        center = (self._screen.shape[0] // 2, self._screen.shape[1] // 2)
        # Hand size must be large for the line end position to change even for
        # small angles, which is then rounded to integers.
        hand_size = max(self._screen.shape[1], self._screen.shape[0]) * 100

        angle_second, angle_minute, angle_hour = self.__get_angles()

        # Draw the second hand.
        end_x = int(hand_size * np.cos(angle_second) + center[0])
        end_y = int(hand_size * np.sin(angle_second) + center[1])
        screen_second = self._screen.copy()
        screen_second = cv.line(
            screen_second,
            center,
            (end_x, end_y),
            color=(0xFF, 0xFF, 0xFF),
            thickness=1,
            lineType=cv.LINE_AA,
        )

        # Draw the minute hand.
        end_x = int(hand_size * np.cos(angle_minute) + center[0])
        end_y = int(hand_size * np.sin(angle_minute) + center[1])
        screen_minute = self._screen.copy()
        screen_minute = cv.line(
            screen_minute,
            center,
            (end_x, end_y),
            color=(0xFF, 0xFF, 0xFF),
            thickness=1,
            lineType=cv.LINE_AA,
        )

        # Draw the hour hand.
        end_x = int(hand_size * np.cos(angle_hour) + center[0])
        end_y = int(hand_size * np.sin(angle_hour) + center[1])
        screen_hour = self._screen.copy()
        screen_hour = cv.line(
            screen_hour,
            center,
            (end_x, end_y),
            color=(0xFF, 0xFF, 0xFF),
            thickness=1,
            lineType=cv.LINE_AA,
        )

        self._screen[:, :, 0] = screen_hour[:, :, 0]
        self._screen[:, :, 1] = screen_minute[:, :, 1]
        self._screen[:, :, 2] = screen_second[:, :, 2]

        # Prevent burn-in with the center by setting it to black.
        self._screen = cv.line(
            self._screen, center, center, color=(0, 0, 0), thickness=3
        )

        yield self._screen
