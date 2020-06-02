import math
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
iterations = 0

times = [[], [], [], []]


# FOR DEBUG

def on_exit(a, b):
    print("exit")
    averages = [np.mean(l) * 1000 for l in times]
    print("avg times", averages)
    print("avg fps", iterations / (time.time() - start_time))
    exit()


signal.signal(signal.SIGINT, on_exit)


def loop():
    """The main loop."""

    while True:
        totalTime = time.time() - start_time
        time0 = time.time()
        times[0].append(time0)
        # draw pixels takes an array of RGB touples
        # 1ms

        beatTimePercentage = (
            totalTime - spotifyHandler.currentSongTime) / spotifyHandler.beatTime
        beatTimePercentage = beatTimePercentage % 120
        if beatTimePercentage < 12:
            g = b = r = animChain.chain1(beatTimePercentage % 12)
        elif beatTimePercentage < 18:
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
        elif beatTimePercentage < 55:
            g = b = r = anim.strobe(beatTimePercentage * 3)
        elif beatTimePercentage < 60:
            g = b = r = anim.curtain(
                anim.easing.triangle(beatTimePercentage / 2))
        elif beatTimePercentage < 65:
            g = b = r = anim.rotateMatrix90(anim.curtain(
                anim.easing.triangle(beatTimePercentage / 2)), 1)
        elif beatTimePercentage < 71:
            g = b = r = animChain.chain3(beatTimePercentage % 16)
        elif beatTimePercentage < 71:
            g = b = r = animChain.chain4(beatTimePercentage % 16)
        elif beatTimePercentage < 78:
            g = b = r = animChain.chain5(beatTimePercentage % 16)
        else:
            g = b = r = animChain.chain2(
                beatTimePercentage % animChain.chain2.length)

        time1 = time.time()
        times[1].append(time1 - time0)

        # 3ms
        display.drawPixels(to8bitRgb(merge(r, g, b)))

        time2 = time.time()
        times[2].append(time2 - time1)

        # 11ms
        display.update()
        time3 = time.time()
        times[3].append(time3 - time2)

        global iterations
        iterations += 1
        # print("frame", iterations, "at", time.time() - start_time, "s")


loop()
