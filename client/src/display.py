#!/usr/bin/env python3
"""! RGB matrix panel socket client script."""
import sys
import socket
import logging
import numpy as np


class Display:
    """! RGB matrix panel socket client class.
    The display current consumption per pixel has been measured for each of the colors separately
    using a USB power meter.
    """

    __socket = None
    __screen = None
    __connected = False
    __current_base = 0.13
    __current_color = [0.000139, 0.0000605, 0.0000378]

    def __init__(
        self,
        server: str,
        port: int = 7777,
        timeout: int = 3.0,
        current_max: float = float("inf"),
    ):
        """! Constructor.
        @param server The server IP address.
        @param port The server port number.
        @param timeout Communication timeout in seconds.
        @param current_max Maximum current limit the matrix is allowed to use, in Amperes.
        """
        self.__connection = (server, port)
        self.__timeout = timeout
        self.__current_max = current_max

    def connect(self) -> bool:
        """! Connect to the server.
        @return Status of the connection: True if connected, False if disconnected.
        """
        if not self.__connected:
            logging.info("[%s] Connecting to display...", self.__class__.__name__)
            try:
                self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.__socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                self.__socket.settimeout(self.__timeout)
                self.__socket.connect(self.__connection)
                logging.info("[%s] Connection successful.", self.__class__.__name__)
                self.__connected = True
            except ConnectionRefusedError:  # pragma: no cover
                logging.warning("[%s] Connection refused.", self.__class__.__name__)
            except (
                socket.timeout,
                ConnectionAbortedError,
                BlockingIOError,
                OSError,
            ) as error:  # pragma: no cover
                logging.warning(
                    "[%s] Connection error: %s", self.__class__.__name__, error
                )

        return self.__connected

    def update(self, screen: np.ndarray) -> bool:
        """! Update the screen. The screen will not be updated if the display has not changed from
        the previous update. If defined, dim screen if estimated current goes beyond limit.
        @return True if the screen was updated, false otherwise.
        """
        if np.all(screen == self.__screen):  # pragma: no cover
            logging.debug("[%s] No changes on display.", self.__class__.__name__)
            return False

        if not self.connect():
            return False  # pragma: no cover

        self.__screen = screen.copy()

        for _ in range(7):
            current_estimated = self.__current_base
            current_estimated += (
                np.sum(self.__screen[:, :, 0] >> 5) * self.__current_color[0]
            )
            current_estimated += (
                np.sum(self.__screen[:, :, 1] >> 5) * self.__current_color[1]
            )
            current_estimated += (
                np.sum(self.__screen[:, :, 2] >> 5) * self.__current_color[2]
            )

            if current_estimated <= self.__current_max:
                logging.debug(
                    "[%s] Estimated current: %.3fA.",
                    self.__class__.__name__,
                    current_estimated,
                )
                break

            self.__screen[(self.__screen & (0b111 << 5)) > 0] -= 1 << 5
        else:
            logging.warning(
                "[%s] Screen dimmed to the maximum.", self.__class__.__name__
            )

        packed = self.pack(self.__screen)

        try:
            self.__socket.sendall(packed)
        except (
            socket.timeout,
            BrokenPipeError,
            ConnectionResetError,
        ):  # pragma: no cover
            logging.warning("[%s] Disconnected.", self.__class__.__name__)
            self.__connected = False
            return False

        try:
            response = self.__socket.recv(1024)
            if response == b"0x4":
                logging.info("[%s] Server closed, exiting.", self.__class__.__name__)
                sys.exit(0)
        except (socket.timeout, ConnectionResetError):  # pragma: no cover
            logging.warning("[%s] Acknowledge timeout.", self.__class__.__name__)
            self.__socket.close()
            self.__connected = False
            return False

        return True

    @staticmethod
    def pack(screen: np.ndarray) -> bytearray:
        """! Pack the frame data to be directly read into the display buffer.
        @param screen The screen data. A terminator character @c \n is added for data syncing.
        @return The packed data to be sent over a socket connection to the screen.
        """
        if screen.shape[0] == 32:
            # Split the top and bottom halves to compress them.
            data_top, data_bottom = screen[:16] >> 5, screen[16:] >> 5
        else:
            # Use a dummy black screen for a 16-pixel height display.
            data_top, data_bottom = screen >> 5, np.zeros_like(screen)

        bit1 = ((data_top >> 0) & 1) << np.array([2, 3, 4], np.uint8)
        bit2 = ((data_top >> 1) & 1) << np.array([2, 3, 4], np.uint8)
        bit3 = ((data_top >> 2) & 1) << np.array([2, 3, 4], np.uint8)

        bit4 = ((data_bottom >> 0) & 1) << np.array([5, 6, 7], np.uint8)
        bit5 = ((data_bottom >> 1) & 1) << np.array([5, 6, 7], np.uint8)
        bit6 = ((data_bottom >> 2) & 1) << np.array([5, 6, 7], np.uint8)

        out = np.zeros((48, 32), dtype=np.uint8)

        out[0::3] += np.sum(bit1, axis=2) + np.sum(bit4, axis=2)
        out[1::3] += np.sum(bit2, axis=2) + np.sum(bit5, axis=2)
        out[2::3] += np.sum(bit3, axis=2) + np.sum(bit6, axis=2)

        return bytearray(out) + b"\n"
