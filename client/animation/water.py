#!/usr/bin/env python3
"""! Animation showing water ripples script."""
import numpy as np
from src.animate import Animate


class Water(Animate):
    """! Animation showing water ripples.
    @image html water.Water.gif width=256px
    Animation showing a randomly generated water drop ripples. The animation creates a new drop in a
    random position every 10 frames.

    @sa https://stackoverflow.com/a/60337269
    """

    __DROP_EVERY_N_FRAMES = 10
    __DAMPING = 0.9
    __drop_frame_count = 0

    def __init__(self, shape: tuple, *args: list, **kwargs: dict):
        super().__init__(shape)
        self.__shape = (shape[0], shape[1], 2)
        self.__water = np.zeros(self.__shape, dtype=np.float)

    def draw(self):
        if self.__drop_frame_count <= 0:
            pos_y, pos_x = np.random.randint(self.__shape[0:2])
            self.__water[pos_y, pos_x, 0] = 20.0
            self.__drop_frame_count = self.__DROP_EVERY_N_FRAMES
        self.__drop_frame_count -= 1

        self.__water[1 : self.__shape[1] - 1, 1 : self.__shape[0] - 1, 0] = (
            (
                self.__water[0 : self.__shape[1] - 2, 0 : self.__shape[0] - 2, 1]
                + self.__water[2 : self.__shape[1], 0 : self.__shape[0] - 2, 1]
                + self.__water[0 : self.__shape[1] - 2, 2 : self.__shape[0], 1]
                + self.__water[2 : self.__shape[1], 2 : self.__shape[0], 1]
            )
            / 2
            - self.__water[1 : self.__shape[1] - 1, 1 : self.__shape[0] - 1, 0]
        ) * self.__DAMPING

        self.__water[:, :, [0, 1]] = self.__water[:, :, [1, 0]]
        self._screen[:, :, 2] = self.__water[:, :, 0].astype(np.uint8)
        yield self._screen
