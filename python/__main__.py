import colorsys
import math
import random
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
    master.configure(background='black')
    tileSize = 60
    w = Canvas(master, width=row * (tileSize + 0), height=col * (tileSize + 0))
    w.pack()

    # setup
    display.generateDisplay(w, 0, tileSize, row, col)
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
color_list = []


def get_time():
    """returns the current song time in 'beats units'"""
    global start_time_seconds
    return sph.time_to_beats(time.time() - start_time_seconds)


def colors(time):
    for i, sect in enumerate(sections_list):
        if time > sect['beat']:
            return (sect['hue1'], sect['hue2'])
    return (sections_list[0]['hue1'], sections_list[0]['hue2'])


def build_song_effects():
    global start_time_seconds
    start_time_seconds = time.time() - sph.currentSongTime
    random.seed(sph.currentTrack['item']['id'])

    global sections_list
    sections_list = []
    for sect in sph.results['sections']:
        sections_list.append({'beat': sph.time_to_beats(sect['start']),
                              'hue1': random.random(),
                              'hue2': random.random()})
    sections_list.reverse()

    effects.add(timed(animChain.chain1, 0))
    for beatIndex in range(len(sph.results['beats'])):
        if not effects(beatIndex):
            effects.add(timed(random.choice(animChain.reg.all), beatIndex))

    for segment in sph.results['segments']:
        seg_time = sph.time_to_beats(segment['start'])
        # there are segments with 'none' as their start time
        if seg_time:
            if colors(seg_time)[1] > 0.5:
                effects.add(timed(anim.diagonalWave,
                                  seg_time, segment['duration']))
            else:
                effects.add(timed(anim.strobe, seg_time, segment['duration']))

    # print(effects)
    print('colors', sections_list)


build_song_effects()


def mapFromTo(x, a=0, b=1, c=0, d=1):
    y = (x - a) / (b - a) * (d - c) + c
    return y


def loop():
    """The main loop."""
    while True:
        curr_effects = effects(get_time())

        # set preliminary random colors
        (hue1, hue2) = colors(get_time())

        if hue1 > 0.5:
            m = anim.overlay_border(
                curr_effects[0], anim.add_clamped(curr_effects[1:]))
        else:
            m = curr_effects[0]

        coloredImage = [(colorsys.hsv_to_rgb(mapFromTo(i, 0, 1, hue1, hue2), 1, anim.clamp(2 * i))
                         if i != 0 else (0, 0, 0))for i in m]
        display.drawPixels(to8bitRgb(coloredImage))
        display.update()  # 11ms


loop()
