#!/usr/bin/env python3
"""! Write text on a provided screen."""
import numpy as np
from PIL import ImageFont, ImageDraw, Image


# pylint: disable=too-few-public-methods
class Text:
    """! Draw text on a referenced screen."""
    ## Normal wrapping, using whitespaces and line breaks.
    WRAP_NORMAL = 0
    ## Force wrapping, wrapping by character.
    WRAP_FORCE = 1
    ## No wrapping, text will overflow screen.
    WRAP_NONE = -1

    def __init__(self, fontpath: str, fontsize: int):
        """! Constructor.
        @param fontpath Path to the font file.
        @param fontsize Font size.
        """
        self.__font = ImageFont.truetype(fontpath, fontsize)

    # pylint: disable=too-many-arguments
    def write(self, screen: np.ndarray, text: str, color: tuple=(0xff, 0xff, 0xff),
        offset: tuple=(0, 0), wrap: int=WRAP_NORMAL):
        """! Draw text on a provided screen.
        @param screen The screen reference.
        @param text Text to write on the screen.
        @param color Color of the text, in RGB, from 0x00 to 0xff.
        @param offset Text offset from top left corner.
        @param wrap Wrapping style.
        """
        screen_pil = Image.fromarray(screen)
        image_draw = ImageDraw.Draw(screen_pil)

        assert wrap in [Text.WRAP_NORMAL, Text.WRAP_FORCE, Text.WRAP_NONE], \
            f"Unrecogised wrap method: {wrap}."

        text_multiline = []
        line = ""
        if wrap is Text.WRAP_NORMAL:
            # Split text into words by whitespace.
            for word in text.split():
                temp = f"{line} {word}".strip()

                # When the line is longer than the canvas width: split.
                if image_draw.textsize(temp, font=self.__font)[0] > screen.shape[1]:
                    text_multiline.append(line)
                    line = word
                else:
                    line = temp

            text_multiline.append(line)
        elif wrap is Text.WRAP_FORCE:
            # Fit text into the screen.
            # New line character is not accurate for line splitting (gap too large).
            for letter in text:
                line += letter

                if image_draw.textsize(line, font=self.__font)[0] > screen.shape[1]:
                    text_multiline.append(line[:-1])
                    line = letter

            text_multiline.append(line)
        else:
            image_draw.text(offset, text, font=self.__font, fill=color)

        offset_y = 0
        for line in text_multiline:
            image_draw.text((offset[0], offset[1]+offset_y), line, font=self.__font, fill=color)
            offset_y += image_draw.textsize(line, font=self.__font)[1]

        screen[:] = np.array(screen_pil)
