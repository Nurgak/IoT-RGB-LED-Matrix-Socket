#!/usr/bin/env python3
"""! Abstract animation script."""
from time import sleep


# pylint: disable=too-few-public-methods
class Animate:
    """! Abstract animation class."""
    def draw(self):  # pragma: no cover
        """! Abstract draw function.
        @exception NotImplementedError Function must be overridden.
        """
        raise NotImplementedError("Draw must be overridden.")

    def animate(self, client: object, rate: int):
        """! Execute the animation.
        @param client The instance which will be updated with the animation.
        @param rate The update rate of the animation in Hz.
        """
        while True:
            client.update(next(self.draw()))
            sleep(1.0 / rate)
