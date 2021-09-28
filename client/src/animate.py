#!/usr/bin/env python3
"""! Abstract animation script."""
from abc import ABC, abstractmethod
from typing import Generator
from time import sleep
import numpy as np


class Animate(ABC):
    """! Main animation class."""

    def __init__(self, shape: tuple, *args: list, **kwargs: dict):
        """! Constructor.
        @param shape Screen shape: height, width and color channels, for example:
        <tt>(32, 32, 3)</tt>.
        @param args Non-Keyword Arguments.
        @param kwargs Keyword Arguments.
        """
        self._screen = np.zeros(shape=shape, dtype=np.uint8)

    def __del__(self):
        """! Destructor, release the used resources."""
        del self._screen

    @abstractmethod
    def draw(self) -> Generator[np.ndarray, None, None]:  # pragma: no cover
        """! @pure Generate one frame of the animation.
        @return Screen generator.
        """

    def animate(self, client: object, update_rate: float = 30.0):
        """! Execute the animation.
        @param client The instance which will be updated with the animation.
        @param update_rate The update rate of the animation, in Hz.
        """
        while True:
            client.update(next(self.draw()))
            sleep(1.0 / update_rate)
