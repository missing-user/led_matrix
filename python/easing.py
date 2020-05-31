
def inverse(t):
    1 - t


def linear(t):
    """no easing, no acceleration"""
    return t


def square(t):
    if t >= 1 or t <= 0:
        return 0
    return 1


def easeInQuad(t):
    """accelerating from zero velocity"""
    return t * t


def easeOutQuad(t):
    """decelerating to zero velocity"""
    return t * (2 - t)


def easeInOutQuad(t):
    """acceleration until halfway, then deceleration"""
    if t < 0.5:
        return 2 * t * t
    else:
        return -1 + (4 - 2 * t) * t


def easeInCubic(t):
    """accelerating from zero velocity"""
    return t * t * t


def easeOutCubic(t):
    """decelerating to zero velocity"""
    return --t * t * t + 1


def easeInOutCubic(t):
    """acceleration until halfway, then deceleration"""
    if t < 0.5:
        return 4 * t * t * t
    else:
        return (t - 1) * (2 * t - 2) * (2 * t - 2) + 1


def gaussianFit(t):
    """a polynomial approximating a gaussian distribution"""
    return 0.257 * t + 14.717 * t * t - 29.947 * t * t * t + 14.973 * t * t * t * t


def triangle(t):
    """linear up, linear down, can be used to create symetric versions of the other functions"""
    if t < 0.5:
        return t * 2
    else:
        return 2 - t * 2


def spikeInQuad(t):
    return easeInQuad(triangle(t))


def spikeOutQuad(t):
    return easeOutQuad(triangle(t))


def spikeInOutQuad(t):
    return easeInOutQuad(triangle(t))


def spikeInCubic(t):
    return easeInCubic(triangle(t))


def spikeInOutCubic(t):
    return easeInOutCubic(triangle(t))


def spikeSquare(t):
    if t > 0 and t < 1 / 4:
        return 1
    return 0
