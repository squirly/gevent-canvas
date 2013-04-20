import gevent
from functools import wraps


def map_into(klass):
    @wraps(klass)
    def create_generator(*greenlets, **kwargs):
        return klass(map(make_greenlet, greenlets), **kwargs)
    return create_generator


def greenlet_starter(greenlet):
    def start_greenlet(previous):
        if not getattr(greenlet, 'immutable', False):
            greenlet.args = (previous.value,) + greenlet.args
        greenlet.start()
    return start_greenlet


def make_greenlet(g_or_func):
    if isinstance(g_or_func, gevent.Greenlet):
        return g_or_func
    elif callable(g_or_func):
        args = (g_or_func,)
    else:
        args = g_or_func
    return gevent.Greenlet(*args)
