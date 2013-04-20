from functools import update_wrapper
import gevent


def pass_parameter(param):
    gevent.sleep()
    return param


class CountCalls(object):
    def __init__(self, wrapped):
        update_wrapper(self, wrapped)
        self.wrapped = wrapped
        self.calls = 0
    
    def __call__(self, *a, **k):
        self.calls += 1
        return self.wrapped(*a, **k)
