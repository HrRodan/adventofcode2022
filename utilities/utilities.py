import collections
import functools
from itertools import islice
from typing import Tuple

POINT_TYP = Tuple[int, int]


def sign(x):
    return -1 if x < 0 else (1 if x > 0 else 0)


@functools.lru_cache(1000)
def tuple_add(t1: POINT_TYP, t2: POINT_TYP):
    return (t1[0] + t2[0], t1[1] + t2[1])


@functools.lru_cache(1000)
def tuple_add_nd(t1: Tuple[int, ...], t2: Tuple[int, ...]):
    return tuple(sum(x) for x in zip(t1, t2))


def sliding_window(iterable, n):
    # sliding_window('ABCDEFG', 4) --> ABCD BCDE CDEF DEFG
    it = iter(iterable)
    window = collections.deque(islice(it, n), maxlen=n)
    if len(window) == n:
        yield tuple(window)
    for x in it:
        window.append(x)
        yield tuple(window)
