import math
import random

from PIL import Image, ImageDraw, ImageFont, ImageOps, ImageSequence

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


def arrow(time_percent, iterations=1, ease=easing.gaussianFit):
    leds = [0] * col * row
    time_percent = time_percent % 1
    # draw one diagonal half of the arrow
    for i in range(len(leds) // 2):
        eval = time_percent * (iterations + 1.5) - 1.5 + \
            xy(i)[0] / row + xy(i)[1] / col
        if(eval > iterations or eval < 0):
            leds[i] = ease(clamp(eval))
        else:
            leds[i] = ease(clamp(eval % 1))
    # draw the other diagonal half of the arrow
    for i in range(len(leds) // 2, len(leds)):
        eval = time_percent * (iterations + 1.5) + \
            xy(i)[0] / row - 1.5 + (col - 1 - xy(i)[1]) / col
        if(eval > iterations or eval < 0):
            leds[i] = ease(clamp(eval))
        else:
            leds[i] = ease(clamp(eval % 1))
    return leds


def doubleArrow(time_percent, iterations=1, ease=easing.spikeSquare):
    leds = [0] * col * row
    time_percent = time_percent % 1
    # draw one diagonal half of the arrow
    for i in range(len(leds) // 4):
        eval = time_percent * (iterations + 1.50) - 1.5 + \
            xy(i)[0] / row + xy(i)[1] / col
        if(eval > iterations or eval < 0):
            leds[i] = ease(clamp(eval))
        else:
            leds[i] = ease(clamp(eval % 1))
    # draw the other diagonal half of the arrow
    for i in range(len(leds) // 4, len(leds)):
        eval = time_percent * (iterations + 1.5) + \
            xy(i)[0] / row - 2 + (col - 1 - xy(i)[1]) / col
        if(eval > iterations or eval < 0):
            leds[i] = ease(clamp(eval))
        else:
            leds[i] = ease(clamp(eval % 1))
    return flipBottomHalf(leds)


def diagonalWave(time_percent, iterations=1, ease=easing.gaussianFit):
    leds = [0] * col * row
    time_percent = time_percent % 1
    for i in range(len(leds)):
        eval = time_percent * (iterations + 2) - 2 + \
            xy(i)[0] / row + xy(i)[1] / col
        if(eval > iterations or eval < 0):
            leds[i] = ease(clamp(eval))
        else:
            leds[i] = ease(clamp(eval % 1))
    return leds


def wave(time_percent, iterations=1, ease=easing.gaussianFit):
    leds = [0] * col * row
    time_percent = time_percent % 1
    for i in range(len(leds)):
        eval = time_percent * (iterations + 1) - 1 + xy(i)[0] / row
        if(eval > iterations or eval < 0):
            leds[i] = ease(clamp(eval))
        else:
            leds[i] = ease(clamp(eval % 1))
    return leds


def squareInwardsSharp(time_percent, ease=easing.linear):
    leds = [0] * col * row
    time_percent = time_percent % 1
    eval = (time_percent * row) / 2
    for i in range(len(leds)):
        distFromCenter = max(abs((col - 1) / 2 - xy(i)[1]),
                             abs((row - 1) / 2 - xy(i)[0]))
        leds[i] = ease(clamp(eval - distFromCenter + 0.5))
    return leds


def squareInwards(time_percent, ease=easing.spikeInCubic):
    leds = [0] * col * row
    time_percent = time_percent % 1
    for i in range(len(leds)):
        distFromCenter = max(abs((col - 1) / 2 - xy(i)[1]),
                             abs((row - 1) / 2 - xy(i)[0]))
        leds[i] = ease(clamp(time_percent * 1.2 - distFromCenter / row))
    return leds


def curtain(time_percent, ease=easing.spikeInCubic):
    leds = [0] * col * row
    time_percent = time_percent % 1
    for i in range(len(leds)):
        distFromCenter = abs((row - 1) / 2 - xy(i)[0])
        leds[i] = ease(clamp(time_percent * 1.2 - distFromCenter / row))
    return leds


def fill(time_percent, ease=easing.triangle, width=16, height=16):
    leds = [0] * col * row
    time_percent = time_percent % 1
    for x in range(width):
        for y in range(height):
            leds[from_xy(x, y)] = ease(time_percent)
    return leds


def cross(time_percent, ease=easing.linearCutoff):
    leds = [0] * col * row
    time_percent = time_percent % 1

    ratio_x = row // 3
    ratio_y = col // 3

    for y in range(col // 2):
        for x in range(ratio_x, row - (ratio_x)):
            leds[from_xy(x, y)] = ease(
                1 - clamp(time_percent * 2 - 1 + y / col))
    leds = add(leds, rotateMatrix90(leds, 1))

    for y in range(ratio_y, col - (ratio_y)):
        for x in range(ratio_x, row - (ratio_x)):
            leds[from_xy(x, y)] = leds[from_xy(x, y)] * 0.5

    return mirrorX(mirrorY(leds))


def splitLines(time_percent):
    leds = [0] * col * row
    time_percent = time_percent % 1
    if time_percent < 0.5:
        def ease(t): return 1 if t <= 1 / 16 and t > 0 else 0
        for y in range(col // 2):
            for x in range(row):
                leds[from_xy(x, y)] = ease(time_percent - y / col)
        mirrorY(leds)
        return leds
    else:
        def ease(t): return 1 if t <= 1 / 8 and t > 0 else 0
        for y in range(col):
            for x in range(row):
                leds[from_xy(x, y)] = ease(time_percent - y / col + 1 / 16)
        return flipLeftHalf(leds)


def circle_inwards(time_percent, ease=easing.spikeInCubic):
    leds = [0] * col * row
    time_percent = time_percent % 1
    eval = time_percent * 1.4143  # hardcoded root(2)
    for i in range(len(leds)):
        dy = (col - 1) / 2 - xy(i)[1]
        dx = (col - 1) / 2 - xy(i)[0]
        distFromCenter = math.sqrt(dy * dy + dx * dx)
        leds[i] = ease(clamp(eval - distFromCenter / row))
    return leds


def strobe(time_percent, ease=easing.triangle, time_factor=2):
    time_percent = time_percent % 1
    return [clamp(ease(time_percent * time_factor))] * row * col


def zipper(time_percent, simultaneus=4):
    """the second parameter determines how many rows are moving at the same time"""
    leds = [0] * col * row
    time_percent = time_percent % 1
    for y in range(col):
        eval = time_percent * (col / simultaneus + 1) - y / simultaneus
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


def img_to_normalized_list(img):
    return [(i[0] / 255, i[1] / 255, i[2] / 255,)for i in list(img.getdata())]


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
            border_width = row - rgb_frame.size[0]
            border_height = col - rgb_frame.size[1]
            border = (border_height + border_width) // 4
            rgb_frame = ImageOps.expand(rgb_frame, border=border, fill='black')

            # normalize the colors from 8bit int to floats in the range 0-1
            normalizedFrame = img_to_normalized_list(rgb_frame)
            listOfGifs[gifPath].append(normalizedFrame)
    # print("following GIFs have been loaded:", gifPaths)


def gif(time_percent, gifName="compress", colorMask=0):
    pos = math.floor((time_percent % 1) * len(listOfGifs[gifName]))
    return [i[colorMask] for i in list(listOfGifs[gifName][pos])]


def dissolve_random(time_percent, ease=easing.linear):
    leds = [random.random() + 1 - time_percent * 2 % 2
            for i in range(col * row)]
    return [ease(clamp(led)) for led in leds]


def dissolve_ordered(time_percent=0, ease=easing.linear, randomize=False):
    if randomize or not hasattr(dissolve_ordered, 'random_leds'):
        dissolve_ordered.random_leds = random.sample(
            list(range(row * col)), row * col)  # creates a shuffled list with all numbers from range(row*col)
        return dissolve_ordered.random_leds
    return [ease(clamp(led - (time_percent % 1) * row * col)) for led in dissolve_ordered.random_leds]


def dissolve(time_percent=0, ease=easing.linear, randomize=False):
    if randomize or not hasattr(dissolve, 'random_leds'):
        dissolve.random_leds = [random.random() + 1 for i in range(col * row)]
        return dissolve.random_leds
    return [ease(clamp(led - time_percent * 2 % 2)) for led in dissolve.random_leds]


def text(time_percent, string="0", position=(0, 3)):
    img = Image.new('1', (row, col), color='black')
    ImageDraw.Draw(img).text(position,  string, 1)
    return list(img.getdata())
