#!/usr/bin/env python3
"""! Test all animations."""
from os import getenv
import subprocess
import logging
from src.localtime import Localtime
from animation.word_clock_english import WordClockEnglish
from animation.word_clock_japanese import WordClockJapanese

def test_analog_clock():
    """! Test analog clock animation."""
    subprocess.run(["./main.py", "AnalogClock", "save", "1"], check=True)

def test_openweathermap_invalid():
    """! Test calling OpenWeatherMap API with invalid key."""
    subprocess.run(["./main.py", "DigitalData",
        "-k", "",
        "-t", "GMT",
        "-c", "Tokyo",
        "save", "1"], check=True)

def test_openweathermap_valid():
    """! Test calling OpenWeatherMap API with valid key."""
    subprocess.run(["./main.py", "DigitalData",
        "-k", getenv('OPENWEATHERMAP_API_KEY'),
        "-t", "GMT",
        "-c", "Tokyo",
        "save", "1"], check=True)

def test_fire():
    """! Test fire animation."""
    subprocess.run(["./main.py", "Fire", "-r", "10000", "save", "100"],
        check=True)

def test_fire_16():
    """! Test fire animation with a 16-pixel high matrix."""
    subprocess.run(["./main.py", "Fire", "-y", "16", "save", "1"],
        check=True)

def test_game_of_life_color():
    """! Test game of life (color) animation."""
    subprocess.run(["./main.py", "GameOfLifeColor", "-r", "10000", "save", "10"],
        check=True)

def test_game_of_life_fast():
    """! Test game of life (fast) animation."""
    subprocess.run(["./main.py", "GameOfLifeFast", "-r", "10000", "save", "100"],
        check=True)

def test_water():
    """! Test water animation."""
    subprocess.run(["./main.py", "Water", "-r", "10000", "save", "100"],
        check=True)

def test_word_clock_english():
    """! Test word clock (English) animation."""
    localtime = Localtime()
    for stamp in range(0, 24*60):
        localtime.set_time(stamp * 60)
        logging.debug("%d - %02d:%02d - %s", stamp, localtime.hour,
            localtime.minute, WordClockEnglish.get_time(localtime))

    subprocess.run(["./main.py", "WordClockEnglish", "save", "1"],
        check=True)

def test_word_clock_japanese():
    """! Test word clock (Japanese) animation."""
    localtime = Localtime()
    for stamp in range(0, 24*60):
        localtime.set_time(stamp * 60)
        logging.debug("%d - %02d:%02d - %s", stamp, localtime.hour,
            localtime.minute, WordClockJapanese.get_time(localtime))

    subprocess.run(["./main.py", "WordClockJapanese", "save", "1"],
        check=True)

def test_qr_code():
    """! Test QR code animation."""
    subprocess.run(["./main.py", "QRCode", "--text", "Test", "save", "1"],
        check=True)

def test_maze():
    """! Test maze generator animation."""
    subprocess.run(["./main.py", "MazeGrowingTree", "-r", "10000", "save", "100"],
        check=True)
