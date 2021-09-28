#!/usr/bin/env python3
"""! Live fire animation."""
import cv2 as cv
import numpy as np
from src.animate import Animate


class Fire(Animate):
    """! Live fire animation class.
    @image html fire.Fire.gif width=256px
    Animation showing a randomly generated live fire.
    """
    __FIRE_HEIGHT_FACTOR = 1.2

    def __init__(self, shape: tuple, *args: list, **kwargs: dict):
        super().__init__(shape)
        self.__fire = np.zeros(shape=shape[0:2], dtype=np.uint8)

    def draw(self):
        # Bottom fire starter line is randomly generated.
        self.__fire[-1, :] = np.random.randint(
            0xff >> 1, 0xff, size=self.__fire.shape[1]
        )
        decay = np.random.randint(
            self.__fire.shape[0] / self.__FIRE_HEIGHT_FACTOR,
            size=self.__fire.shape
        )
        self.__fire[:-1] = np.clip(self.__fire[1:] - decay[1:], 0, 0xFF)
        self._screen = cv.applyColorMap(self.__fire, cv.COLORMAP_HOT)
        # Transform BGR to RGB, because of OpenCV conventions.
        self._screen = self._screen[:, :, ::-1]
        yield self._screen
