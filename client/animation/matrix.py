#!/usr/bin/env python3
"""! Animation showing the Matrix rain animation."""
import random
import string
import numpy as np
from src.animate import Animate
from src.text import Text


class Matrix(Animate):
    """! Animation showing the Matrix rain.
    @image html matrix.Matrix.gif width=256px
    Animation showing ranomly generated ASCII characters falling like the Matrix rain.
    """

    __columns = []

    class Column:
        """! Matrix rain column.
        One column instance of the Matrix rain animation.
        """

        __TRACE = (3, 32)
        __SPEED_MIN = 0.2
        __tick = 1
        __string = ""

        def __init__(
            self,
            characters: str,
            offset_column: int,
            font: Text,
            font_size: tuple,
        ):
            """! Constructor.
            @param characters Allowable characters in the column.
            @param offset_column Column offset in pixels from the left.
            @param font Text font.
            @param font_size Text font size.
            """
            self.__characters = characters
            self.__font = font
            self.__offsets = (offset_column * font_size[0], font_size[1])
            self.__trace = self.__get_trace()
            self.__speed = self.__get_speed()

        def __get_speed(self) -> float:
            return random.random() * (1 - self.__SPEED_MIN) + self.__SPEED_MIN

        def __get_trace(self) -> int:
            return random.randint(self.__TRACE[0], self.__TRACE[1])

        def animate(self):
            """! Update the Matrix rain column data."""
            self.__tick -= 0.1
            if self.__tick <= self.__speed:
                self.__tick = 1
            else:
                return

            self.__string += random.choice(self.__characters)
            if len(self.__string) > self.__trace:
                self.__string = ""
                self.__trace = self.__get_trace()
                self.__speed = self.__get_speed()

        def draw(self, screen: np.ndarray):
            """! Draw the Matrix rain column on a provided canvas.
            @param screen Instance of the canvas to draw on.
            """
            for row, letter in enumerate(self.__string):
                green = len(self.__string) - row - 1
                if green == 0:
                    color = (0xFF, 0xFF, 0xFF)
                    letter = random.choice(self.__characters)
                else:
                    color = (0x00, (0b111 - green) << 5, 0x00)

                self.__font.write(
                    screen,
                    letter,
                    color=color,
                    offset=(
                        self.__offsets[0],
                        row * self.__offsets[1],
                    ),
                )

    def __init__(self, shape: tuple, *args: list, **kwargs: dict):
        super().__init__(shape)
        fontpath = "client/font/small_5x3.ttf"
        fontsize = 8
        self.__text = Text(fontpath, fontsize)
        font_size = (4, 6)
        characters = string.printable if kwargs["text"] == "" else kwargs["text"]

        for offset_column in range(shape[0] // font_size[0]):
            self.__columns.append(
                self.Column(characters, offset_column, self.__text, font_size)
            )

    def draw(self):
        self._screen[:] = 0
        for column in self.__columns:
            column.animate()
            column.draw(self._screen)
        yield self._screen
