#!/usr/bin/env python3
"""! Home animation."""
from random import choice
import numpy as np
from src.animate import Animate
from src.localtime import Localtime
from animation.digital_data import DigitalData
from animation.game_of_life import GameOfLifeFast
from animation.rgb import Mandelbrot, GrowingTree, HilbertCurve


class Home(Animate):
    """! Home animation class."""

    __burnin_init_flag = False
    __burnin_animation = None

    def __init__(self, shape: tuple, *args: list, **kwargs: dict):
        super().__init__(shape)
        self.__localtime = Localtime(timezone=kwargs["timezone"], update_rate=1.0)
        self.__digital_data = DigitalData(shape, *args, **kwargs)
        self.__blank = np.zeros_like(self._screen)

    def draw(self):
        if self.__localtime.second == 59 and self.__burnin_init_flag:
            # Reset the burn-in animation flag.
            self.__burnin_init_flag = False

        # elif self.__localtime.hour == 11 and \
        #    self.__localtime.minute >= 30 and \
        #    0 <= self.__localtime.second < 5:
        #     # Show that it is lunchtime for 5 seconds every minute
        #     # Image of food (meal)
        #     pass
        # elif self.__localtime.hour == 12 and \
        #    self.__localtime.minute < 30 and \
        #    0 <= self.__localtime.second < 5:
        #     # Show that it is time to brush teeth for 5 seconds every minute
        #     # Image of teeth being brushed (toothbrush)
        #     frame = image_toothbrush.seek(
        #         (image_toothbrush.tell() + 1) % image_toothbrush.n_frames
        #     )
        #     screen = cv.resize(frame, self.__shape[0:2])
        # elif self.__localtime.hour == 12 and \
        #    self.__localtime.minute >= 30 and \
        #    0 <= self.__localtime.second < 5:
        #     # Show that it is time for a nap for 5 seconds every minute
        #     # Image of nap time (bed)
        #     pass
        # elif self.__localtime.hour == 20 and \
        #    self.__localtime.minute < 30 and \
        #    0 <= self.__localtime.second < 5:
        #     # Show that it is time for a shower for 5 seconds every minute
        #     # Image of shower time (water)
        #     pass
        # elif self.__localtime.hour == 20 and \
        #    self.__localtime.minute < 45 and \
        #    0 <= self.__localtime.second < 5:
        #     # Show that it is time to brush teeth for 5 seconds every minute
        #     # Image of teeth being brushed (toothbrush)
        #     pass
        # elif self.__localtime.hour == 20 and \
        #    self.__localtime.minute >= 45 and \
        #    0 <= self.__localtime.second < 5:
        #     # Show that it is time for bed for 5 seconds every minute
        #     # Image of bed time (moon)
        #     pass

        # if self.__localtime.hour == 7 and \
        #    self.__localtime.minute >= 45 and \
        #    0 <= self.__localtime.second < 5:
        #     # Show that it is time to go to school for 5 seconds every minute
        #     # Image of school (bicycle)
        #     pass
        if self.__localtime.hour >= 22 or self.__localtime.hour < 6:
            # Turn off the display from 22 to 6 o'clock.
            self._screen = self.__blank
        elif 0 <= self.__localtime.second < 5:
            # Avoid burn-in by randomly toggling pixels.
            # self._screen = np.random.randint(0, 0xff >> 2, size=self._screen.shape,
            #     dtype=np.uint8)

            # Run the game of life.
            if not self.__burnin_init_flag:
                # Initialize the animation screen.
                self.__burnin_animation = choice(
                    [
                        GameOfLifeFast(self._screen.shape),
                        Mandelbrot(self._screen.shape),
                        GrowingTree(self._screen.shape),
                        HilbertCurve(self._screen.shape),
                    ]
                )
                self.__burnin_init_flag = True

            self._screen = next(self.__burnin_animation.draw(), self.__blank)
        else:
            self._screen = next(self.__digital_data.draw(), self.__blank)

        # Limit brightness during the night.
        if self.__localtime.hour >= 20 or self.__localtime.hour <= 6:
            self._screen = np.clip(self._screen, 0, 0xFF >> 2)
        yield self._screen
