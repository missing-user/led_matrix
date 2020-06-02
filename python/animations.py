import math

from PIL import Image, ImageSequence

import easing

row = 16
col = 16

# helper functions


def clamp(value, min=0, max=1):
    if(value < min):
        return min
    elif(value > max):
        return max
    return value


def fromXY(x, y):
    return y * row + x


def XY(index):
    return [index % row, index // row]


# rotates the given matrix by count 90deg increments
def rotateMatrix90(input_leds, count):
    count = (count + 4) % 4
    rotated_leds = input_leds.copy()
    if count == 1:
        for i in range(len(input_leds)):
            # rotate 90 deg
            rotated_leds[fromXY(XY(i)[1], row - 1 - XY(i)[0])] = input_leds[i]
    elif count == 2:
        for i in range(len(input_leds)):
            # rotate 90 deg
            rotated_leds[fromXY(row - 1 - XY(i)[0], col -
                                1 - XY(i)[1])] = input_leds[i]

    elif count == 3:
        for i in range(len(input_leds)):
            # rotate 90 deg
            rotated_leds[i] = input_leds[fromXY(XY(i)[1], row - 1 - XY(i)[0])]
    elif count == 0:
        return input_leds
    return rotated_leds


def mirrorX(input_leds):
    for y in range(col):
        for x in range(row // 2):
            input_leds[fromXY(row - 1 - x, y)] = input_leds[fromXY(x, y)]
    return input_leds


def mirrorY(input_leds):
    for x in range(row):
        for y in range(col // 2):
            input_leds[fromXY(x, col - 1 - y)] = input_leds[fromXY(x, y)]
    return input_leds

# animations


def arrow(timePercent, iterations=1, ease=easing.gaussianFit):
    leds = [0] * col * row
    # draw one diagonal half of the arrow
    for i in range(len(leds) // 2):
        eval = timePercent * (iterations + 1.5) - 1.5 + \
            XY(i)[0] / row + XY(i)[1] / col
        if(eval > iterations or eval < 0):
            leds[i] = ease(clamp(eval))
        else:
            leds[i] = ease(clamp(eval % 1))
    # draw the other diagonal half of the arrow
    for i in range(len(leds) // 2, len(leds)):
        eval = timePercent * (iterations + 1.5) + \
            XY(i)[0] / row - 1.5 + (col - 1 - XY(i)[1]) / col
        if(eval > iterations or eval < 0):
            leds[i] = ease(clamp(eval))
        else:
            leds[i] = ease(clamp(eval % 1))
    return leds


def doubleArrow(timePercent, iterations=1, ease=easing.spikeSquare):
    leds = [0] * col * row
    # draw one diagonal half of the arrow
    for i in range(len(leds) // 4):
        eval = timePercent * (iterations + 1.50) - 1.5 + \
            XY(i)[0] / row + XY(i)[1] / col
        if(eval > iterations or eval < 0):
            leds[i] = ease(clamp(eval))
        else:
            leds[i] = ease(clamp(eval % 1))
    # draw the other diagonal half of the arrow
    for i in range(len(leds) // 4, len(leds)):
        eval = timePercent * (iterations + 1.5) + \
            XY(i)[0] / row - 2 + (col - 1 - XY(i)[1]) / col
        if(eval > iterations or eval < 0):
            leds[i] = ease(clamp(eval))
        else:
            leds[i] = ease(clamp(eval % 1))
    # flip the bottom half to get opposing arrows
    for x in range(row):
        for y in range(col // 2):
            leds[fromXY(row - 1 - x, col - 1 - y)] = leds[fromXY(x, y)]
    return leds


def diagonalWave(timePercent, iterations=1, ease=easing.gaussianFit):
    leds = [0] * col * row
    for i in range(len(leds)):
        eval = timePercent * (iterations + 2) - 2 + \
            XY(i)[0] / row + XY(i)[1] / col
        if(eval > iterations or eval < 0):
            leds[i] = ease(clamp(eval))
        else:
            leds[i] = ease(clamp(eval % 1))
    return leds


def wave(timePercent, iterations=1, ease=easing.gaussianFit):
    leds = [0] * col * row
    for i in range(len(leds)):
        eval = timePercent * (iterations + 1) - 1 + XY(i)[0] / row
        if(eval > iterations or eval < 0):
            leds[i] = ease(clamp(eval))
        else:
            leds[i] = ease(clamp(eval % 1))
    return leds


def squareInwardsSharp(timePercent, ease=easing.linear):
    leds = [0] * col * row
    eval = (timePercent * row) / 2
    for i in range(len(leds)):
        distFromCenter = max(abs((col - 1) / 2 - XY(i)[1]),
                             abs((row - 1) / 2 - XY(i)[0]))
        leds[i] = ease(clamp(eval - distFromCenter + 0.5))
    return leds


def squareInwards(timePercent, ease=easing.spikeInCubic):
    leds = [0] * col * row
    for i in range(len(leds)):
        distFromCenter = max(abs((col - 1) / 2 - XY(i)[1]),
                             abs((row - 1) / 2 - XY(i)[0]))
        leds[i] = ease(clamp(timePercent * 1.2 - distFromCenter / row))
    return leds


def curtain(timePercent, ease=easing.spikeInCubic):
    leds = [0] * col * row
    for i in range(len(leds)):
        distFromCenter = abs((row - 1) / 2 - XY(i)[0])
        leds[i] = ease(clamp(timePercent * 1.2 - distFromCenter / row))
    return leds


def circleInwards(timePercent, ease=easing.spikeInCubic):
    leds = [0] * col * row
    eval = timePercent * 1.4143  # hardcoded root(2)
    for i in range(len(leds)):
        dy = (col - 1) / 2 - XY(i)[1]
        dx = (col - 1) / 2 - XY(i)[0]
        distFromCenter = math.sqrt(dy * dy + dx * dx)
        leds[i] = ease(clamp(eval - distFromCenter / row))
    return leds


def circleInwardsSharp(timePercent, ease=easing.linear):
    leds = [0] * col * row
    eval = (timePercent * row * 1.4143) / 2  # hardcoded root(2)
    for i in range(len(leds)):
        dy = (col - 1) / 2 - XY(i)[1]
        dx = (col - 1) / 2 - XY(i)[0]
        distFromCenter = math.sqrt(dy * dy + dx * dx)
        leds[i] = ease(clamp(eval - distFromCenter + 0.5))
    return leds


def strobe(timePercent, ease=easing.triangle):
    return [clamp(ease(timePercent * 2))] * row * col


def zipper(timePercent, simultaneus=4):
    """the second parameter determines how many rows are moving at the same time"""
    leds = [0] * col * row

    for y in range(col):
        eval = timePercent * (col / simultaneus + 1) - y / simultaneus
        for x in range(row // 2):
            if(clamp(eval) == eval):
                leds[fromXY(x, y)] = easing.square(
                    eval * (row - 1) / 2 - x)
        if(eval < 0):
            leds[fromXY(0, y)] = 1
        if(eval > 1):
            leds[fromXY(row // 2 - 1, y)] = 1

    mirrorX(leds)
    return leds


gifPaths = ["animation8times4", "compress", "cross", "buildingCross8"]
listOfGifs = []
for gifPath in gifPaths:
    gifFile = Image.open("effectGifs/" + gifPath + ".gif")
    listOfGifs.append([])
    for frame in ImageSequence.Iterator(gifFile):
        listOfGifs[len(listOfGifs) - 1].append(frame.convert('RGB').getdata())


def gif(timePercent, gifIndex=0, colorMask=0):
    pos = math.floor(timePercent * len(listOfGifs[gifIndex]))
    return [i[colorMask] / 255 for i in list(listOfGifs[gifIndex][pos])]
