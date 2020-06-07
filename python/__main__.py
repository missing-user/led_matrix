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
    tileSize = 60
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
    random.seed(sph.currentTrack['item']['id'])
    effects.add(timed(animChain.chain2, 0))
    for beat in range(600):
        if not effects(beat):
            effects.add(timed(random.choice(animChain.reg.all), beat))

    for segment in sph.results['segments']:
        seg_time = sph.time_to_beats(segment['start'])
        # there are segments with 'none' as their start time
        if seg_time:
            effects.add(timed(anim.diagonalWave,
                              seg_time, segment['duration']))
    # print(effects)


build_song_effects()


def loop():
    """The main loop."""
    while True:
        curr_effects = effects(get_time())
        if len(curr_effects) > 1:
            r = g = b = anim.overlay_border(
                curr_effects[0], [0] * row * col, len(curr_effects) - 1)
            g = anim.overlay_border([0] * row * col, anim.add_clamped(
                curr_effects[1:]), len(curr_effects) - 1)
        else:
            r = b = curr_effects[0]
            g = [0] * row * col

        r = g = b = effects(get_time())[0]

        display.drawPixels(to8bitRgb(merge(r, g, b)))
        display.update()  # 11ms


loop()
