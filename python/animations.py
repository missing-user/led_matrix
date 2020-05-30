import math

import easing

row = 16
col = 16


def clamp(value, min=0, max=1):
    if(value < min):
        return min
    elif(value > max):
        return max
    return value


def fromXY(x, y):
    return y * row + x


def XY(index):
    return [index % row, math.floor(index / row)]


def arrow(timePercent, iterations=1, ease=easing.gaussianFit):
    leds = [0] * col * row
    # draw one diagonal half of the arrow
    for i in range(len(leds) / 2):
        eval = timePercent * (iterations + 1.5) - \
            1.5 + XY(i)[0] / row + XY(i)[1] / col
        if(eval > iterations):
            leds[i] = ease(clamp(eval))
        else:
            leds[i] = ease(clamp(eval % 1))
    # draw the other diagonal half of the arrow
    for i in range(len(leds) / 2, len(leds)):
        eval = timePercent * (iterations + 1.5) + \
            XY(i)[0] / row - 1.5 + (col - 1 - XY(i)[1]) / col
        if(eval > iterations):
            leds[i] = ease(clamp(eval))
        else:
            leds[i] = ease(clamp(eval % 1))
    return leds


def diagonalWave(timePercent, iterations=1, ease=easing.gaussianFit):
    leds = [0] * col * row
    for i in range(len(leds)):
        eval = timePercent * (iterations + 2) - 2 + \
            XY(i)[0] / row + XY(i)[1] / col
        if(eval > iterations):
            leds[i] = ease(clamp(eval))
        else:
            leds[i] = ease(clamp(eval % 1))
    return leds


def wave(timePercent, iterations=1, ease=easing.gaussianFit):
    leds = [0] * col * row
    for i in range(len(leds)):
        eval = timePercent * (iterations + 1) - 1 + XY(i)[0] / row
        if(eval > iterations):
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
    leds = [0] * col * row
    for led in leds:
        led = clamp(ease(timePercent * 2))
    return leds
