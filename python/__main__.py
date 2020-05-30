import math
import time

import numpy as np
from PIL import Image

import animations

TESTING = True

# import depending on production or testing
if TESTING:
    # Testing
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


def loop():
    display.drawPixels(list(img.getdata()))

    while True:
        totalTime = time.time() - start_time

        # draw pixels takes an array of RGB touples
        r = animations.curtain(totalTime % 1)
        g = animations.curtain((totalTime + 0.1) % 1)
        b = animations.curtain((totalTime + 0.2) % 1)
        display.drawPixels(to8bitRgb(merge(r, g, b)))

        display.update()

        global iterations
        iterations += 1
        print(time.time() - start_time, iterations)


loop()
