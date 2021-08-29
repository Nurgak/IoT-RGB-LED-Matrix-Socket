#!/usr/bin/env python3
"""! Animation showing water ripples script."""
from time import sleep
import numpy as np
from src.animate import Animate


class Water(Animate):
    """! Animation showing water ripples class.
    @image html media/Water.gif "Water animation example" width=256px
    Animation showing a randomly generated water drop ripples, inspired by
    https://web.archive.org/web/20160418004149/http://freespace.virgin.net/hugo.elias/graphics/x_water.htm
    and https://stackoverflow.com/a/60337269.
    """
    def __init__(self, shape: tuple, *args: list, **kwargs: dict):
        """! Constructor.
        @param shape Screen shape: height, width and color channels, for example:
        <tt>(32, 32, 3)</tt>.
        @param args Non-Keyword Arguments, not used.
        @param kwargs Keyword Arguments, not used.
        """
        self.__shape = (shape[0], shape[1], 2)
        self.__screen = np.zeros(shape, dtype=np.uint8)
        self.__water = np.zeros(self.__shape, dtype=np.float)
        self.__damping = 0.9
        self.drop()

    def drop(self, value: float=20.0):
        """! Add a random drop on the screen.
        @param value The value to add at a random position on the screen. A
        higher value will create a drop with more ripples.
        """
        random_x = np.random.randint(1, self.__shape[1] - 1)
        random_y = np.random.randint(1, self.__shape[0] - 1)
        self.__water[random_y, random_x, 0] = value

    def draw(self):
        """! Draw one frame of the animation."""
        self.__water[1:self.__shape[1]-1, 1:self.__shape[0]-1, 0] = ((
            self.__water[0:self.__shape[1]-2, 0:self.__shape[0]-2, 1] +
            self.__water[2:self.__shape[1], 0:self.__shape[0]-2, 1] +
            self.__water[0:self.__shape[1]-2, 2:self.__shape[0], 1] +
            self.__water[2:self.__shape[1], 2:self.__shape[0], 1]
            ) / 2 - self.__water[1:self.__shape[1]-1, 1:self.__shape[0]-1, 0]) * self.__damping

        self.__water[:, :, [0, 1]] = self.__water[:, :, [1, 0]]
        self.__screen[:, :, 2] = self.__water[:, :, 0].astype(np.uint8)
        yield self.__screen

    def animate(self, client, rate):
        """! Execute the animation.
        @param client The instance which will be updated with the animation.
        @param rate The update rate of the animation in Hz.
        """
        last_drop = 0
        while True:
            if not last_drop:
                self.drop()
                last_drop = 10
            last_drop -= 1
            client.update(next(self.draw()))
            sleep(1.0 / rate)
