import math
import random
import signal
import time

import numpy as np

import animationChains as animChain
import animations as anim
import spotifyHandler

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


start_time = time.time()

currEffect = animChain.chain1
effectOffset = 0


def loop():
    """The main loop."""
    global effectOffset
    global currEffect
    while True:
        totalTime = time.time() - start_time

        beatTimePercentage = (
            totalTime - spotifyHandler.currentSongTime) / spotifyHandler.beatTime
        beatTimePercentage -= effectOffset

        if beatTimePercentage < 18:
            r = anim.arrow(beatTimePercentage)
            g = anim.rotateMatrix90(
                anim.arrow(beatTimePercentage), 2)
            b = anim.rotateMatrix90(
                anim.arrow(beatTimePercentage), 1)
        elif beatTimePercentage < 22:
            r = anim.zipper(beatTimePercentage)
        elif beatTimePercentage < 26:
            r = g = b = anim.diagonalWave(beatTimePercentage)
        elif beatTimePercentage < 30:
            r = anim.circleInwards(beatTimePercentage / 2)
            g = b = anim.circleInwards((beatTimePercentage))
        elif beatTimePercentage < 38:
            g = b = anim.gif(beatTimePercentage / 8, "buildingCross8", 1)
            r = anim.gif(beatTimePercentage / 8, "buildingCross8", 0)
        elif beatTimePercentage < 46:
            r = b = anim.gif(beatTimePercentage / 8, "cross")
            g = anim.gif(beatTimePercentage / 8, "cross")
        elif beatTimePercentage < 50:
            g = r = anim.gif(beatTimePercentage, "compress")
            b = anim.strobe(beatTimePercentage)

        if beatTimePercentage >= currEffect.length or beatTimePercentage < 0:
            currEffect = random.choice(animChain.reg.all)
            effectOffset += beatTimePercentage
            print('now starting:', currEffect.__name__)
        r = g = b = currEffect(beatTimePercentage % currEffect.length)

        display.drawPixels(to8bitRgb(merge(r, g, b)))
        display.update()  # 11ms


loop()
