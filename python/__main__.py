import math
import random
import signal
import time

import numpy as np

import animationChains as animChain
import animations as anim
import spotifyHandler as sph
from effect_list import Effect_List, timed

TESTING = True
row = 16
col = 16

anim.row = row
anim.col = col

# import depending on production or testing
if TESTING:
    # Testing
    # setup Tkinter
    import preview as display
    from tkinter import Tk, Canvas

    # the canvas fits matrix and has a margin of [pixel_spacing] around the border
    master = Tk()
    tileSize = 40
    w = Canvas(master, width=row * (tileSize + 5), height=col * (tileSize + 5))
    w.pack()

    # setup
    display.generateDisplay(w, 5, tileSize, row, col)
    print("starting matrix in testing mode")
else:
    # Production
    import Led_display
    display = Led_display(row, col)


def merge(l1, l2, l3):
    """merges two or three lists to one list of touples"""
    return list(map(lambda x, y, z: (x, y, z), l1, l2, l3))


def to8bitRgb(floatList):
    return [(math.floor(i[0] * 255), math.floor(i[1] * 255), math.floor(i[2] * 255)) for i in floatList]


start_time_seconds = time.time()
effects = Effect_List()


def get_time():
    """returns the current song time in 'beats units'"""
    global start_time_seconds
    return sph.time_to_beats(time.time() - start_time_seconds)


def build_song_effects():
    global start_time_seconds
    start_time_seconds = time.time() - sph.currentSongTime
    effects.add(timed(animChain.chain2, 0))
    for test in range(400):
        if not effects(test):
            effects.add(timed(random.choice(animChain.reg.all), test))
    print(effects)


build_song_effects()


def loop():
    """The main loop."""
    while True:
        print(get_time())
        r = g = b = effects(get_time())[0]

        display.drawPixels(to8bitRgb(merge(r, g, b)))
        display.update()  # 11ms


loop()
