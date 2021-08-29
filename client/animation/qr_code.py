#!/usr/bin/env python3
"""! QR code generator animation script."""
import numpy as np
import qrcode
from src.animate import Animate

class QRCode(Animate):
    """! QR code generator animation class.
    @image html media/QRCode.png "QRCode animation example" width=256px
    Animation displaying a static QR-code-encoded-text.
    """
    def __init__(self, shape: tuple, *args: list, **kwargs: dict):
        """! Constructor.
        @param shape Screen shape: height, width and color channels, for example:
        <tt>(32, 32, 3)</tt>.
        @param args Non-Keyword Arguments, not used.
        @param kwargs Keyword Arguments, set the @p text parameter to the text
        that will be encoded in the QR code.
        """
        self.__back_color = (0x00, 0x00, 0x00)
        self.__fill_color = (0xff, 0xff, 0xff)
        self.__screen = np.full(shape, self.__back_color, dtype=np.uint8)
        self.__text = kwargs["text"]
        assert self.__text != "", "Text is empty."

    def draw(self):
        """! Draw one frame of the animation."""
        qr_code = qrcode.QRCode(
            version=1,
            #error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=1,
            border=0,
        )

        qr_code.add_data(self.__text)
        qr_code.make(fit=True)

        qr_pil = qr_code.make_image(
            fill_color=self.__fill_color,
            back_color=self.__back_color
        )
        qr_np = np.array(qr_pil)

        assert qr_np.shape <= self.__screen.shape, \
            f"[{self.__class__.__name__}] QR code too large."

        # Center the code on the screen.
        offset_y = (self.__screen.shape[0] - qr_np.shape[0]) // 2
        offset_x = (self.__screen.shape[1] - qr_np.shape[1]) // 2
        self.__screen[offset_y:qr_np.shape[1]+offset_y,
            offset_x:qr_np.shape[0]+offset_x] = qr_np
        yield self.__screen
