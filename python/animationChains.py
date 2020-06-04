
import easing
from animations import *


def makeRegistrar():
    """adds all funcs with this decorator to a list"""
    registry = []

    def registrar(func):
        registry.append(func)
        return func  # normally a decorator returns a wrapped function,
        # but here we return func unmodified, after registering it
    registrar.all = registry
    return registrar


reg = makeRegistrar()


def length(l):  # decorator factory
    """decorator that returns the length of an animation chain in beats"""
    def decorator(func):  # decorator
        func.length = l
        return func

    return decorator


@reg
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


@reg
@length(2)
def chain2(time):
    return splitLines(easing.triangle(time / 2))


@reg
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


@reg
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


@reg
@length(6)
def chain5(time):
    if time < 1:
        return gif(time, "compressingLines")
    elif time < 4:
        return gif((time - 0.5) / 3, "rotatingLines")
    elif time < 5:
        return gif(time, "stonehengeToBorder")
    return gif(0.4, "compressingLines")


@reg
@length(8)
def chain6(time):
    if time < 4:
        return gif(time, "symTriangle")
    elif (time % 2) <= 1:
        return rotateMatrix90(flipEverySecondRow(wave(time, 1, easing.spikeInCubic)), 1)
    else:
        return flipEverySecondRow(wave(time, 1, easing.spikeInCubic))


@reg
@length(8)
def chain7(time):
    if time < 1:
        return rotateMatrix90(arrow(-time))
    elif time < 4:
        return rotateMatrix90(arrow(time / 3 - 0.333, 6))
    elif time < 6:
        return curtain(-time)
    return rotateMatrix90(wave(time / 2))


@reg
@length(6)
def chain8(time):
    diamond = mirrorX(mirrorY(diagonalWave(time)))
    if time < 1:
        return gif(time, "buildTiles")
    elif time < 2:
        return rotateMatrix90(curtain(time, easing.spikeSquare), 1)
    elif time < 3:
        return maskCorner(diamond)
    elif time < 4:
        return maskCorner(diamond, 1)
    elif time < 5:
        return maskCorner(diamond, 2)
    elif time < 6:
        return maskCorner(diamond, 3)


@reg
@length(6)
def chain9(time):
    if time % 2 <= 1:
        return gif(time, "dot")
    return squareInwards(time)


@reg
@length(30)
def chain10(time):
    if time < 8:
        return circleInwards(time)
    elif time < 12:
        return rotateMatrix90(curtain(easing.triangle(time / 2)), 1)
    elif time < 16:
        return curtain(easing.triangle(time / 2))
    elif time < 18:
        return strobe(time * 3)
    elif time < 24:
        return gif(time, "compress")
    elif time < 28:
        return zipper(easing.triangle(time / 2 % 1))
    return circleInwards(-time)
