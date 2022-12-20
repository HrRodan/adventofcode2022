from collections import deque

import numpy as np

from utilities import tuple_add_nd

with open('input.txt') as f:
    positions = tuple(tuple(int(x) for x in line.strip().split(',')) for line in f.readlines())

shape = tuple(max(x) + 1 for x in zip(*positions))

lava = np.full(shape=shape, fill_value=0, dtype=np.byte)
lava[tuple(np.transpose(positions))] = 1
lava = np.pad(lava, pad_width=1, mode='constant', constant_values=0)
r1 = sum(np.count_nonzero(np.diff(lava, axis=i, prepend=0, append=0)) for i in range(3))

print(r1)

# part 2
all_zeros = {tuple(x) for x in np.transpose((lava == 0).nonzero())}
all_ones = {tuple(x) for x in np.transpose((lava == 1).nonzero())}
points_to_visit = deque([(0, 0, 0)])
directions = (1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)
edges = set()
while points_to_visit:
    this_point = points_to_visit.pop()
    for d in directions:
        next_point = tuple_add_nd(this_point, d)
        if next_point in all_zeros:
            points_to_visit.append(next_point)
        elif next_point in all_ones:
            edges.add((this_point, next_point))
    all_zeros.discard(this_point)

print(len(edges))
