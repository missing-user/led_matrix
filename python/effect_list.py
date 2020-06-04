import functools
from animationChains import length


class Effect_List:
    def __init__(self, list=[]):
        self.list = list

    def add(self, *elems):
        for e in elems:
            self.list.append(e)

    def get_active(self, time):
        return [e for e in self.list if e.start_time <= time <= e.start_time + e.length]
        # return list(filter(lambda elem: elem.start_time <= time <= elem.start_time + elem.length, self.list))

    def __call__(self, time):
        return [func(time - func.start_time) for func in self.get_active(time)]


def timed(func, start_time):
    @functools.wraps(func)
    def wrapper(time):
        return func(time)
    wrapper.start_time = start_time
    wrapper.length = func.length
    return wrapper


if __name__ == "__main__":
    @length(5)
    def x(time):
        print('x', time)
        return 'x'

    @length(7)
    def y(time):
        print('y', time)
        return 'y'

    effects = Effect_List()
    effects.add(timed(x, 1), timed(y, 2))

    print(effects.list)

    for t in range(12):
        print(f"t={t}", effects.get_active(t))

    for t in range(12):
        print(f"t={t}", effects(t))
