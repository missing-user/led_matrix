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


for value in range(0, 20):
    print(EasingFunctions.spikeInOutCubic(value / 20))
