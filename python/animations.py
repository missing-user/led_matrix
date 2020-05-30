import itertools
import math

row = 16
col = 16


class EasingFunctions:
    @staticmethod
    def inverse(t):
        1 - t

    # no easing, no acceleration
    @staticmethod
    def linear(t):
        return t

    # accelerating from zero velocity
    @staticmethod
    def easeInQuad(t):
        return t * t

    # decelerating to zero velocity
    @staticmethod
    def easeOutQuad(t):
        return t * (2 - t)

    # acceleration until halfway, then deceleration
    @staticmethod
    def easeInOutQuad(t):
        if t < 0.5:
            return 2 * t * t
        else:
            return -1 + (4 - 2 * t) * t

    # accelerating from zero velocity

    @staticmethod
    def easeInCubic(t):
        return t * t * t

    # decelerating to zero velocity

    @staticmethod
    def easeOutCubic(t):
        return --t * t * t + 1

    # acceleration until halfway, then deceleration

    @staticmethod
    def easeInOutCubic(t):
        if t < 0.5:
            return 4 * t * t * t
        else:
            return (t - 1) * (2 * t - 2) * (2 * t - 2) + 1

    # a polynomial approximating a gaussian distribution
    @staticmethod
    def gaussianFit(t):
        return 0.257 * t + 14.717 * t * t - 29.947 * t * t * t + 14.973 * t * t * t * t

    # linear up, linear down, can be used to create symetric versions of the other functions

    @staticmethod
    def triangle(t):
        if t < 0.5:
            return t * 2
        else:
            return 2 - t * 2

    @staticmethod
    def spikeInQuad(t):
        return EasingFunctions.easeInQuad(EasingFunctions.triangle(t))

    @staticmethod
    def spikeOutQuad(t):
        return EasingFunctions.easeOutQuad(EasingFunctions.triangle(t))

    @staticmethod
    def spikeInOutQuad(t):
        return EasingFunctions.easeInOutQuad(EasingFunctions.triangle(t))

    @staticmethod
    def spikeInCubic(t):
        return EasingFunctions.easeInCubic(EasingFunctions.triangle(t))

    @staticmethod
    def spikeInOutCubic(t):
        return EasingFunctions.easeInOutCubic(EasingFunctions.triangle(t))


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


class Effects:
    @staticmethod
    def arrow(timePercent, iterations=1, ease=EasingFunctions.gaussianFit):
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

    @staticmethod
    def diagonalWave(timePercent, iterations=1, ease=EasingFunctions.gaussianFit):
        leds = [0] * col * row
        for i in range(len(leds)):
            eval = timePercent * (iterations + 2) - 2 + \
                XY(i)[0] / row + XY(i)[1] / col
            if(eval > iterations):
                leds[i] = ease(clamp(eval))
            else:
                leds[i] = ease(clamp(eval % 1))
        return leds

    @staticmethod
    def wave(timePercent, iterations=1, ease=EasingFunctions.gaussianFit):
        leds = [0] * col * row
        for i in range(len(leds)):
            eval = timePercent * (iterations + 1) - 1 + XY(i)[0] / row
            if(eval > iterations):
                leds[i] = ease(clamp(eval))
            else:
                leds[i] = ease(clamp(eval % 1))
        return leds

    @staticmethod
    def squareInwardsSharp(timePercent, ease=EasingFunctions.linear):
        leds = [0] * col * row
        eval = (timePercent * row) / 2
        for i in range(len(leds)):
            distFromCenter = max(abs((col - 1) / 2 - XY(i)[1]),
                                 abs((row - 1) / 2 - XY(i)[0]))
            leds[i] = ease(clamp(eval - distFromCenter + 0.5))
        return leds

    @staticmethod
    def squareInwards(timePercent, ease=EasingFunctions.spikeInCubic):
        leds = [0] * col * row
        for i in range(len(leds)):
            distFromCenter = max(abs((col - 1) / 2 - XY(i)[1]),
                                 abs((row - 1) / 2 - XY(i)[0]))
            leds[i] = ease(clamp(timePercent * 1.2 - distFromCenter / row))
        return leds

    @staticmethod
    def curtain(timePercent, ease=EasingFunctions.spikeInCubic):
        leds = [0] * col * row
        for i in range(len(leds)):
            distFromCenter = abs((row - 1) / 2 - XY(i)[0])
            leds[i] = ease(clamp(timePercent * 1.2 - distFromCenter / row))
        return leds

    @staticmethod
    def circleInwards(timePercent, ease=EasingFunctions.spikeInCubic):
        leds = [0] * col * row
        eval = timePercent * 1.4143  # hardcoded root(2)
        for i in range(len(leds)):
            dy = (col - 1) / 2 - XY(i)[1]
            dx = (col - 1) / 2 - XY(i)[0]
            distFromCenter = math.sqrt(dy * dy + dx * dx)

            leds[i] = ease(clamp(eval - distFromCenter / row))
        return leds

    @staticmethod
    def circleInwardsSharp(timePercent, ease=EasingFunctions.linear):
        leds = [0] * col * row
        eval = (timePercent * row * 1.4143) / 2  # hardcoded root(2)
        for i in range(len(leds)):
            dy = (col - 1) / 2 - XY(i)[1]
            dx = (col - 1) / 2 - XY(i)[0]
            distFromCenter = math.sqrt(dy * dy + dx * dx)
            leds[i] = ease(clamp(eval - distFromCenter + 0.5))
        return leds

    @staticmethod
    def strobe(timePercent, ease=EasingFunctions.triangle):
        leds = [0] * col * row
        for led in leds:
            led = clamp(ease(timePercent * 2))
        return leds
