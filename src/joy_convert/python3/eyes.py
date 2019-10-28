#!/usr/bin/env python3

import board
import neopixel
import sys


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print('Usage: eye.py red green blue')
        exit(1)
    print (sys.argv)
    red = int(sys.argv[1])
    green = int(sys.argv[2])
    blue = int(sys.argv[3])

    #Single ring
    #pixels = neopixel.NeoPixel(board.D18, 16)
    #2 rings (series)
    pixels = neopixel.NeoPixel(board.D18, 32)
    pixels.fill((green, blue, red))
