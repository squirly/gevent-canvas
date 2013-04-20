from canvas import _chain, _group
from core import map_into

chain = map_into(_chain)
group = map_into(_group)


def chord(header):
    return lambda callback: chain(
        _group(header),
        callback
    )
