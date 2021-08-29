#!/usr/bin/env python3
"""! Maze generator animation script."""
from time import sleep
import numpy as np
from src.animate import Animate


class MazeGrowingTree(Animate):
    """! Maze generator animation class.
    @image html media/MazeGrowingTree.gif "MazeGrowingTree animation example" width=256px
    Recursive animation showing a maze being generated using the growing tree
    algorithm, inspired from
    https://weblog.jamisbuck.org/2011/1/27/maze-generation-growing-tree-algorithm.
    The forward pass is displayed in in green while the backwards pass is red.
    At the end of the animation the screen resets and starts over from a random
    position.
    """
    __DIRECTIONS = np.array([[-1, 0], [1, 0], [0, -1], [0, 1]])

    def __init__(self, shape: tuple, *args: list, **kwargs: dict):
        """! Constructor.
        @param shape Screen shape: height, width and color channels, for example:
        <tt>(32, 32, 3)</tt>.
        @param args Non-Keyword Arguments, not used.
        @param kwargs Keyword Arguments, not used.
        """
        self.__screen = np.zeros(shape=shape, dtype=np.uint8)
        self.__color_forward = (0x00, 0xff, 0x00)
        self.__color_backward = (0xff, 0x00, 0x00)

    # pylint: disable=arguments-differ
    def draw(self, position: tuple=(0, 0)):
        """! Draw one frame of the animation.
        @param position Start position of the maze generator.
        """
        self.__screen[position[0], position[1], :] = self.__color_forward
        yield self.__screen

        allowed_moves = []
        for move in self.__DIRECTIONS:
            adjacent = position + move
            if 0 <= adjacent[1] < self.__screen.shape[1] and \
               0 <= adjacent[0] < self.__screen.shape[0] and \
               np.all(self.__screen[adjacent[0], adjacent[1], :] == 0):
                allowed_moves.append(list(move))

        for random_move in np.random.permutation(len(allowed_moves)):
            next_position = position + allowed_moves[random_move]
            yield from self.draw(next_position)

        self.__screen[position[0], position[1], :] = self.__color_backward
        yield self.__screen

    def animate(self, client: object, rate: int):
        """! Execute the animation.
        @param client The instance which will be updated with the animation.
        @param rate The update rate of the animation in Hz.
        """
        while True:
            self.__screen[:] = 0
            start = np.random.randint(self.__screen.shape[0:2])
            for screen in self.draw(start):  # pragma: no cover
                client.update(screen)
                sleep(1.0 / rate)
