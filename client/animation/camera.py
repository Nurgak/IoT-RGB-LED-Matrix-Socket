#!/usr/bin/env python3
"""! Camera animation."""
import logging
import cv2 as cv
from src.animate import Animate


class Camera(Animate):
    """! Camera animation class.
    @image html camera.Camera.gif width=256px
    Animation displaying the input from a camera, resized for the screen. Needs the client to have a
    camera input.
    """
    __DEVICE = 0
    __RESOLUTION = (640, 480)
    __FPS = 30

    def __init__(self, shape: tuple, *args: list, **kwargs: dict):
        super().__init__(shape)
        self.__camera = cv.VideoCapture(self.__DEVICE)
        assert self.__camera.isOpened(), \
            f"[{self.__class__.__name__}] Video capturing has not been initialized."
        self.__camera.set(cv.CAP_PROP_FRAME_WIDTH, self.__RESOLUTION[0])
        self.__camera.set(cv.CAP_PROP_FRAME_HEIGHT, self.__RESOLUTION[1])
        self.__camera.set(cv.CAP_PROP_FPS, self.__FPS)

    def __del__(self):
        self.__camera.release()
        del self.__camera
        super().__del__()

    def draw(self):
        success, frame = self.__camera.read()
        if not success:
            logging.warning("[%s] Could not get frame from camera.", self.__class__.__name__)
        else:
            self._screen = cv.resize(frame, self._screen.shape[0:2], cv.INTER_NEAREST)
        yield self._screen
