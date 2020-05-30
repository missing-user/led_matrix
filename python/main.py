import math
import time

import numpy as np
from PIL import Image

import animations

# import depending on production or testing
TESTING = True
if(TESTING):
    # load a preview image
    try:
        global img
        img = Image.open("../web/images/256icon.png")
        img.thumbnail((16, 16))
        img = img.convert('RGB')
    except IOError:
        pass

    import preview as display
    from tkinter import *
    master = Tk()
    # the canvas fits matrix and has a margin of [pixel_spacing] around the border
    w = Canvas(master, width=16 * (10 + 2),
               height=16 * (10 + 2))
    w.pack()
    display.generateDisplay(w, 2, 10, 16, 16)


else:
    import Led_display
    display = Led_display(16, 16)

totalTime = 0

# merges two or three lists to one list of touples


def merge(l1, l2, l3):
    return list(map(lambda x, y, z: (x, y, z), l1, l2, l3))


def to8bitRgb(floatList):
    return [(math.floor(i[0] * 255), math.floor(i[1] * 255), math.floor(i[2] * 255)) for i in floatList]


def loop():
    global totalTime
    time.sleep(0.007)
    totalTime += 0.007
    # draw pixels takes an array of RGB touples
    if(totalTime < 0):
        display.drawPixels(list(img.getdata()))
    else:

        r = animations.Effects.curtain(totalTime % 1)
        g = animations.Effects.curtain((totalTime + 0.1) % 1)
        b = animations.Effects.curtain((totalTime + 0.2) % 1)
        display.drawPixels(to8bitRgb(merge(r, g, b)))
        pass
    display.update()

    loop()


loop()
