
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
    return -t * t * t + 1


def easeInOutCubic(t):
    """acceleration until halfway, then deceleration"""
    if t < 0.5:
        return 4 * t * t * t
    else:
        return (t - 1) * (2 * t - 2) * (2 * t - 2) + 1


def gaussianFit(t):
    """a nice polynomial bump"""
    return 16 * t**2 - 32 * t**3 + 16 * t**4


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


if __name__ == "__main__":
    eases = [gaussianFit, easeInOutCubic, easeInOutCubic, inverse, linear,
             linearCutoff, square, easeInQuad, easeOutQuad, easeInOutQuad, spikeSquare]
    sym_functions = [spikeInOutCubic, spikeInCubic, spikeInOutQuad, spikeOutQuad, spikeInQuad, triangle]

    num_iterations = 151  # prime number, non hom distrib

    success = True

    print('testing easing functions')
    for ease in eases:
        print('testing', ease.__name__)
        for i in range(num_iterations):
            res = ease(i / num_iterations)
            if res < 0 or res > 1:
                print(ease.__name__, 'failed at', i / num_iterations, 'with result', res)
                success = False

    print('testing symetric easing functions')
    for ease in sym_functions:
        print('testing', ease.__name__)
        for i in range(num_iterations):
            res1 = ease(i / num_iterations)
            res2 = ease(1 - (i / num_iterations))
            if res1 < 0 or res1 > 1:
                print(ease.__name__, 'failed at', i / num_iterations, 'with result', res1)
                success = False
            if not abs(res1 - res2) < 1e-8:
                print(ease.__name__, 'not symetrical at', i / num_iterations, 'error', abs(res1 - res2))
                success = False

    print()
    print('all easing functions PASSED' if success else 'some tests have FAILED!')
