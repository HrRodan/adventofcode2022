from itertools import pairwise

import numpy as np

from utilities import sign, tuple_add

with open('input.txt') as f:
    rocks = [[tuple(int(x) for x in points.split(',')) for points in line.strip().split(' -> ')] for line in
             f.readlines()]

start = (500, 0)
all_rocks = set()
for r in rocks:
    for (x1, y1), (x2, y2) in pairwise(r):
        all_rocks.update([(x2, y2)])
        if x1 == x2:
            all_rocks.update((x1, y) for y in range(y1, y2, sign(y2 - y1)))
        elif y1 == y2:
            all_rocks.update((x, y1) for x in range(x1, x2, sign(x2 - x1)))

shape = (max(x for x, _ in all_rocks) + 1, max(y for _, y in all_rocks) + 1)
cave = np.zeros(shape=shape)
for r in all_rocks:
    cave[r] = 1

STEPS_TO_TRY = [(0, 1), (-1, 1), (1, 1)]

all_sands = set()
current_sand = start
while current_sand[1] <= shape[1]:
    previous_sand = current_sand
    for step in STEPS_TO_TRY:
        next_sand = tuple_add(current_sand, step)
        if next_sand not in all_sands and next_sand not in all_rocks:
            current_sand = next_sand
            break

    if previous_sand == current_sand:
        all_sands.add(current_sand)
        current_sand = start

for s in all_sands:
    cave[s] = 2

print(len(all_sands))

# part 2

all_sands_part2 = set()
current_sand = start
while True:
    previous_sand = current_sand
    for step in STEPS_TO_TRY:
        next_sand = tuple_add(current_sand, step)
        if next_sand not in all_sands_part2 and next_sand not in all_rocks:
            current_sand = next_sand
            break

    if previous_sand == current_sand or current_sand[1] == shape[1]:
        all_sands_part2.add(current_sand)
        current_sand = start

    if previous_sand == current_sand == start:
        break


cave_part2 = np.zeros(shape=(1000, shape[1] + 3))
for s in all_sands_part2:
    cave_part2[s] = 2
for r in all_rocks:
    cave_part2[r] = 1

print(len(all_sands_part2))
