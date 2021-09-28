#!/usr/bin/env python3
"""! RGB animation scripts."""
import numpy as np
from hilbert import decode as HilbertDecode
from src.animate import Animate


class HilbertCurveGenerator:
    """! Hilbert curve generator helper class.
    Will loop the value when overflow occurs.
    """

    __index = 0

    def __init__(self, dimension: int, bits: int):
        """! Constructor.
        @param dimension Hilbert curve dimension.
        @param bits Bits in the Hilbert curve.
        """
        self.__hilberts = HilbertDecode(
            np.arange((2 ** dimension) ** bits), dimension, bits
        )

    def __next__(self) -> int:
        """! Returns the next Hilbert curve value in the configured list.
        @return The next Hilbert curve value.
        """
        value = self.get(self.__index)
        self.__index += 1
        return value

    def get(self, index: int) -> int:
        """! Returns the Hilbert curve value in the specified position.
        @return The Hilbert curve value at the specified index.
        """
        return self.__hilberts[index % len(self.__hilberts)]


class GrowingTree(Animate):
    """! Animation filling the screen with 3-bit Hilbert curve colors using the growing tree
    traversal algorithm.
    @image html rgb.GrowingTree.gif width=256px
    Recursive animation showing a maze being generated using the growing tree algorithm. The colors
    are generated from a Hilbert curve cube.

    @sa https://weblog.jamisbuck.org/2011/1/27/maze-generation-growing-tree-algorithm.
    @sa https://stackoverflow.com/questions/18395725/test-if-numpy-array-contains-only-zeros
    """

    __DIRECTIONS = np.array([[-1, 0], [1, 0], [0, -1], [0, 1]])

    def __init__(self, shape: tuple, *args: list, **kwargs: dict):
        super().__init__(shape)
        # 32*32=1024 positions do not perfectly map to a (2**3)**3=512 Hilbert
        # curve, so every color will be represented twice on a 32x32 matrix.
        self.__colors = HilbertCurveGenerator(dimension=3, bits=3)

        position_init = np.random.randint(self._screen.shape[0:2])
        self.__screen_generator = self.__explore(position_init)

    def draw(self):
        return self.__screen_generator

    def __explore(self, position: tuple):
        self._screen[position[0], position[1], :] = next(self.__colors, 0) << 5
        yield self._screen

        adjacent_pixels = position + self.__DIRECTIONS
        np.random.shuffle(adjacent_pixels)
        for pos_y, pos_x in adjacent_pixels:
            if (
                0 <= pos_y < self._screen.shape[0]
                and 0 <= pos_x < self._screen.shape[1]
                and not np.any(self._screen[pos_y, pos_x])
            ):
                yield from self.__explore((pos_y, pos_x))


class HilbertCurve(Animate):
    """! Animation filling a 32x32 pixel screen with 3-bit, 3D Hilbert curve colors using a 5-bit,
    2D Hilbert curve traversal.
    @image html rgb.HilbertCurve.gif width=256px

    @sa https://possiblywrong.wordpress.com/allrgb-hilbert-curves-and-random-spanning-trees/
    """

    def __init__(self, shape: tuple, *args: list, **kwargs: dict):
        super().__init__(shape)
        # 32*32 pixels=1024 positions perfectly map to a 2**2**5=1024 Hilbert curve.
        self.__position_generator = HilbertCurveGenerator(dimension=2, bits=5)
        # 32*32 pixels=1024 positions do not perfectly map to a (2**3)**3=512 Hilbert curve, so
        # every color will be represented twice on a 32x32 matrix.
        self.__color_generator = HilbertCurveGenerator(dimension=3, bits=3)

    def draw(self):
        pos_x, pos_y = next(self.__position_generator, (0, 0))
        color = next(self.__color_generator, 0) << 5
        self._screen[pos_x, pos_y, :] = color
        yield self._screen


class Mandelbrot(Animate):
    """! Fractal animation based on the Mandelbrot set.
    The iteration is limited to 512 and the coloring is done using a 3-bit, 3D Hilbert curve, thus
    all the color values are displayed as 512 iterations is equal to (2**3)**3 = 512 colors.
    @image html rgb.Mandelbrot.gif width=256px
    @sa https://en.wikipedia.org/wiki/Mandelbrot_set
    @sa https://codereview.stackexchange.com/a/216241
    @sa http://www.paulbourke.net/fractals/mandelbrot/
    @sa https://tsmeets.itch.io/mandelbrot
    """

    __LIMITS = 1.5
    __HILBERT_BITS = 3
    __HILBERT_DIMENSION = 3
    __ITERATION_MAX = (2 ** __HILBERT_DIMENSION) ** __HILBERT_BITS
    __ITERATION_STEP = 1
    __iterations = 1

    def __init__(self, shape: tuple, *args: list, **kwargs: dict):
        super().__init__(shape)
        # List interesting points and the maximum zoom level.
        self.__center = (-0.5, 0)

        # Pre-generate 512 colors based on the Hilbert curve.
        self.__colors = HilbertCurveGenerator(
            self.__HILBERT_DIMENSION, self.__HILBERT_BITS
        )

    def draw(self):
        xmin = -self.__LIMITS + self.__center[0]
        xmax = self.__LIMITS + self.__center[0]
        ymin = -self.__LIMITS + self.__center[1]
        ymax = self.__LIMITS + self.__center[1]

        complex_grid = np.zeros(self._screen.shape[0:2], dtype=np.complex)
        complex_grid.real, complex_grid.imag = np.meshgrid(
            np.linspace(xmin, xmax, num=self._screen.shape[1]),
            np.linspace(ymin, ymax, num=self._screen.shape[0]),
        )

        # Colors are encoded on 512 values, therefore 8 bits are not enough.
        iteration_grid = np.zeros(self._screen.shape[0:2], dtype=np.uint16)
        z_grid = np.zeros(self._screen.shape[0:2], dtype=np.complex)
        elements_todo = np.ones(self._screen.shape[0:2], dtype=bool)
        for iteration in range(min(self.__iterations, self.__ITERATION_MAX)):
            z_grid[elements_todo] = (
                z_grid[elements_todo] ** 2 + complex_grid[elements_todo]
            )
            mask = np.logical_and(
                (z_grid.real ** 2 + z_grid.imag ** 2) > 4, elements_todo
            )
            iteration_grid[mask] = iteration
            elements_todo = np.logical_and(elements_todo, np.logical_not(mask))

        self.__iterations += self.__ITERATION_STEP

        # Map the iteration values to the colors, left shift to get 8-bit colors.
        self._screen[:] = self.__colors.get(iteration_grid) << (8 - self.__HILBERT_BITS)

        yield self._screen
