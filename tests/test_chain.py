from gevent_canvas import chain
from helpers import CountCalls, pass_parameter
from gevent import Greenlet


def test_simple_chain():
    value = object()
    test_function = CountCalls(pass_parameter)
    greenlet = chain(
        Greenlet(test_function, value),
        test_function,
    )
    greenlet.start()
    assert value == greenlet.get()
    assert 2 == test_function.calls


def test_long_chain():
    value = object()
    test_function = CountCalls(pass_parameter)
    greenlet = chain(
        (test_function, value),
        test_function,
        test_function,
        test_function,
        test_function,
        test_function,
    )
    greenlet.start()
    assert value == greenlet.get()
    assert 6 == test_function.calls


def test_chain_one():
    value = object()
    test_function = CountCalls(pass_parameter)
    greenlet = chain(
        (test_function, value),
    )
    greenlet.start()
    assert value == greenlet.get()
    assert 1 == test_function.calls


def test_chain_with_immutable():
    value, value2 = object(), object()
    test_function = CountCalls(pass_parameter)
    immutable_greenlet = Greenlet(test_function, value2)
    immutable_greenlet.immutable = True
    greenlet = chain(
        (test_function, value),
        test_function,
        immutable_greenlet,
        test_function,
    )
    greenlet.start()
    assert value2 == greenlet.get()
    assert 4 == test_function.calls


def test_chain_add_args():
    return_second = lambda x, y: y
    value, value2 = object(), object()
    greenlet = chain(
        (pass_parameter, value),
        (return_second, value2),
    )
    greenlet.start()
    assert value2 == greenlet.get()


def test_nested_chain():
    value = object()
    test_function = CountCalls(pass_parameter)
    greenlet = chain(
        (test_function, value),
        chain(
            test_function,
            test_function,
            test_function,
            test_function),
        test_function,
    )
    greenlet.start()
    assert value is greenlet.get()
    assert 6 == test_function.calls


def test_pass_into_chain():
    value = object()
    test_function = CountCalls(pass_parameter)
    greenlet = chain(
        test_function,
        test_function,
    )
    greenlet.start(value)
    assert value == greenlet.get()
    assert 2 == test_function.calls


def test_pass_into_chain_later():
    value = object()
    test_function = CountCalls(pass_parameter)
    greenlet = chain(
        test_function,
        test_function,
    )
    greenlet.start_later(0, value)
    assert value == greenlet.get()
    assert 2 == test_function.calls
