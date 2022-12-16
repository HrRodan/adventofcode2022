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

# part 1

all_positions = [x for s in sensors for x in s if type(x) == tuple]
count_postions_on_y = len({((x, y_p) for x, y_p in all_positions if y_p == y_line)})


def get_occupied_y_range(y_value):
    occupied_y_ranges = []
    for (x_y, y_s), _, d in sensors:
        delta_y = abs(y_value - y_s)
        if delta_y <= d:
            occupied_y_ranges.append((x_y - (d - delta_y), x_y + (d - delta_y) + 1))
    return occupied_y_ranges


all_occupied = {y for r in get_occupied_y_range(y_line) for y in range(*r)}

print(len(all_occupied) - count_postions_on_y)

#part 2

def find_gap(occupied_y):
    x_max = None
    for (x1, x2) in sorted(occupied_y):
        x1 = max(x1, 0)
        x2 = min(x2, max_p + 1)
        if not x_max:
            x_max = x1
        if x1 > x_max:
            return True
        x_max = max(x_max, x2)
    return False


for y_current in range(max_p + 1):
    if y_current % 100000 == 0:
        print(y_current)
    if gap := find_gap(get_occupied_y_range(y_current)):
        y_result = y_current
        break

all_occupied_part2 = {y for r in get_occupied_y_range(y_result) for y in range(*r)}

for x1, x2 in pairwise(sorted(all_occupied_part2)):
    if x2 - x1 != 1:
        x_result = x1 + 1

print(x_result * 4000000 + y_result)
