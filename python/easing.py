
def inverse(t):
    """falling linear function"""
    return 1 - t


def linear(t):
    """no easing, no acceleration"""
    return t


def linearCutoff(t):
    """ starts off linear, but is 0 if time >= 1"""
    if t >= 1:
        return 0
    return t


def square(t):
    """always 0 exept for t>=0 and t<=1"""
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
    """a mirrored quadratic ease"""
    return easeInQuad(triangle(t))


def spikeOutQuad(t):
    """a mirrored OutQuad ease"""
    return easeOutQuad(triangle(t))


def spikeInOutQuad(t):
    """a mirrored InOutQuad ease"""
    return easeInOutQuad(triangle(t))


def spikeInCubic(t):
    """a mirrored InCubic ease"""
    return easeInCubic(triangle(t))


def spikeInOutCubic(t):
    """a mirrored InOutCubic ease"""
    return easeInOutCubic(triangle(t))


def spikeSquare(t):
    """1 in the first fourth of the segment, 0 else"""
    if t > 0 and t < 1 / 4:
        return 1
    return 0
