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
    from PIL import Image
    # load a preview image
    try:
        global img
        img = Image.open("../web/images/256icon.png")
        img.thumbnail((16, 16))
        img = img.convert('RGB')
    except IOError:
        pass

    # setup Tkinter
    import preview as display
    from tkinter import Tk, Canvas

    # the canvas fits matrix and has a margin of [pixel_spacing] around the border
    master = Tk()
    tileSize = 40
    w = Canvas(master, width=row * (tileSize + 2), height=col * (tileSize + 2))
    w.pack()

    # setup
    display.generateDisplay(w, 2, tileSize, row, col)
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
    display.drawPixels(list(img.getdata()))

    while True:
        totalTime = time.time() - start_time
        time0 = time.time()
        times[0].append(time0)
        totalTime = totalTime % 20
        # draw pixels takes an array of RGB touples
        # 1ms
        if totalTime < 1:
            r = g = b = animations.gif(
                (totalTime - spotifyHandler.currentSongTime) / 8 / spotifyHandler.beatTime % 1)

        elif totalTime < 8:
            r = b = g = animations.doubleArrow(
                (totalTime - spotifyHandler.currentSongTime) / spotifyHandler.beatTime % 1)
        elif totalTime < 8:
            r = animations.arrow(
                (totalTime - spotifyHandler.currentSongTime) / spotifyHandler.beatTime % 1)
            g = animations.rotateMatrix90(animations.arrow(
                (totalTime - spotifyHandler.currentSongTime) / spotifyHandler.beatTime % 1), 2)
            b = animations.rotateMatrix90(animations.arrow(
                (totalTime - spotifyHandler.currentSongTime) / spotifyHandler.beatTime % 1), 1)
        elif totalTime < 12:
            r = animations.zipper(
                (totalTime - spotifyHandler.currentSongTime) / spotifyHandler.beatTime % 1)
        elif totalTime < 18:
            r = g = b = animations.diagonalWave(
                (totalTime - spotifyHandler.currentSongTime) / spotifyHandler.beatTime % 1)
        else:
            r = animations.circleInwards(
                (totalTime - spotifyHandler.currentSongTime) / spotifyHandler.beatTime % 1)
            g = animations.circleInwards(
                (totalTime - spotifyHandler.currentSongTime + 0.1) / spotifyHandler.beatTime % 1)
            b = animations.circleInwards(
                (totalTime - spotifyHandler.currentSongTime + 0.2) / spotifyHandler.beatTime % 1)
        time1 = time.time()
        times[1].append(time1 - time0)

        # 3ms
        display.drawPixels(to8bitRgb(merge(r, g, b)))

        # display.drawPixels(list(img.getdata()))       #draw an image
        time2 = time.time()
        times[2].append(time2 - time1)

        # 11ms
        display.update()
        time3 = time.time()
        times[3].append(time3 - time2)

        global iterations
        iterations += 1
        print("frame", iterations, "at", time.time() - start_time, "s")


loop()
