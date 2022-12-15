import re
from itertools import pairwise

from scipy.spatial import distance

test = False

if test:
    y_line = 10
    file_name = 'input_test.txt'
    max_p = 20
else:
    y_line = 2000000
    file_name = 'input.txt'
    max_p = 4000000

with open(file_name) as f:
    sensors = [[(c[0], c[1]), (c[2], c[3])] for line in f.readlines() for c in
               [[int(x) for x in re.findall(r'-?\d+', line.strip())]]]

for v in sensors:
    v.append(distance.cityblock(v[0], v[1]))


def overlap_1d(r1, r2):
    return max(0, min(r1[1], r2[1]) - max(r2[0], r1[0]))


max_distance = max(x for _, _, x in sensors)
all_x = [x for (x, _), _, _ in sensors]
x_range = (min(all_x) - max_distance - 1, max(all_x) + max_distance + 1)

all_positions = [x for s in sensors for x in s if type(x) == tuple]
count_postions_on_y = len({((x, y_p) for x, y_p in all_positions if y_p == y_line)})


# part 1
def get_occupied_y_range(y_value):
    occupied_y_ranges = []
    for (x_y, y_s), _, d in sensors:
        delta_y = abs(y_value - y_s)
        if delta_y <= d:
            occupied_y_ranges.append((x_y - (d - delta_y), x_y + (d - delta_y) + 1))
    return occupied_y_ranges


all_occupied = {y for r in get_occupied_y_range(y_line) for y in range(*r)}

print(len(all_occupied) - count_postions_on_y)

# part 2

for y_current in range(max_p + 1):
    x_values = {x for r in get_occupied_y_range(y_current) for x in range(*r) if 0 <= x <= max_p}
    if y_current % 10 == 0:
        print(y_current)
    if len(x_values) != max_p+1:
        y_result = y_current
        result = x_values
        break

for x1, x2 in pairwise(sorted(x_values)):
    if x2-x1 != 1:
        x_result = x1+1

print(x_result*4000000 + y_result)