#!/usr/bin/env python3
"""! QR code generator animation script."""
import numpy as np
import qrcode
from src.animate import Animate


class QRCode(Animate):
    """! QR code generator animation class.
    @image html qr_code.QRCode.png width=256px
    Animation displaying a static QR-code-encoded-text.
    """

    __CODE_COLOR = (0xFF, 0xFF, 0xFF)

    def __init__(self, shape: tuple, *args: list, **kwargs: dict):
        super().__init__(shape)
        self.__text = kwargs["text"]
        assert self.__text != "", "Text is empty."

    def draw(self):
        qr_code = qrcode.QRCode(
            version=1,
            # error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=1,
            border=0,
        )

        qr_code.add_data(self.__text)
        qr_code.make(fit=True)

        qr_pil = qr_code.make_image(fill_color=self.__CODE_COLOR, back_color=(0, 0, 0))
        qr_np = np.array(qr_pil)

        assert (
            qr_np.shape <= self._screen.shape
        ), f"[{self.__class__.__name__}] QR code too large."

        # Center the code on the screen.
        offset_y = (self._screen.shape[0] - qr_np.shape[0]) // 2
        offset_x = (self._screen.shape[1] - qr_np.shape[1]) // 2
        self._screen[
            offset_y : qr_np.shape[1] + offset_y, offset_x : qr_np.shape[0] + offset_x
        ] = qr_np
        yield self._screen
