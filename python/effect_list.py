import functools

from animationChains import length


class Effect_List:
    def __init__(self, list=[]):
        self.list = list

    def add(self, *elems):
        self.list.extend(elems)

    def get_active(self, time):
        return [e for e in self.list if e.start_time <= time < e.start_time + e.length]
        # return list(filter(lambda elem: elem.start_time <= time <= elem.start_time + elem.length, self.list))

    def __repr__(self):
        if not self.list:
            return "Effect_List is empty"
        latest_effect = 600  # e.start_time + e.length
        t = 0
        elements = []
        while self.get_active(t):
            elements.append("\t ".join(f.__name__ for f in self.get_active(t)))
            t += 1
        return "\nEffect_List:\n" + "\n".join(elements)

        #elements = [(f.__name__, f.start_time) for f in self.list]
        # return f"Effect_List = {elements}"

    def __getitem__(self, time):
        return self.get_active(time)

    def __call__(self, time):
        return [func(time - func.start_time) for func in self.get_active(time)]


def timed(func, start_time, override_length=None):
    @functools.wraps(func)
    def wrapper(time):
        return func(time)
    wrapper.start_time = start_time

    # prefer override_length, take animation chain length if that exists, else 1
    wrapper.length = override_length or func.length if hasattr(
        func, "length") else 1

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

    print(effects)
    print(effects.list)

    for t in range(12):
        print(f"t={t}", effects[t])

    for t in range(12):
        print(f"t={t}", effects(t))
