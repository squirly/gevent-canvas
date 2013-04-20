import gevent
from gevent_canvas.core import make_greenlet


def pass_parameter(param):
    gevent.sleep()
    return param


class TestMakeGreenlet:
    func = lambda *a: a
    
    def is_greenlet(self, test):
        return isinstance(test, gevent.Greenlet)
    
    def test_from_greenlet(self):
        greenlet = gevent.Greenlet()
        assert greenlet is make_greenlet(greenlet)

    def test_from_function(self):
        greenlet = make_greenlet(self.func)
        assert self.is_greenlet(greenlet)
        assert greenlet._run == self.func

    def test_from_tuple(self):
        greenlet = make_greenlet((self.func, 'test', 'test2'))
        assert self.is_greenlet(greenlet)
        assert greenlet._run == self.func


def test_greenlet_starter():
    pass


def test_map_into():
    pass
