import random

import environment as env

import easing
from animations import *
import effect_list

row = env.rows
col = env.cols


def makeRegistrar():
    """adds all funcs with this decorator to a list"""
    registry = []

    def registrar(func):
        registry.append(func)
        return func
    registrar.all = registry
    return registrar


reg = makeRegistrar()


def simple_factory(func):
    def factory():
        return func
    return factory


def properties(elength, intensity=None):  # decorator factory
    """decorator that returns the length of an animation chain in beats"""
    def decorator(func):  # decorator
        func.elength=elength

        if intensity != None:
            func.intensity=intensity
        return func

    return decorator


@reg
def snowflake_single_factory(x=None, y=None):
    if not x:
        x = random.choice(range(row))
    else:
        x = clamp(x, 0, row - 1)
    if not y:
        y = random.choice(range(col))
    else:
        y = clamp(y, 0, col - 1)

    @properties(elength=2)
    def snowflake_single(time):
        return snowflake(time, x, y)
    return snowflake_single


@reg
def snowflake_multiple_factory():
    count = random.choice(range(row // 4, row))
    methods = [snowflake_single_factory() for i in range(count)]

    @properties(elength=2)
    def snowflake_multiple(time):
        matrices = [method(time) for method in methods]
        return add_clamped(matrices)
    return snowflake_multiple


@reg
@simple_factory
@properties(elength=12)
def dithered_diamond(time):
    if time < 4:
        return gif(time / 4, "dithered45degSquare")
    elif time < 6:
        return multiply(splitLines(time / 2), time / 2)
    elif time < 9:
        return gif(time / 3, "buildArrows")
    elif time < 10:
        effectResult = doubleArrow(
            time / 2 + 1, 1, lambda t: 0 if t * 6 % 1 == t * 6 % 2 else 1)
        return rotate90(effectResult, 1)
    elif time < 11:
        return diagonal_wave(1 - time, easing.square)
    return diagonal_wave(time, easing.square)


dsc_list = effect_list.Effect_List()
dsc_list.add(effect_list.timed(diagonal_wave, 0, 3),
             effect_list.timed(lambda t: diagonal_wave(t, easing.easeOutQuad), 3, 1),
             effect_list.timed(lambda t: square_inwards(t, easing.easeOutCubic), 4, 1),
             effect_list.timed(square_inwards, 5, 3),
             effect_list.timed(lambda t: square_inwards(
                 easing.triangle(t / 2), easing.easeOutQuad), 8, 2),
             effect_list.timed(lambda t: mirrorX(mirrorY(diagonal_wave(-t))), 10, 6))


@reg
@simple_factory
@properties(elength=16)
def diamond_square_compress(time):
    return dsc_list.get_current(time)[0]


@reg
@simple_factory
@properties(elength=16, intensity=True)
def cross_routine(time):
    if time < 4:
        return cross(time, easing.square)
    elif time < 12:
        # cross with strobing squares in all 4 corners
        filledCorners = mirrorX(
            mirrorY(fill(clamp((time % 1) * 2 - 1), width=4, height=4)))
        return add_clamped([cross(time), filledCorners])
    elif time < 13:
        # two waves moving in oposite directions
        return rotate90(flipBottomHalf(wave(time)), 1)
    elif time < 14:
        # same as above, but 90deg rotated
        return flipBottomHalf(wave(time))
    return strobe(time * 3)


@reg
@simple_factory
@properties(elength=7)
def stonehenge_routine(time):
    if time < 1:
        return gif(time, "compressingLines")
    elif time < 4:
        # the rotating lines gif is 6 beats long
        return gif((time - 1) / 3, "rotatingLines")
    elif time < 5:
        return gif(time, "stonehengeToBorder")
    return overlay_border([0 for i in range(row*col)], square_inwards(time, easing.inverse), 2)


@reg
@simple_factory
@properties(elength=8, intensity=True)
def flipped_lines(time):
    if time < 4:
        return gif(time, "symTriangle")
    elif (time % 2) <= 1:
        return rotate90(flipEverySecondRow(wave(time, 1, easing.spikeInCubic)), 1)
    else:
        return flipEverySecondRow(wave(time, 1, easing.spikeInCubic))


audc_list = effect_list.Effect_List()
audc_list.add(effect_list.timed(lambda t: rotate90(arrow(-t)), 0, 1),
              effect_list.timed(lambda t: rotate90(arrow(t / 3, 4)), 1, 3),
              effect_list.timed(lambda t: curtain(-t), 4, 2),
              effect_list.timed(lambda t: rotate90(wave(t / 2)), 6, 2))


@reg
@simple_factory
@properties(elength=8)
def arrow_up_down_curtain(time):
    return audc_list.get_current(time)[0]


@reg
@simple_factory
@properties(elength=6)
def build_wipe_corners(time):
    diamond = mirrorX(mirrorY(diagonal_wave(time)))
    if time < 1:
        return gif(time, "buildTiles")
    elif time < 2:
        return rotate90(curtain(time, easing.spikeSquare), 1)
    elif time < 3:
        return mask_rect(diamond, 0, row // 2, 0, col // 2)  # corner NW
    elif time < 4:
        return mask_rect(diamond, row // 2, row, 0, col // 2)  # corner NE
    elif time < 5:
        return mask_rect(diamond, row // 2, row, col // 2, col)
    elif time < 6:
        return mask_rect(diamond, 0, row // 2, col // 2, col)


@reg
@simple_factory
@properties(elength=6)
def dot_and_square(time):
    if time % 2 <= 1:
        return gif(time, "dot")
    return square_inwards_sharp(time)


@reg
@simple_factory
@properties(elength=4)
def cross_flipper(time):
    if time >= 1 and time < 2:
        return cross(-time, easing.spikeInCubic)
    return cross(time, easing.spikeInCubic)


@reg
def diagonal_masked_factory():
    masks = random.choice(['triangleMasks', 'borderMasks', 'ditheredMasks'])

    @properties(elength=10)
    def masked_factory_child(time):
        m = gif(0, masks)
        inv_m = ease_image(m, easing.inverse)
        diagonal_arrow = multiply(square_inwards(time, origin=(0, 0)), inv_m)
        if time < 1:
            return multiply(rotate90(diagonal_wave(time, easing.linear)), m)
        if time < 5:
            return add([diagonal_arrow, m])
        if time < 6:
            return multiply(diagonal_wave(time, easing.inverse), m)
        if time < 9:
            return rotate90(diagonal_arrow, 3)
        return rotate90(multiply(diagonal_wave(time), m))
    return masked_factory_child


@reg
def fancy_diagonal_masked_factory():
    masks = random.choice(['triangleMasks', 'triangleMasks', 'borderMasks', 'ditheredMasks'])
    rot = random.randint(0, 4)

    @properties(elength=10)
    def fancy_masked_factory_child(time):
        m = gif(0, masks)
        inv_m = ease_image(m, easing.inverse)
        def diagonal_arrow(t, e): return multiply(square_inwards(t, origin=(0, 0), ease=e), inv_m)
        if time < 1:
            return diagonal_arrow(time, easing.easeInCubic)
        elif time < 3:
            return add_clamped([diagonal_wave(time), inv_m])
        elif time < 4:
            return multiply(rotate90(diagonal_wave(time, easing.easeOutCubic)), inv_m)
            # return diagonal_arrow(time, easing.easeOutCubic)
        elif time < 5:
            return rotate90(diagonal_arrow(time, easing.easeInCubic), 3)
        elif time < 6:
            return rotate90(add_clamped([inv_m, diagonal_wave(time, easing.easeInCubic)]))
        elif time < 10:
            static_mask = rotate90(fill(0.5, easing.triangle, row,
                                   col - col * (int(time - 6) + 1) // 4), 2)
            moving_stripe = mask_rect(wave(time, 1, easing.inverse), 0, row,
                                      col * int(time - 6) // 4, col * (int(time - 6) + 1) // 4)
            return rotate90(add_clamped([static_mask, moving_stripe]), rot)
        return diagonal_arrow(time, easing.spikeInCubic)
    return fancy_masked_factory_child


@reg
@simple_factory
@properties(elength=32, intensity=True)
def chain10(time):
    if time < 8:
        return circle_inwards(time / 4, easing.spikeInOutCubic, 4)
    elif time < 12:
        return rotate90(curtain(easing.triangle(time / 2)), 1)
    elif time < 16:
        return curtain(easing.triangle(time / 2))
    elif time < 20:
        return strobe(time)
    elif time < 24:
        return multiply(gif(time, "compress"), time)
    elif time < 28:
        return circle_inwards(easing.triangle(time / 2 % 1), easing.linear)
    return circle_inwards(-time)


@reg
@simple_factory
@properties(elength=28, intensity=True)
def flashing_corners(time):
    if time < 8:
        return rotate90(arrow(time, 2), int(time))
    elif time < 12:
        return square_inwards_sharp(time)
    elif time < 16:
        return rotate90(fill(time * 2, width=row // 2, height=col // 2), int(time))
    elif time < 20:
        return gif(time, "fourGradientsLinearSpin")
    return rotate90(gif(time, "spiral16"), 2 * int(time))


def sample(listt, repeat):
    resultingList = []
    for i in range(repeat):
        listt[Math.floor(Math.random() * listt.length)]
    return resultingList

@reg
@simple_factory
@properties(elength=12)
def flashing_symbols(time):
    return multiply(gif(time / 4, "staticFrames", int(time / 4 % 3)), time)


@reg
def random_dissolve_factory():
    random_leds = [random.random() for i in range(col * row)]
    ordered_leds = sample(list(range(col * row)), row * col)
    ordered_leds = [led / (row * col) for led in ordered_leds]

    @properties(elength=14)
    def dissolve_chain(time):
        if time < 4:
            # randomize each frame
            return dissolve_random(-time / 4)
        elif time < 8:
            return dissolve(time / 4, ordered_leds, row * col)
        elif time < 10:
            return rotate90(wave(1 - easing.triangle((time / 2) % 1), 1, easing.inverse))
        return dissolve(-easing.triangle((time / 2) % 1), random_leds)
    return dissolve_chain


calm_list = effect_list.Effect_List()
calm_list.add(effect_list.timed(lambda t: dissolve_random(t / 6), 0, 6),
              effect_list.timed(lambda t: circle_inwards(t / 3), 6, 3),
              effect_list.timed(lambda t: square_inwards(t / 3), 9, 3),
              effect_list.timed(lambda t: cross(t), 12, 4),
              effect_list.timed(lambda t: diagonal_wave(t / 3), 15, 3))


@reg
@simple_factory
@properties(elength=18)
def calming(time):
    return add_clamped(calm_list.get_current(time))


sharp_list = effect_list.Effect_List()
sharp_list.add(effect_list.timed(lambda t: square_inwards_sharp(-t), 0, 4),
               effect_list.timed(lambda t: circle_inwards(easing.easeInOutCubic(easing.triangle(t / 2)), easing.easeInOutQuad), 4, 2),
               effect_list.timed(lambda t: multiply(square_inwards(t / 8), gif(t, "fourGradientsLinearSpin")), 6, 6))


@reg
@simple_factory
@properties(elength=10)
def sharp_pattern(time):
    return add_clamped(sharp_list.get_current(time))


@reg
def color_steps_factory():
    random_leds = [random.random() for i in range(col * row)]
    random_colors = [1 / 8, 3 / 8, 5 / 8, 7 / 8]
    random.shuffle(random_colors)

    @properties(elength=20)
    def color_steps(time):
        if time < 8:
            return overlay_border(fill(int(time) / 4, easing.linear))
        elif time < 10:
            return square_inwards(time)
        elif time < 12:
            return dissolve(time / 2, random_leds)
        elif time < 16:
            return fill(time / 2)

        nw_corner = fill(random_colors[0], easing.linear, row // 2, col // 2)
        ne_corner = rotate90(
            fill(random_colors[1], easing.linear, row // 2, col // 2), 1)
        se_corner = rotate90(
            fill(random_colors[2], easing.linear, row // 2, col // 2), 2)
        sw_corner = rotate90(
            fill(random_colors[3], easing.linear, row // 2, col // 2), 3)

        if time < 17:
            return nw_corner
        elif time < 18:
            return add([nw_corner, ne_corner])
        elif time < 19:
            return add([nw_corner, ne_corner, se_corner])
        return add([nw_corner, ne_corner, se_corner, sw_corner])
    return color_steps


@reg
def wipe_lines_factory():
    rot1 = random.randint(0, 4)
    rot2 = random.randint(0, 4)

    @properties(elength=8)
    def wipe_lines(time):
        if time < 4:
            static_mask = fill(0.5, easing.triangle, row, col * int(time) // 4)
            moving_stripe = mask_rect(wave(time, 1, easing.linear), 0, row,
                                      col * int(time) // 4, col * (int(time) + 1) // 4)
            return rotate90(add([static_mask, moving_stripe]), rot1)

        time = time % 4
        static_mask = rotate90(fill(0.5, easing.triangle, row,
                               col - col * (int(time) + 1) // 4), 2)
        moving_stripe = mask_rect(wave(time, 1, easing.inverse), 0, row,
                                  col * int(time) // 4, col * (int(time) + 1) // 4)
        return rotate90(add_clamped([static_mask, moving_stripe]), rot2)
    return wipe_lines


@reg
def raindrops_factory():
    round = random.random() > 0.5
    coordinates = [(random.randint(0, row), random.randint(0, col)) for i in range(8)]

    @properties(elength=8)
    def raindrops(time):
        t = time if time < 4 else -time
        if round:
            return multiply(circle_inwards(t, origin=coordinates[int(time)]), easing.easeOutCubic(-t % 1))
        else:
            return square_inwards(t, origin=coordinates[int(time)])
    return raindrops


timewarp_list = effect_list.Effect_List()
timewarp_list.add(
    effect_list.timed(lambda t: curtain(-t / 2.5, easing.spikeInCubic), 0, 2.1),
    effect_list.timed(lambda t: clock(easing.gaussianFit(t / 8) * 4), 2, 8),
    effect_list.timed(lambda t: curtain(t / 2, easing.spikeInCubic), 9.5, 2),
    effect_list.timed(lambda t: circle_inwards(easing.gaussianFit(t / 8) * 4), 12, 8),
    effect_list.timed(lambda t: diagonal_wave(easing.easeInOutCubic(t / 6) * 3), 20, 6)
)


@reg
@simple_factory
@properties(elength=26)
def timewarp(time):
    return add_clamped(timewarp_list.get_current(time))


@reg
@simple_factory
@properties(elength=8, intensity=True)
def fan_open_close(time):
    return rotate90(fill_triangle(time, int(time % 2)), int(time / 2))


@reg
@simple_factory
@properties(elength=3)
def split_triangle_merge(time):
    tri = fill_triangle(0.5, 0)
    trinverse = ease_image(tri, easing.inverse)
    if time < 1:
        return add_clamped([multiply(rotate90(wave(time / 2), 2), tri), multiply(wave(time / 2), trinverse)])
    if time <= 2:
        return wave(0.5)
    return multiply(rotate90(wave(time, ease=easing.inverse)), wave(0.5))


@reg
@simple_factory
@properties(elength=9)
def ditherfill(time):
    if time < 6:
        return gif(time / 6, 'ditherFill')
    if time <= 7:
        return flipBottomHalf(wave(-time, ease=easing.linear))
    return multiply(diagonal_wave(easing.triangle(time / 2)), gif(0.2, 'ditherFill'))


@reg
@simple_factory
@properties(elength=8)
def ball_bounce(time):
    bheight = easing.spikeOutQuad(time % 1)
    return circle_inwards(0.2 + 0.15 * bheight, ease=easing.easeOutQuad, origin=(col - col * bheight, row * easing.triangle((time / 4) % 1)))

@reg
@simple_factory
@properties(elength=4)
def spiral_mov(time):
    def bandpass(t):
        return easing.spikeInCubic(clamp(4*t-time))
    return ease_image(gif(0, 'squareSpiral'), bandpass)


# FOR TESTING/DEBUG
# Overwrite set of chains to choose from
# reg.all = [color_steps_factory]
