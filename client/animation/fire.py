#!/usr/bin/env python3
"""! Live fire animation."""
import cv2 as cv
import numpy as np
from src.animate import Animate


class Fire(Animate):
    """! Live fire animation class.
    @image html media/Fire.gif "Fire animation example" width=256px
    Animation showing a randomly generated live fire.
    """
    def __init__(self, shape: tuple, *args: list, **kwargs: dict):
        """! Constructor.
        @param shape Screen shape: height, width and color channels, for example:
        <tt>(32, 32, 3)</tt>.
        @param args Non-Keyword Arguments, not used.
        @param kwargs Keyword Arguments, not used.
        """
        self.__fire = np.zeros(shape=shape[0:2], dtype=np.uint8)

    def draw(self):
        """! Draw one frame of the animation."""
        # Bottom fire starter line is randomly generated.
        self.__fire[-1, :] = np.random.randint(0xff >> 1, 0xff,
            size=self.__fire.shape[1])
        decay = np.random.randint(self.__fire.shape[0] / 1.2,
            size=self.__fire.shape)
        self.__fire[:-1] = np.clip(self.__fire[1:] - decay[1:], 0, 0xff)
        screen = cv.applyColorMap(self.__fire, cv.COLORMAP_HOT)
        # Transform BGR to RGB, because of OpenCV conventions.
        screen = screen[:, :, ::-1]
        yield screen
