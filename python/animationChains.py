
import easing
from animations import *


def length(l):  # decorator factory
    """decorator that returns the length of an animation chain in beats"""
    def decorator(func):  # decorator
        func.length = l
        return func

    return decorator


@length(12)
def chain1(time):
    if time < 4:
        return gif(time / 4, "dithered45degSquare")
    elif time < 6:
        return splitLines(time / 2)
    elif time < 9:
        return gif(time / 3, "buildArrows")
    elif time < 10:
        effectResult = doubleArrow(
            time / 2 + 1, 1, lambda t: 0 if t * 6 % 1 == t * 6 % 2 else 1)
        return rotateMatrix90(effectResult, 1)
    elif time < 11:
        return diagonalWave(1 - time, 1, easing.square)
    return diagonalWave(time, 1, easing.square)


@length(2)
def chain2(time):
    return splitLines(easing.triangle(time / 2))


@length(16)
def chain3(time):
    if time < 3:
        return diagonalWave(time)
    elif time < 4:
        return diagonalWave(time, 1, easing.easeOutQuad)
    elif time < 5:
        return squareInwards(time, lambda t: 1 - easing.easeInQuad(t))
    elif time < 8:
        return squareInwards(time)
    elif time < 10:
        return squareInwards(easing.triangle(time / 2 % 1), easing.easeOutQuad)
    return mirrorX(mirrorY(diagonalWave(-time)))


@length(16)
def chain4(time):
    if time < 4:
        return cross(time, easing.square)
    elif time < 12:
        filledCorners = mirrorX(
            mirrorY(fill(clamp((time % 1) * 2), width=6, height=6)))
        return add(cross(time), filledCorners)
    elif time < 13:
        return rotateMatrix90(flipBottomHalf(wave(time)), 1)
    elif time < 14:
        return flipBottomHalf(wave(time))
    return strobe(time * 3)


@length(9)
def chain5(time):
    if time < 1:
        return gif(time, "compressingLines")
    elif time < 7:
        return gif((time - 1) / 6, "rotatingLines")
    elif time < 9:
        return gif(time / 2 + 0.5, "stonehengeToBorder")

    return gif(0.4, "compressingLines")
