import math
import signal
import time

import numpy as np

import animations
import spotifyHandler

TESTING = True
row = 16
col = 16

animations.row = row
animations.col = col

# import depending on production or testing
if TESTING:
    # Testing
    # setup Tkinter
    import preview as display
    from tkinter import Tk, Canvas

    # the canvas fits matrix and has a margin of [pixel_spacing] around the border
    master = Tk()
    tileSize = 80
    w = Canvas(master, width=row * (tileSize + 5), height=col * (tileSize + 2))
    w.pack()

    # setup
    display.generateDisplay(w, 5, tileSize, row, col)
    print("starting matrix in testing mode")
else:
    # Production
    import Led_display
    display = Led_display(row, col)

totalTime = 0


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
        totalTime = totalTime % 55
        # draw pixels takes an array of RGB touples
        # 1ms

        beatTimePercentage = (
            totalTime - spotifyHandler.currentSongTime) / spotifyHandler.beatTime
        if totalTime < 4:
            r = g = b = animations.gif(beatTimePercentage / 8 % 1)
        elif totalTime < 8:
            r = b = g = animations.doubleArrow(beatTimePercentage % 1)
        elif totalTime < 12:
            r = animations.arrow(beatTimePercentage % 1)
            g = animations.rotateMatrix90(
                animations.arrow(beatTimePercentage % 1), 2)
            b = animations.rotateMatrix90(
                animations.arrow(beatTimePercentage % 1), 1)
        elif totalTime < 18:
            r = animations.zipper(beatTimePercentage % 1)
        elif totalTime < 22:
            r = g = b = animations.diagonalWave(beatTimePercentage % 1)
        elif totalTime < 26:
            r = animations.circleInwards(beatTimePercentage / 2 % 1)
            g = animations.circleInwards((beatTimePercentage) % 1)
            b = animations.circleInwards(beatTimePercentage % 1)
        elif totalTime < 32:
            g = b = animations.gif(beatTimePercentage / 8 % 1, 3, 1)
            r = animations.gif(beatTimePercentage / 8 % 1, 3, 0)

        elif totalTime < 36:
            g = b = animations.gif(beatTimePercentage / 8 % 1, 2)
            r = animations.gif(beatTimePercentage / 8 % 1, 2)
        elif totalTime < 40:
            g = b = animations.gif(beatTimePercentage % 1, 1)
            r = animations.strobe(beatTimePercentage % 1)
        elif totalTime < 45:
            g = b = r = animations.strobe(beatTimePercentage * 3 % 1)
        elif totalTime < 50:
            g = b = r = animations.curtain(
                animations.easing.triangle(beatTimePercentage / 2 % 1))
        elif totalTime < 55:
            g = b = r = animations.rotateMatrix90(animations.curtain(
                animations.easing.triangle(beatTimePercentage / 2 % 1)), 1)

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
