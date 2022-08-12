#!/usr/bin/env python3
"""! IoT RGB LED Matrix Socket main animation caller script.

The script imports all animation modules from the animation directory, the CLI
interface is self-documenting using the @c --help parameter.

New animations can be added by creating a new file in the animations directory.
"""
import os
import sys
import argparse
import logging
from importlib import import_module
from src.save import Save
from src.display import Display

parser = argparse.ArgumentParser(description="IoT RGB LED Matrix animation loader.")
parser.add_argument("animation", type=str, help="animation class")
parser.add_argument("-x", "--width", type=int, default=32, help="panel width in pixels")
parser.add_argument(
    "-y", "--height", type=int, default=32, help="panel height in pixels"
)
parser.add_argument(
    "-r", "--rate", type=int, default=30, help="animation update rate in Hz"
)
parser.add_argument(
    "-t",
    "--timezone",
    type=str,
    default="GMT",
    help="timezone for animations showing time",
)
parser.add_argument("-k", "--key", type=str, default="", help="OpenWeatherMap API key")
parser.add_argument(
    "-c", "--city", type=str, default="", help="city name for weather data"
)
parser.add_argument("--text", type=str, default="", help="text data to display")
parser.add_argument("-v", dest="verbose", action="count", help="increase verbosity")

subparsers = parser.add_subparsers(help="mode")

parser_save = subparsers.add_parser("save", help="save the animation to an image")
parser_save.add_argument(
    "frames",
    type=int,
    help="specify number of frames, 1 will generate a png, more will generate a gif",
)
parser_save.add_argument(
    "-d",
    "--dir",
    type=str,
    default="client/media",
    help="directory where to save the image",
)

parser_display = subparsers.add_parser(
    "display", help="display the animation on a LED matrix"
)
parser_display.add_argument("server", type=str, help="server address")
parser_display.add_argument("-p", "--port", type=int, default=7777, help="server port")
parser_display.add_argument(
    "-c",
    "--current",
    type=float,
    default=float("inf"),
    help="maximum current in Amperes",
)

args = parser.parse_args()

logging_level = [logging.ERROR, logging.WARNING, logging.INFO, logging.DEBUG][
    args.verbose or 0
]
logging.basicConfig(format="%(levelname)s:%(message)s", level=logging_level)

if hasattr(args, "frames"):  # pragma: no cover
    args.server = "0.0.0.0"
    args.port = 7777
    args.current = 0.2
    filename = os.path.join(args.dir, args.animation)
    Save(filename, frames=args.frames, port=args.port)

client = Display(args.server, port=args.port, current_max=args.current)

shape = (args.height, args.width, 3)

try:
    animation_module, animation_method = args.animation.split(".")
    animation_instance = getattr(
        import_module(f"animation.{animation_module}"), animation_method
    )
    animation_instance(shape, **vars(args)).animate(
        client=client, update_rate=args.rate
    )
except KeyboardInterrupt:  # pragma: no cover
    sys.exit(0)
