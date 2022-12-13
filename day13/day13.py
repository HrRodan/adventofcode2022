from ast import literal_eval
from functools import cmp_to_key
from itertools import zip_longest
from typing import Union, Optional

with open('input.txt') as f:
    pairs = [[literal_eval(y) for y in x.split('\n')] for x in f.read().strip().split('\n\n')]

VALUE_TYPE = Optional[Union[int, list]]


def compare(left_value: VALUE_TYPE, right_value: VALUE_TYPE):
    compare_result = 0
    sentry = object()
    for left, right in zip_longest(left_value, right_value, fillvalue=sentry):
        type_left = type(left)
        type_right = type(right)
        if right == sentry:
            return -1
        elif left == sentry:
            return 1
        elif type_right == type_left == int:
            if left < right:
                return 1
            elif right < left:
                return -1
        elif type_left == type_right == list:
            if right and not left:
                return 1
            elif left and not right:
                return -1
            else:
                compare_result = compare(left, right)
        elif type_right != type_left:
            if type_right == int:
                compare_result = compare(left, [right])
            elif type_left == int:
                compare_result = compare([left], right)
        if compare_result != 0:
            break
    return compare_result


results = [(i, compare(*r)) for i, r in enumerate(pairs, start=1)]
r1 = sum(i for i, c in results if c == 1)
print(r1)

# part 2
pairs_part2 = [p for pair in pairs for p in pair]
addon1 = [[2]]
addon2 = [[6]]
pairs_part2.extend([addon1, addon2])
results_part2 = sorted(pairs_part2, key=cmp_to_key(compare), reverse=True)
r2 = [i for i, c in enumerate(results_part2, start=1) if c in [addon1, addon2]]
print(r2[0] * r2[1])
