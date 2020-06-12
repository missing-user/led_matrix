import math

from PIL import Image, ImageOps, ImageSequence

import easing

# helper functions


def overlay_border(leds, overlay, width=1):
    for y in range(col):
        for x in range(width):
            leds[from_xy(x, y)] = overlay[from_xy(x, y)]

    for y in range(width):
        for x in range(row):
            leds[from_xy(x, y)] = overlay[from_xy(x, y)]

    for y in range(col - width, col):
        for x in range(row):
            leds[from_xy(x, y)] = overlay[from_xy(x, y)]

    for y in range(col):
        for x in range(row - width, row):
            leds[from_xy(x, y)] = overlay[from_xy(x, y)]
    return leds


def clamp(value, min=0, max=1):
    if(value < min):
        return min
    elif(value > max):
        return max
    return value


def from_xy(x, y):
    return y * row + x


def xy(index):
    return [index % row, index // row]


def multiply(leds, mult):
    if isinstance(mult, list):
        return [leds[i] * mult[i] for i in range(len(leds))]
    return [leds[i] * (mult % 1) for i in range(len(leds))]


def flipBottomHalf(leds):
    for x in range(row):
        for y in range(col // 2):
            leds[from_xy(row - 1 - x, col - 1 - y)] = leds[from_xy(x, y)]
    return leds


def flipLeftHalf(leds):
    for y in range(col):
        for x in range(row // 2, row):
            leds[from_xy(row - 1 - x, col - 1 - y)] = leds[from_xy(x, y)]
    return leds


def maskCorner(leds, corner=0):
    for y in range(col // 2):
        for x in range(row // 2):
            if not corner == 0:
                leds[from_xy(x, y)] = 0

    for y in range(col // 2):
        for x in range(row // 2, row):
            if not corner == 1:
                leds[from_xy(x, y)] = 0

    for y in range(col // 2, col):
        for x in range(row // 2, row):
            if not corner == 2:
                leds[from_xy(x, y)] = 0

    for y in range(col // 2, col):
        for x in range(row // 2):
            if not corner == 3:
                leds[from_xy(x, y)] = 0
    return leds


def flipEverySecondRow(input_leds):
    leds = input_leds.copy()
    for y in range(0, col, 2):
        for x in range(row):
            leds[from_xy(row - 1 - x, y)] = input_leds[from_xy(x, y)]
    return leds


def rotateMatrix90(input_leds, count=1):
    """rotates the given matrix by count 90deg increments"""
    count = (count + 4) % 4
    rotated_leds = input_leds.copy()
    if count == 1:
        for i in range(len(input_leds)):
            # rotate 90 deg
            rotated_leds[from_xy(xy(i)[1], row - 1 - xy(i)[0])] = input_leds[i]
    elif count == 2:
        for i in range(len(input_leds)):
            # rotate 90 deg
            rotated_leds[from_xy(row - 1 - xy(i)[0], col -
                                 1 - xy(i)[1])] = input_leds[i]

    elif count == 3:
        for i in range(len(input_leds)):
            # rotate 90 deg
            rotated_leds[i] = input_leds[from_xy(xy(i)[1], row - 1 - xy(i)[0])]
    elif count == 0:
        return input_leds
    return rotated_leds


def add(matrix1, matrix2):
    return[matrix1[i] + matrix2[i] for i in range(len(matrix1))]


def add_clamped(matrices):
    if len(matrices) > 0:
        result = [0] * len(matrices[0])
    else:
        result = [0] * row * col
    for i in range(len(result)):
        for matrix in matrices:
            result[i] += matrix[i]
        result[i] = clamp(result[i])
    return result
    return[matrix1[i] + matrix2[i] for i in range(len(matrix1))]


def mirrorX(input_leds):
    for y in range(col):
        for x in range(row // 2):
            input_leds[from_xy(row - 1 - x, y)] = input_leds[from_xy(x, y)]
    return input_leds


def mirrorY(input_leds):
    for x in range(row):
        for y in range(col // 2):
            input_leds[from_xy(x, col - 1 - y)] = input_leds[from_xy(x, y)]
    return input_leds

# animations


def arrow(timePercent, iterations=1, ease=easing.gaussianFit):
    leds = [0] * col * row
    timePercent = timePercent % 1
    # draw one diagonal half of the arrow
    for i in range(len(leds) // 2):
        eval = timePercent * (iterations + 1.5) - 1.5 + \
            xy(i)[0] / row + xy(i)[1] / col
        if(eval > iterations or eval < 0):
            leds[i] = ease(clamp(eval))
        else:
            leds[i] = ease(clamp(eval % 1))
    # draw the other diagonal half of the arrow
    for i in range(len(leds) // 2, len(leds)):
        eval = timePercent * (iterations + 1.5) + \
            xy(i)[0] / row - 1.5 + (col - 1 - xy(i)[1]) / col
        if(eval > iterations or eval < 0):
            leds[i] = ease(clamp(eval))
        else:
            leds[i] = ease(clamp(eval % 1))
    return leds


def doubleArrow(timePercent, iterations=1, ease=easing.spikeSquare):
    leds = [0] * col * row
    timePercent = timePercent % 1
    # draw one diagonal half of the arrow
    for i in range(len(leds) // 4):
        eval = timePercent * (iterations + 1.50) - 1.5 + \
            xy(i)[0] / row + xy(i)[1] / col
        if(eval > iterations or eval < 0):
            leds[i] = ease(clamp(eval))
        else:
            leds[i] = ease(clamp(eval % 1))
    # draw the other diagonal half of the arrow
    for i in range(len(leds) // 4, len(leds)):
        eval = timePercent * (iterations + 1.5) + \
            xy(i)[0] / row - 2 + (col - 1 - xy(i)[1]) / col
        if(eval > iterations or eval < 0):
            leds[i] = ease(clamp(eval))
        else:
            leds[i] = ease(clamp(eval % 1))
    return flipBottomHalf(leds)


def diagonalWave(timePercent, iterations=1, ease=easing.gaussianFit):
    leds = [0] * col * row
    timePercent = timePercent % 1
    for i in range(len(leds)):
        eval = timePercent * (iterations + 2) - 2 + \
            xy(i)[0] / row + xy(i)[1] / col
        if(eval > iterations or eval < 0):
            leds[i] = ease(clamp(eval))
        else:
            leds[i] = ease(clamp(eval % 1))
    return leds


def wave(timePercent, iterations=1, ease=easing.gaussianFit):
    leds = [0] * col * row
    timePercent = timePercent % 1
    for i in range(len(leds)):
        eval = timePercent * (iterations + 1) - 1 + xy(i)[0] / row
        if(eval > iterations or eval < 0):
            leds[i] = ease(clamp(eval))
        else:
            leds[i] = ease(clamp(eval % 1))
    return leds


def squareInwardsSharp(timePercent, ease=easing.linear):
    leds = [0] * col * row
    timePercent = timePercent % 1
    eval = (timePercent * row) / 2
    for i in range(len(leds)):
        distFromCenter = max(abs((col - 1) / 2 - xy(i)[1]),
                             abs((row - 1) / 2 - xy(i)[0]))
        leds[i] = ease(clamp(eval - distFromCenter + 0.5))
    return leds


def squareInwards(timePercent, ease=easing.spikeInCubic):
    leds = [0] * col * row
    timePercent = timePercent % 1
    for i in range(len(leds)):
        distFromCenter = max(abs((col - 1) / 2 - xy(i)[1]),
                             abs((row - 1) / 2 - xy(i)[0]))
        leds[i] = ease(clamp(timePercent * 1.2 - distFromCenter / row))
    return leds


def curtain(timePercent, ease=easing.spikeInCubic):
    leds = [0] * col * row
    timePercent = timePercent % 1
    for i in range(len(leds)):
        distFromCenter = abs((row - 1) / 2 - xy(i)[0])
        leds[i] = ease(clamp(timePercent * 1.2 - distFromCenter / row))
    return leds


def fill(timePercent, ease=easing.triangle, width=16, height=16):
    leds = [0] * col * row
    timePercent = timePercent % 1
    for x in range(width):
        for y in range(height):
            leds[from_xy(x, y)] = ease(timePercent)
    return leds


def cross(timePercent, ease=easing.linearCutoff):
    leds = [0] * col * row
    timePercent = timePercent % 1

    ratio_x = 3 * row // 8
    ratio_y = 3 * col // 8

    for y in range(col // 2):
        for x in range(ratio_x, row - (ratio_x)):
            leds[from_xy(x, y)] = ease(
                1 - clamp(timePercent * 2 - 1 + y / col))
    leds = add(leds, rotateMatrix90(leds, 1))

    for y in range(ratio_y, col - (ratio_y)):
        for x in range(ratio_x, row - (ratio_x)):
            leds[from_xy(x, y)] = leds[from_xy(x, y)] * 0.5

    return mirrorX(mirrorY(leds))


def splitLines(timePercent):
    leds = [0] * col * row
    timePercent = timePercent % 1
    if timePercent < 0.5:
        def ease(t): return 1 if t <= 1 / 16 and t > 0 else 0
        for y in range(col // 2):
            for x in range(row):
                leds[from_xy(x, y)] = ease(timePercent - y / col)
        mirrorY(leds)
        return leds
    else:
        def ease(t): return 1 if t <= 1 / 8 and t > 0 else 0
        for y in range(col):
            for x in range(row):
                leds[from_xy(x, y)] = ease(timePercent - y / col + 1 / 16)
        return flipLeftHalf(leds)


def circle_inwards(timePercent, ease=easing.spikeInCubic):
    leds = [0] * col * row
    timePercent = timePercent % 1
    eval = timePercent * 1.4143  # hardcoded root(2)
    for i in range(len(leds)):
        dy = (col - 1) / 2 - xy(i)[1]
        dx = (col - 1) / 2 - xy(i)[0]
        distFromCenter = math.sqrt(dy * dy + dx * dx)
        leds[i] = ease(clamp(eval - distFromCenter / row))
    return leds


def strobe(timePercent, ease=easing.triangle):
    timePercent = timePercent % 1
    return [clamp(ease(timePercent * 2))] * row * col


def zipper(timePercent, simultaneus=4):
    """the second parameter determines how many rows are moving at the same time"""
    leds = [0] * col * row
    timePercent = timePercent % 1
    for y in range(col):
        eval = timePercent * (col / simultaneus + 1) - y / simultaneus
        for x in range(row // 2):
            if(clamp(eval) == eval):
                leds[from_xy(x, y)] = easing.square(
                    eval * (row - 1) / 2 - x)
        if(eval < 0):
            leds[from_xy(0, y)] = 1
        if(eval > 1):
            leds[from_xy(row // 2 - 1, y)] = 1

    mirrorX(leds)
    return leds


def load_gifs():
    gifPaths = ["compress", "cross", "buildingCross8", "dithered45degSquare", "buildArrows", "compressingLines",
                "rotatingLines", "stonehengeToBorder", "buildTiles", "dot", "symTriangle", "fourGradientsLinearSpin", "spiral16", "staticFrames"]
    global listOfGifs
    listOfGifs = {}
    print("loading GIFs")
    for gifPath in gifPaths:
        gifFile = Image.open("effectGifs/" + gifPath + ".gif")
        listOfGifs[gifPath] = []
        for frame in ImageSequence.Iterator(gifFile):
            rgb_frame = frame.convert('RGB')
            # in case of mismatch between gif and matrix resolution, add border
            border_width = row - 1 - rgb_frame.size[0]
            border_height = col - 1 - rgb_frame.size[1]
            border = (border_height + border_width) // 2
            rgb_frame = ImageOps.expand(rgb_frame, border=border, fill='black')

            # normalize the colors from 8bit int to floats in the range 0-1
            normalizedFrame = [(i[0] / 255, i[1] / 255, i[2] / 255,)
                               for i in list(rgb_frame.getdata())]
            listOfGifs[gifPath].append(normalizedFrame)
    # print("following GIFs have been loaded:", gifPaths)


def gif(timePercent, gifName="compress", colorMask=0):
    pos = math.floor((timePercent % 1) * len(listOfGifs[gifName]))
    return [i[colorMask] for i in list(listOfGifs[gifName][pos])]
