from collections import defaultdict
from itertools import count
from typing import List
import numpy as np

with open('input.txt') as f:
    snafu_numbers_raw = [x.strip() for x in f.readlines()]

snafu_dict = {
    '2': 2,
    '1': 1,
    '0': 0,
    '-': -1,
    '=': -2
}

snafu_dict_reversed = {v: k for k, v in snafu_dict.items()}


def base5():
    for i in count():
        yield 5 ** i


def snafu_to_dec(snafu_number: str) -> int:
    snafu_int_reversed = (snafu_dict[x] for x in snafu_number[::-1])
    return sum(x * y for x, y in zip(snafu_int_reversed, base5()))


def dec_to_snafu(dec_number: int) -> str:
    base_5_reversed = [int(x) for x in np.base_repr(dec_number, 5)[::-1]]
    for i in range(len(base_5_reversed)):
        x = base_5_reversed[i]
        if x <= 2:
            base_5_reversed[i] = x
        else:
            base_5_reversed[i] = x - 5
            try:
                base_5_reversed[i + 1] += 1
            except IndexError:
                base_5_reversed.append(1)
    return ''.join([snafu_dict_reversed[x] for x in base_5_reversed[::-1]])


r1 = dec_to_snafu(sum(snafu_to_dec(x) for x in snafu_numbers_raw))
print(r1)
