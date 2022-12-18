import numpy as np
import scipy

with open('input_test.txt') as f:
    positions = tuple(tuple(int(x) for x in line.strip().split(',')) for line in f.readlines())

shape = tuple(max(x) + 2 for x in zip(*positions))

lava = np.full(shape=shape, fill_value=0, dtype=np.byte)
lava[tuple(np.transpose(positions))] = 1
r1 = sum(np.count_nonzero(np.diff(lava, axis=i, prepend=0, append=0)) for i in range(3))

print(r1)

# part 2
convex_hull = scipy.spatial.ConvexHull(positions, qhull_options='FA')