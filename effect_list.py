class Effect_List:
    def __init__(self, list=None):
        # works with given list as reference, doen't just copy the content
        self.list = [] if list is None else list

    def add(self, *elems):
        self.list.extend(elems)
        #print('element added, new list is ',self.list)

    def clear(self):
        self.list.clear()

    def get_active(self, time):

        return [e for e in self.list if e.start_time <= time < e.start_time + e.elength]
        # return list(filter(lambda elem: elem.start_time <= time <= elem.start_time + elem.length, self.list))

    def repr(self):
        # elements = [f.__name__ for f in self.list]
        return f"Effect_List = {self.list}"

    def __getitem__(self, time):
        return self.get_active(time)

    def get_current(self, time):
        return [func(time - func.start_time) for func in self.get_active(time)]


def timed(func, start_time, override_length=None):
    def wrapper(time):
        return func(time)
    wrapper.start_time = start_time

    # prefer override_length, take animation chain length if that exists, else 1
    wrapper.elength = func.elength.elength if func.elength else 1
    if override_length:
        wrapper.elength= override_length

    return wrapper
