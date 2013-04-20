import gevent
from core import greenlet_starter

class ArgsAddedGreenlet(gevent.Greenlet):
    def add_args(self, args):
        self.args = args + self.args

    def start(self, *args):
        self.add_args(args)
        return gevent.Greenlet.start(self)

    def start_later(self, seconds, *args):
        self.add_args(args)
        return gevent.Greenlet.start_later(self, seconds)


class _chain(ArgsAddedGreenlet):
    def __init__(self, greenlets, *args, **k):
        self.greenlets = greenlets
        gevent.Greenlet.__init__(self, *args, **k)

    def _run(self, *args, **kwargs):
        previous = self.greenlets[0]
        for greenlet in self.greenlets[1:]:
            previous.link_value(greenlet_starter(greenlet))
            previous = greenlet
        first = self.greenlets[0]
        first.args = args + first.args
        first.kwargs.update(kwargs)
        first.start()
        gevent.joinall(self.greenlets, raise_error=True)
        last = self.greenlets[-1]
        return last.value


class _group(ArgsAddedGreenlet):
    def __init__(self, greenlets, *args):
        self.greenlets = greenlets
        gevent.Greenlet.__init__(self, *args)

    def _run(self, *args):
        def start_greenlet(greenlet):
            greenlet.args = args + greenlet.args
            greenlet.start()
        map(start_greenlet, self.greenlets)
        gevent.joinall(self.greenlets, raise_error=True)
        return map(lambda g: g.value, self.greenlets)
