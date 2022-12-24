import heapq
import math
from collections import defaultdict
from typing import Dict, List

import numpy as np
from scipy.spatial.distance import cdist

from utilities import POINT_TYP, tuple_add

with open('input.txt') as f:
    area_raw = np.array([list(line.strip()) for line in f.readlines()])

# cut outer_area
area_raw = area_raw[1:-1, 1:-1]
shape = area_raw.shape
blizzard_north = area_raw == '^'
blizzard_south = area_raw == 'v'
blizzard_west = area_raw == '<'
blizzard_east = area_raw == '>'
all_points = {tuple(x) for x in np.transpose(area_raw.nonzero())}
repetition_count = math.lcm(shape[0], shape[1])

# precompute blizzard location, repeats after lcm
blizzard_location: Dict[int, np.array] = {}
for i in range(repetition_count):
    blizzard_location[i] = blizzard_east | blizzard_west | blizzard_south | blizzard_north
    blizzard_east = np.roll(blizzard_east, axis=1, shift=1)
    blizzard_north = np.roll(blizzard_north, axis=0, shift=-1)
    blizzard_west = np.roll(blizzard_west, axis=1, shift=-1)
    blizzard_south = np.roll(blizzard_south, axis=0, shift=1)

# precompute neighbors (and self)
neighbors_and_self: Dict[POINT_TYP, List[POINT_TYP]] = defaultdict(list)
for p in all_points:
    neighbors_and_self[p].append(p)
    for d in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
        next_point = tuple_add(p, d)
        if next_point in all_points:
            neighbors_and_self[p].append(next_point)

# add real start and end which are outside numpy array
START = (0, 0)
END = (shape[0] - 1, shape[1] - 1)
REAL_START = (-1, 0)
REAL_END = (END[0] + 1, END[1])
#add real start
neighbors_and_self[REAL_START].extend([START, REAL_START])
neighbors_and_self[START].append(REAL_START)
all_points.add((REAL_START))
#add real end
neighbors_and_self[REAL_END].extend([END, REAL_END])
neighbors_and_self[END].append(REAL_END)
all_points.add((REAL_END))

# precompute cityblock distances to end and start for heap optimization
distances_to_end = {k: int(v[0]) for k, v in zip(all_points, cdist(list(all_points), [REAL_END], metric='cityblock'))}
distances_to_start = {k: int(v[0]) for k, v in
                      zip(all_points, cdist(list(all_points), [REAL_START], metric='cityblock'))}


def find_fastest_path(start: POINT_TYP, end: POINT_TYP, distances, offset_time=0):
    point_times_to_vist = []
    # heap order: min(cityblock distance to end, time, position)
    heapq.heappush(point_times_to_vist, (distances[start], offset_time, start))
    min_time = math.inf
    visited = {(start, offset_time)}

    # Dijkstra's algorithm
    while point_times_to_vist:
        current_distance, current_time, current_postion = heapq.heappop(point_times_to_vist)
        next_time = current_time + 1
        if next_time > min_time:
            continue
        for next_point in neighbors_and_self[current_postion]:
            next_point_time_tuple = (next_point, next_time)
            # REAL Start and REAL END have never blizzards
            if next_point_time_tuple not in visited and \
                    (next_point == REAL_START or
                     next_point == REAL_END or
                     not blizzard_location[next_time % repetition_count][next_point]):
                visited.add(next_point_time_tuple)
                if next_point == end:
                    min_time = min(min_time, next_time)
                    continue
                heapq.heappush(point_times_to_vist, (distances[next_point], next_time, next_point))

    return min_time


r1 = find_fastest_path(REAL_START, REAL_END, distances=distances_to_end)
print(r1)

# part 2
end_start = find_fastest_path(REAL_END, REAL_START, offset_time=r1, distances=distances_to_start)
start_end_2 = find_fastest_path(REAL_START, REAL_END, offset_time=end_start, distances=distances_to_end)
print(start_end_2)
