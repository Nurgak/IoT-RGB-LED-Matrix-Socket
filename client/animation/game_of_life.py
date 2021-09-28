#!/usr/bin/env python3
"""! Conway's Game of Life animation."""
import cv2 as cv
import numpy as np
from src.animate import Animate


class GameOfLifeColor(Animate):
    """! Conway's Game of Life animation class, in color.
    @image html game_of_life.GameOfLifeColor.gif width=256px
    Iterative animation, generated based on the previous frame and simplisic
    rules, described in https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life#Rules,
    resulting in seemingly live beings. The first frame is generated randomly and
    the animation progresses from there. As the animation progresses it will
    eventually stall in either a static frame or a short loop. In this case
    it needs to be restarted.
    """

    def __init__(self, shape: tuple, *args: list, **kwargs: dict):
        super().__init__(shape)
        self._screen = np.random.randint(0xFF, size=shape, dtype=np.uint8)
        mask = np.random.randint(2, size=shape[0:2], dtype=np.uint8)
        self._screen[mask == 0] = (0, 0, 0)

    def draw(self):
        """! Draw one frame of the animation."""
        new_status = np.zeros_like(self._screen)
        for roll_y in range(0, self._screen.shape[0]):
            rolled_y = np.roll(self._screen, -roll_y + 1, axis=0)
            for roll_x in range(0, self._screen.shape[1]):
                rolled_yx = np.roll(rolled_y, -roll_x + 1, axis=1)

                neighbours = rolled_yx[0:3, 0:3]

                # Mask the center cell.
                neighbours[1, 1, :] = 0

                # Count the number of neighbours.
                neighbours_count = np.sum(np.any(neighbours, axis=-1))

                # Status of the current cell.
                cell_is_alive = np.any(self._screen[roll_y, roll_x])

                # Apply the game of life rules.
                new_cell_value = (0, 0, 0)
                if cell_is_alive and 2 <= neighbours_count <= 3:
                    # Color remains the same as cell does not die.
                    new_cell_value = self._screen[roll_y, roll_x]
                elif not cell_is_alive and neighbours_count == 3:
                    # New cell is born: take the average color of the three "parents".
                    # Saturate the colors to avoid fading out.
                    parents = neighbours[np.any(neighbours > 0, axis=-1)].reshape(
                        (-1, 3)
                    )
                    # Mutate if parents are too similar.
                    new_cell_value = (
                        np.random.randint(0xFF, size=3)
                        if np.std(parents, axis=0).max() < 1
                        else parents.mean(axis=0, dtype=np.uint8)
                    )

                new_status[roll_y, roll_x, :] = new_cell_value

        self._screen = new_status
        yield self._screen


class GameOfLifeFast(Animate):
    """! Conway's Game of Life animation class, optimized for execution speed.
    @image html game_of_life.GameOfLifeFast.gif width=256px
    Iterative animation, generated based on the previous frame and simplisic
    rules, described in https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life#Rules,
    resulting in seemingly live beings. The first frame is generated randomly and
    the animation progresses from there. As the animation progresses it will
    eventually stall in either a static frame or a short loop. In this case
    it needs to be restarted.
    """

    __KERNEL = kernel = np.array([[1, 1, 1], [1, 0, 1], [1, 1, 1]], dtype=np.uint8)

    def __init__(self, shape: tuple, *args: list, **kwargs: dict):
        super().__init__(shape)
        # Create a random binary image.
        self._screen = np.random.randint(2, size=shape[0:2], dtype=np.bool)

    def draw(self):
        """! Draw one frame of the animation."""
        # Create an agumented by 1 pixel, wrapped image from the screen.
        screen_augmented = cv.copyMakeBorder(
            self._screen.astype(np.uint8), 1, 1, 1, 1, cv.BORDER_WRAP
        )
        # Count the number of neighbours using the 2D filter and a 3x3 kernel.
        screen_filtered = cv.filter2D(
            screen_augmented, -1, GameOfLifeFast.__KERNEL, borderType=cv.BORDER_ISOLATED
        )
        # Crop the augmented image back to the original size.
        neighbours = screen_filtered[1:-1, 1:-1]
        # Apply the Conway's Game of Life rules.
        self._screen = ((self._screen == 1) & (neighbours >= 2) & (neighbours <= 3)) | (
            self._screen == 0
        ) & (neighbours == 3)
        # Yield a 3-channel screen by transforming the gray image to RGB.
        yield cv.cvtColor(self._screen.astype(np.uint8) * 0xFF, cv.COLOR_GRAY2RGB)
