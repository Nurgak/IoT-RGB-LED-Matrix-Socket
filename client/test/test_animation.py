#!/usr/bin/env python3
"""! Test all animations."""
from os import getenv
import subprocess
import logging
from src.localtime import Localtime
from animation.word_clock import English, Japanese


def test_analog_clock():
    """! Test analog clock animation."""
    subprocess.run(["./main.py", "analog_clock.AnalogClock", "-vvv", "save", "1"], check=True)


def test_openweathermap_invalid():
    """! Test calling OpenWeatherMap API with invalid key."""
    subprocess.run(
        [
            "./main.py",
            "digital_data.DigitalData",
            "-k",
            "",
            "-t",
            "GMT",
            "-c",
            "Tokyo",
            "-vvv",
            "save",
            "1",
        ],
        check=True,
    )


def test_openweathermap_valid():
    """! Test calling OpenWeatherMap API with valid key."""
    subprocess.run(
        [
            "./main.py",
            "digital_data.DigitalData",
            "-k",
            getenv("OPENWEATHERMAP_API_KEY"),
            "-t",
            "GMT",
            "-c",
            "Tokyo",
            "-vvv",
            "save",
            "1",
        ],
        check=True,
    )


def test_fire_16():
    """! Test fire animation with a 16-pixel high matrix."""
    subprocess.run(["./main.py", "fire.Fire", "-y", "16", "save", "2"], check=True)


def test_fire():
    """! Test fire animation."""
    subprocess.run(["./main.py", "fire.Fire", "-r", "10000", "save", "100"], check=True)


def test_game_of_life_color():
    """! Test game of life (color) animation."""
    subprocess.run(
        ["./main.py", "game_of_life.GameOfLifeColor", "-r", "10000", "save", "100"],
        check=True,
    )


def test_game_of_life_fast():
    """! Test game of life (fast) animation."""
    subprocess.run(
        ["./main.py", "game_of_life.GameOfLifeFast", "-r", "10000", "save", "100"],
        check=True,
    )


def test_water():
    """! Test water animation."""
    subprocess.run(
        ["./main.py", "water.Water", "-r", "10000", "save", "100"], check=True
    )


def test_word_clock_english():
    """! Test word clock (English) animation."""
    localtime = Localtime(update_rate=0)
    word_clock = English((0, 0), timezone="GMT")
    for stamp in range(0, 24 * 60):
        localtime.set_time(stamp * 60)
        logging.debug(
            "%d - %02d:%02d - %s",
            stamp,
            localtime.hour,
            localtime.minute,
            word_clock.get_time(localtime),
        )

    subprocess.run(["./main.py", "word_clock.English", "save", "1"], check=True)


def test_word_clock_japanese():
    """! Test word clock (Japanese) animation."""
    localtime = Localtime(update_rate=0)
    word_clock = Japanese((0, 0), timezone="GMT")
    for stamp in range(0, 24 * 60):
        localtime.set_time(stamp * 60)
        logging.debug(
            "%d - %02d:%02d - %s",
            stamp,
            localtime.hour,
            localtime.minute,
            word_clock.get_time(localtime),
        )

    subprocess.run(["./main.py", "word_clock.Japanese", "save", "1"], check=True)


def test_qr_code():
    """! Test QR code animation."""
    subprocess.run(
        ["./main.py", "qr_code.QRCode", "--text", "Test", "save", "1"], check=True
    )


def test_growing_tree():
    """! Test the growing tree animation."""
    subprocess.run(
        ["./main.py", "rgb.GrowingTree", "-r", "10000", "save", "1023"], check=True
    )


def test_mandelbrot():
    """! Test Mandelbrot animation."""
    subprocess.run(
        ["./main.py", "rgb.Mandelbrot", "-r", "10000", "save", "24"], check=True
    )


def test_hilbert():
    """! Test Hilbert curve animation."""
    subprocess.run(
        ["./main.py", "rgb.HilbertCurve", "-r", "10000", "save", "1023"], check=True
    )
