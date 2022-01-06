#!/usr/bin/env python3
"""! Animation saving server script."""
import socket
import logging
from threading import Thread
import numpy as np
from PIL import Image


class Save(Thread):
    """! Animation saving server class."""

    __frame_array = []
    __TIMEOUT = 3
    __FRAME_LENGTH = 48 * 32 + 1

    def __init__(
        self, name: str, frames: int = 1, duration: int = 40, port: int = 7777
    ):
        """! Constructor.
        @param name File name to save as.
        @param frames Number of frames to save.
        @param duration Duration of the animated image.
        @param port Port on which to advertise the saving server.
        """
        Thread.__init__(self, target=self.__run)
        self.__name = name
        assert frames > 0, "Frame count must be greater than 0."
        self.__frames = frames
        self.__duration = duration

        self.__server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.__server.settimeout(self.__TIMEOUT)
        self.__server.bind(("0.0.0.0", port))
        self.start()

    def __run(self):
        self.__server.listen(1)
        while len(self.__frame_array) < self.__frames:
            conn, _ = self.__server.accept()
            with conn:
                while len(self.__frame_array) < self.__frames:
                    data = conn.recv(self.__FRAME_LENGTH)
                    # Remove the terminator character.
                    data = data[:-1]
                    screen = self.unpack(data)
                    frame = Image.fromarray(screen)
                    self.__frame_array.append(frame)
                    # Acknowledge or terminate connection.
                    conn.send(
                        b"\n" if len(self.__frame_array) < self.__frames else b"0x4"
                    )

                    logging.debug(
                        "[%s] Progress: %.2f%%",
                        self.__class__.__name__,
                        100 * len(self.__frame_array) / self.__frames,
                    )
        logging.debug("[%s] Saving image...", self.__class__.__name__)
        filename = self.save()
        logging.info("[%s] Saved image under %s", self.__class__.__name__, filename)

    @staticmethod
    def unpack(data: bytearray) -> np.ndarray:
        """! Parse a binary screen to a numpy array.
        @param data Packed data as a byte array.
        @return Unpacked data as a Numpy array.
        """
        screen = np.array(list(data), dtype=np.uint8).reshape((48, 32))

        bit2 = screen[0::3]
        bit1 = screen[1::3]
        bit0 = screen[2::3]

        screen = np.zeros((32, 32, 3), dtype=np.uint8)
        screen[:16, :, 0] = (
            ((bit0 & 0x4) << 5) | ((bit1 & 0x4) << 4) | ((bit2 & 0x4) << 3)
        )
        screen[:16, :, 1] = (
            ((bit0 & 0x8) << 4) | ((bit1 & 0x8) << 3) | ((bit2 & 0x8) << 2)
        )
        screen[:16, :, 2] = (
            ((bit0 & 0x10) << 3) | ((bit1 & 0x10) << 2) | ((bit2 & 0x10) << 1)
        )
        screen[16:, :, 0] = (
            ((bit0 & 0x20) << 2) | ((bit1 & 0x20) << 1) | ((bit2 & 0x20) << 0)
        )
        screen[16:, :, 1] = (
            ((bit0 & 0x40) << 1) | ((bit1 & 0x40) << 0) | ((bit2 & 0x40) >> 1)
        )
        screen[16:, :, 2] = (
            ((bit0 & 0x80) << 0) | ((bit1 & 0x80) >> 1) | ((bit2 & 0x80) >> 2)
        )
        return screen

    def save(self) -> str:
        """! Save the animation.
        @return The file name under which the image was saved.
        """
        extention = "gif" if self.__frames > 1 else "png"
        filename = f"{self.__name}.{extention}"
        self.__frame_array[0].save(
            filename,
            save_all=True,
            append_images=self.__frame_array[1:],
            optimize=False,
            duration=self.__duration,
            loop=0,
        )
        return filename
