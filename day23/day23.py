from itertools import cycle
from typing import Tuple

import numpy as np
from scipy.ndimage import generic_filter

from utilities import sliding_window

with open('input.txt') as f:
    grove = np.array([[1 if x == '#' else 0 for x in line.strip()] for line in f.readlines()], dtype=np.byte)

# 012
# 345
# 678
# 0 - north, 1 - south, 2 - west, 3 -east
direction_cycle_repeat = sliding_window(cycle([0, 1, 2, 3]), 4)


def numpy_tuple_wrapper(function):
    def inner(array_part, *args, **kwargs):
        array_part_tuple = tuple(int(x) for x in array_part)
        return function(array_part_tuple, *args, **kwargs)

    return inner


# @numpy_tuple_wrapper
# @lru_cache
def check_surrounding(array_part: Tuple[int], current_cycle: Tuple[int]):
    # no elves
    if int(array_part[4]) == 0:
        return 0
    direction_array = [
        array_part[0] + array_part[1] + array_part[2],
        array_part[6] + array_part[7] + array_part[8],
        array_part[0] + array_part[3] + array_part[6],
        array_part[2] + array_part[5] + array_part[8]
    ]
    # no movement
    if all(x == 0 for x in direction_array):
        return 1
    return next((i + 10 for i in current_cycle if direction_array[i] == 0), 1)


# -0-
# 123
# -4-
# @numpy_tuple_wrapper
# @lru_cache
def check_collisions(array_part: Tuple[int]):
    this_value = array_part[2]
    if this_value != 0:
        return this_value
    count = (array_part[0] == 11) * 1 + (array_part[1] == 13) * 1 + (array_part[3] == 12) * 1 + (
            array_part[4] == 10) * 1
    return 99 if count > 1 else 0


# @numpy_tuple_wrapper
# @lru_cache
def allow_movement(array_part: Tuple[int]):
    this_value = array_part[2]
    if this_value in [0, 99]:
        return 0
    else:
        return 1 if (this_value == 10 and array_part[0] == 99) or (this_value == 11 and array_part[4] == 99) \
                    or (this_value == 12 and array_part[1] == 99) or (this_value == 13 and array_part[3] == 99) \
            else this_value


for i in range(1, 1000):
    # grove = np.pad(grove, pad_width=1, mode='constant', constant_values=0)
    next_cycle = tuple(next(direction_cycle_repeat))
    grove_test = generic_filter(grove, size=(3, 3), function=check_surrounding, mode='constant', cval=0,
                                extra_arguments=(next_cycle,)).astype(np.byte)
    if np.array_equal(grove, grove_test):
        r2 = i
        break
    grove = generic_filter(grove_test, footprint=((0, 1, 0), (1, 1, 1), (0, 1, 0)), function=check_collisions,
                           mode='constant', cval=0).astype(np.byte)
    grove = generic_filter(grove, footprint=((0, 1, 0), (1, 1, 1), (0, 1, 0)),
                           function=allow_movement, mode='constant', cval=0).astype(np.byte)
    grove = np.pad(grove, pad_width=1, mode='constant', constant_values=0)
    north = np.roll((grove == 10), axis=0, shift=-1)
    south = np.roll((grove == 11), axis=0, shift=1)
    east = np.roll((grove == 13), axis=1, shift=1)
    west = np.roll((grove == 12), axis=1, shift=-1)
    grove = (north + south + east + west + grove == 1).astype(np.byte)
    if i % 10 == 0:
        # trim array
        nz = np.nonzero(grove)  # Indices of all nonzero elements
        grove = grove[nz[0].min():nz[0].max() + 1, nz[1].min():nz[1].max() + 1]
    if i == 10:
        grove_part1 = grove.copy()

# trim array
nz = np.nonzero(grove_part1)  # Indices of all nonzero elements
arr_trimmed = grove_part1[nz[0].min():nz[0].max() + 1, nz[1].min():nz[1].max() + 1]
r1 = np.count_nonzero(arr_trimmed == 0)
print(r1)

# part2
print(r2)
