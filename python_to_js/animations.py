import math
import random

import environment as env

import easing
import gif

row = env.rows
col = env.cols
listOfGifs = gif.gifs

# helper functions


def overlay_border(leds, overlay=[0 for i in range(row*col)], width=1):
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
    if(value <= min):
        return min
    elif(value >= max):
        return max
    return value


def from_xy(x, y):
    return y * row + x


def xy(index):
    return [index % row, index // row]


def multiply(leds, mult):
    if isinstance(mult, list):
        return [leds[i] * mult[i] for i in range(len(leds))]
    # in case you want to pass time as multiplier, mod 1 necessary
    return [leds[i] * (mult % 1) for i in range(len(leds))]


def flipBottomHalf(leds):
    for x in range(row):
        for y in range(col // 2):
            leds[from_xy(row - 1 - x, col - 1 - y)] = leds[from_xy(x, y)]
    return leds


def ease_image(leds, ease=easing.linear):
    return [ease(i) for i in leds]


def flipLeftHalf(leds):
    for y in range(col):
        for x in range(row // 2, row):
            leds[from_xy(row - 1 - x, col - 1 - y)] = leds[from_xy(x, y)]
    return leds


def mask_rect(input_leds, fromx, tox, fromy, toy):
    leds = [0 for i in range(row*col)]
    fromx = clamp(fromx, 0, row)
    tox = clamp(tox, 0, row)
    fromy = clamp(fromy, 0, col)
    toy = clamp(toy, 0, col)
    for y in range(fromy, toy):
        for x in range(fromx, tox):
            leds[from_xy(x, y)] = input_leds[from_xy(x, y)]
    return leds


def flipEverySecondRow(input_leds):
    leds = input_leds.slice()
    for y in range(0, col, 2):
        for x in range(row):
            leds[from_xy(row - 1 - x, y)] = input_leds[from_xy(x, y)]
    return leds


def rotate90(input_leds, count=1):
    """rotates the given matrix by count 90deg increments"""
    count = (count + 4) % 4
    rotated_leds = [0 for i in range(row*col)]
    if count == 1:
        for i in range(len(input_leds)):
            # rotate 90 deg
            rotated_leds[from_xy(xy(i)[1], row - 1 - xy(i)[0])] = input_leds[i]
    elif count == 2:
        # rotate 180 deg
        rotated_leds = list(reversed(input_leds))

    elif count == 3:
        for i in range(len(input_leds)):
            # rotate -90 deg
            rotated_leds[i] = input_leds[from_xy(xy(i)[1], row - 1 - xy(i)[0])]
    elif count == 0:
        return input_leds
    return rotated_leds


def add(matrices):
    if len(matrices) == 0:
        return [0 for i in range(row*col)]
    return [sum(vals) if any(vals) else 0 for vals in zip(*matrices)]


def add_clamped(matrices):
    if len(matrices) == 0:
        return [0 for i in range(row*col)]
    return [clamp(sum(vals)) if any(vals) else 0 for vals in zip(*matrices)]


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
    leds = [0 for i in range(row*col)]
    time_percent = time_percent % 1
    # draw one diagonal half of the arrow
    for i in range(len(leds) // 2):
        param_res = time_percent * (iterations + 1.5) - 1.5 + \
            xy(i)[0] / row + xy(i)[1] / col
        if(param_res >= iterations or param_res < 0):
            leds[i] = ease(clamp(param_res))
        else:
            leds[i] = ease(clamp(param_res % 1))
    # draw the other diagonal half of the arrow
    for i in range(len(leds) // 2, len(leds)):
        param_res = time_percent * (iterations + 1.5) + \
            xy(i)[0] / row - 1.5 + (col - 1 - xy(i)[1]) / col
        if(param_res >= iterations or param_res < 0):
            leds[i] = ease(clamp(param_res))
        else:
            leds[i] = ease(clamp(param_res % 1))
    return leds


def doubleArrow(time_percent, iterations=1, ease=easing.spikeSquare):
    leds = [0 for i in range(row*col)]
    time_percent = time_percent % 1
    # draw one diagonal half of the arrow
    for i in range(len(leds) // 4):
        param_res = time_percent * (iterations + 1.50) - 1.5 + \
            xy(i)[0] / row + xy(i)[1] / col
        if(param_res >= iterations or param_res < 0):
            leds[i] = ease(clamp(param_res))
        else:
            leds[i] = ease(clamp(param_res % 1))
    # draw the other diagonal half of the arrow
    for i in range(len(leds) // 4, len(leds)):
        param_res = time_percent * (iterations + 1.5) + \
            xy(i)[0] / row - 2 + (col - 1 - xy(i)[1]) / col
        if(param_res >= iterations or param_res < 0):
            leds[i] = ease(clamp(param_res))
        else:
            leds[i] = ease(clamp(param_res % 1))
    return flipBottomHalf(leds)


def diagonal_wave(time_percent, ease=easing.gaussianFit, iterations=1):
    leds = [0 for i in range(row*col)]
    time_percent = time_percent % 1
    for i in range(len(leds)):
        param_res = time_percent * (iterations + 2) - 2 + \
            xy(i)[0] / row + xy(i)[1] / col
        if(param_res >= iterations or param_res < 0):
            leds[i] = ease(clamp(param_res))
        else:
            leds[i] = ease(clamp(param_res % 1))
    return leds


def wave(time_percent, iterations=1, ease=easing.gaussianFit):
    leds = [0 for i in range(row*col)]
    time_percent = time_percent % 1
    for i in range(len(leds)):
        param_res = time_percent * (iterations + 1) - 1 + xy(i)[0] / row
        if param_res >= iterations or param_res < 0:
            leds[i] = ease(clamp(param_res))
        else:
            leds[i] = ease(clamp(param_res % 1))
    return leds


def square_inwards_sharp(time_percent, ease=easing.square):
    leds = [0 for i in range(row*col)]
    time_percent = time_percent % 1
    param_res = (time_percent * row) / 2
    for i in range(len(leds)):
        dist_from_center = max(abs((col - 1) / 2 - xy(i)[1]),
                               abs((row - 1) / 2 - xy(i)[0]))
        leds[i] = ease(clamp(param_res - dist_from_center + 0.5))
    return leds


def square_inwards(time_percent, ease=easing.spikeInCubic, origin=((row - 1) / 2, (col - 1) / 2)):
    leds = [0 for i in range(row*col)]
    time_percent = time_percent % 1
    # get the longest distance our wave has to travel
    max_dist_origin = max(origin[1], origin[0],
                          col - origin[1], row - origin[0])
    # convert that to a percentage instead
    matrix_percent = row / max_dist_origin
    for i in range(len(leds)):
        dist_from_origin = max(abs(origin[1] - xy(i)[1]),
                               abs(origin[0] - xy(i)[0]))
        # moves slower the closer origin is to center (needs less time to fill matrix)
        leds[i] = ease(clamp(time_percent * 2 * matrix_percent -
                             dist_from_origin / max_dist_origin))
    return leds


def curtain(time_percent, ease=easing.spikeInCubic):
    leds = [0 for i in range(row*col)]
    time_percent = time_percent % 1
    for i in range(len(leds)):
        dist_from_center = abs((row - 1) / 2 - xy(i)[0])
        leds[i] = ease(clamp(time_percent * 1.2 - dist_from_center / row))
    return leds


def fill(time_percent, ease=easing.triangle, width=row, height=col):
    leds = [0 for i in range(row*col)]
    time_percent = time_percent % 1
    for x in range(width):
        for y in range(height):
            leds[from_xy(x, y)] = ease(time_percent)
    return leds


def cross(time_percent, ease=easing.linearCutoff):
    leds = [0 for i in range(row*col)]
    time_percent = time_percent % 1

    ratio_x = row // 3
    ratio_y = col // 3

    for y in range(col // 2):
        for x in range(ratio_x, row - (ratio_x)):
            leds[from_xy(x, y)] = ease(
                1 - clamp(time_percent * 2 - 1 + y / col))
    leds = add([leds, rotate90(leds, 1)])

    for y in range(ratio_y, col - (ratio_y)):
        for x in range(ratio_x, row - (ratio_x)):
            leds[from_xy(x, y)] = leds[from_xy(x, y)] * 0.5

    return mirrorX(mirrorY(leds))


def splitLines(time_percent):
    leds = [0 for i in range(row*col)]
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


def circle_inwards(time_percent, ease=easing.spikeInCubic, iterations=1, origin=((row - 1) / 2, (col - 1) / 2)):
    leds = [0 for i in range(row*col)]
    time_percent = time_percent % 1
    param_res = time_percent * (0.4143 + iterations)  # hardcoded root(2)

    for i in range(len(leds)):
        dy = origin[0] - xy(i)[1]
        dx = origin[1] - xy(i)[0]
        dist_from_center = (dy ** 2 + dx ** 2)**0.5
        if(param_res - dist_from_center / row > iterations or param_res - dist_from_center / row < 0):
            leds[i] = ease(clamp(param_res - dist_from_center / row))
        else:
            leds[i] = ease(clamp((param_res - dist_from_center / row) % 1))
    return leds


def strobe(time_percent, ease=easing.triangle, time_factor=2):
    time_percent = time_percent % 1
    return [clamp(ease(time_percent * time_factor))] * row * col


def zipper(time_percent, simultaneus=4):
    """the second parameter determines how many rows are moving at the same time"""
    leds = [0 for i in range(row*col)]
    time_percent = time_percent % 1
    for y in range(col):
        param_res = time_percent * (col / simultaneus + 1) - y / simultaneus
        for x in range(row // 2):
            if(clamp(param_res) == param_res):
                leds[from_xy(x, y)] = easing.square(
                    param_res * (row - 1) / 2 - x)
        if(param_res < 0):
            leds[from_xy(0, y)] = 1
        if(param_res > 1):
            leds[from_xy(row // 2 - 1, y)] = 1

    mirrorX(leds)
    return leds


def gif(time_percent, gifName="compress", colorMask=0):
    pos = int((time_percent % 1) * len(listOfGifs[gifName]))
    return [i[colorMask] for i in list(listOfGifs[gifName][pos])]


def dissolve_random(time_percent, ease=easing.linear):
    leds = [random.random() + 1 - time_percent * 2 % 2
            for i in range(col * row)]
    return [ease(clamp(led)) for led in leds]


def draw_line(x0, y0, x1, y1):
    leds = [0 for i in range(row*col)]
  # implementation of breshams line draw algorithm
    dx = x1 - x0
    dy = y1 - y0

    xsign = 1 if dx > 0 else -1
    ysign = 1 if dy > 0 else -1

    dx = abs(dx)
    dy = abs(dy)

    if dx > dy:
        xx, xy, yx, yy = xsign, 0, 0, ysign
    else:
        dx, dy = dy, dx
        xx, xy, yx, yy = 0, ysign, xsign, 0

    D = 2 * dy - dx
    y = 0

    for x in range(dx + 1):
        lx = x0 + x * xx + y * yx
        ly = y0 + x * xy + y * yy

        if ly == clamp(ly, 0, col - 1) and lx == clamp(lx, 0, row - 1):
            leds[from_xy(lx, ly)] = 1
        if D >= 0:
            y += 1
            D -= 2 * dx
        D += 2 * dy

    return leds


def clock(time_percent):
    time_percent = time_percent % 1
    l1 = draw_line(row // 2, col // 2, row // 2 + int(row * math.sin(time_percent * math.pi)),
                   col // 2 + int(-col * math.cos(time_percent * math.pi)))
    l2 = draw_line(row // 2, col // 2, row // 2 + int(-row * math.sin(time_percent * math.pi)),
                   col // 2 + int(col * math.cos(time_percent * math.pi)))
    return add_clamped([l1, l2])


def fill_triangle(time_percent, corner=0):
    time_percent = time_percent % 1
    if corner == 0:
        l1 = draw_line(0, 0, int(2 * row * math.sin(time_percent * math.pi / 2)),
                       int(2 * col * math.cos(time_percent * math.pi / 2)))
        l1 = fill_empty(l1, 1)
    elif corner == 1:
        l1 = draw_line(row, 0, row - 1 - int(2 * row * math.sin(time_percent * math.pi / 2)),
                       int(2 * col * math.cos(time_percent * math.pi / 2)))
        l1 = fill_empty(l1)
    return l1


def fill_empty(input_leds, corner=0):
    if corner % 4 == 0:
        for x in range(row):
            for y in range(col):
                if input_leds[from_xy(x, y)] == 1:
                    break
                input_leds[from_xy(x, y)] = 1
    elif corner % 4 == 1:
        for y in range(col):
            for x in range(row):
                if input_leds[from_xy(x, y)] == 1:
                    break
                input_leds[from_xy(x, y)] = 1

    elif corner % 4 == 2:
        for y in range(col):
            for x in reversed(list(range(row))):
                if input_leds[from_xy(x, y)] == 1:
                    break
                input_leds[from_xy(x, y)] = 1

    elif corner % 4 == 3:
        for y in range(col):
            for x in reversed(list(range(row))):
                if input_leds[from_xy(x, y)] == 1:
                    break
                input_leds[from_xy(x, y)] = 1
    return input_leds


def snowflake(time_percent, x, y, fade=8):
    leds = [0 for i in range(row*col)]
    y = int(time_percent * 2 * col) - y - fade
    for i in range(1, fade + 1):
        yi = y + i
        if yi >= 0 and yi < col:
            leds[from_xy(x, yi)] = 1 - 1 / i
    return leds


def dissolve(time_percent, random_leds, number_of_steps=1, ease=easing.linear):
    time_percent = time_percent % 1
    return [ease(clamp(1 + led * number_of_steps - time_percent * (1 + number_of_steps))) for led in random_leds]
