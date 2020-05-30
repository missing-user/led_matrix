import math
import time

import numpy as np

import animations

TESTING = True

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
    w = Canvas(master, width=16 * (10 + 2), height=16 * (10 + 2))
    w.pack()

    # setup
    display.generateDisplay(w, 2, 10, 16, 16)
else:
    # Production
    import Led_display
    display = Led_display(16, 16)

totalTime = 0


def merge(l1, l2, l3):
    """merges two or three lists to one list of touples"""
    return list(map(lambda x, y, z: (x, y, z), l1, l2, l3))


def to8bitRgb(floatList):
    return [(math.floor(i[0] * 255), math.floor(i[1] * 255), math.floor(i[2] * 255)) for i in floatList]


import time
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


import signal
signal.signal(signal.SIGINT, on_exit)


def loop():
    """The main loop."""
    display.drawPixels(list(img.getdata()))

    while True:
        totalTime = time.time() - start_time
        time0 = time.time()
        times[0].append(time0)

        # draw pixels takes an array of RGB touples
        # 1ms
        r = animations.curtain(totalTime % 1)
        g = animations.curtain((totalTime + 0.1) % 1)
        b = animations.curtain((totalTime + 0.2) % 1)
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
        print(time.time() - start_time, iterations)


loop()
