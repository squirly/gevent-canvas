from gevent_canvas import group
from helpers import CountCalls, pass_parameter
from gevent import Greenlet


class generate_greenlets(object):
    def __init__(self, count, function=pass_parameter):
        self.values = range(count)
        self.function = CountCalls(function)
        make_greenlets = lambda value: Greenlet(self.function, value)
        self.greenlets = map(make_greenlets, self.values)
    
    calls = property(lambda self: self.function.calls) 


def test_simple_group():
    values = range(2)
    test_function = CountCalls(pass_parameter)
    greenlet = group(
        Greenlet(test_function, values[0]),
        (test_function, values[1]),
    )
    greenlet.start()
    assert values == greenlet.get()
    assert 2 == test_function.calls


def test_big_group():
    count = 6
    generator = generate_greenlets(count)
    greenlet = group(*generator.greenlets)
    greenlet.start()
    assert generator.values == greenlet.get()
    assert 6 == generator.calls


def test_group_one():
    value = object()
    test_function = CountCalls(pass_parameter)
    greenlet = group(
        (test_function, value),
    )
    greenlet.start()
    assert [value] == greenlet.get()
    assert 1 == test_function.calls


def test_with_immutable():
    count = 3
    generator = generate_greenlets(count)
    
    extra_value = object()
    extra_function = CountCalls(pass_parameter)
    immutable_greenlet = Greenlet(extra_function, extra_value)
    immutable_greenlet.immutable = True
    greenlet = group(
        generator.greenlets[0],
        generator.greenlets[1],
        immutable_greenlet,
        generator.greenlets[2],
    )
    greenlet.start()
    assert generator.values[0:2] + [extra_value] + generator.values[2:3] == greenlet.get()
    assert count == generator.calls
    assert 1 == extra_function.calls

def test_nested_group():
    count = 6
    values = range(count)
    test_function = CountCalls(pass_parameter)
    make_greenlets = lambda value: Greenlet(test_function, value)
    greenlets = map(make_greenlets, values)
    greenlet = group(
        greenlets[0],
        group(*greenlets[1:5]),
        greenlets[5],
    )
    greenlet.start()
    assert [values[0], values[1:5], values[5]] == greenlet.get()
    assert 6 == test_function.calls
