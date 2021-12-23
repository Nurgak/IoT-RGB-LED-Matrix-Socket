#!/usr/bin/env python3
"""! Animation showing falling snow script."""
import cv2 as cv
import numpy as np
from src.animate import Animate


class Snow(Animate):
    """! Animation showing falling snow.
    @image html snow.Snow.gif width=256px
    Animation showing a randomly generated falling snowflakes.
    """

    def __init__(self, shape: tuple, *args: list, **kwargs: dict):
        super().__init__(shape)
        self.__snow = np.zeros(shape[0:2], dtype=np.uint8)

    def draw(self):
        self.__snow[1:, :] = self.__snow[0:-1, :]
        self.__snow[0, :] = (
            np.random.random(size=self._screen.shape[1]) < np.random.random() * 0.1
        )
        yield cv.cvtColor((self.__snow) * 0xFF, cv.COLOR_GRAY2RGB)
