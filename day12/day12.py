import networkx as nx
import numpy as np

from utilities import *

with open('input.txt') as f:
    height_map = np.array([[ord(x) for x in line.strip()] for line in f.readlines()]).astype(int)

start = tuple(np.argwhere(height_map == ord('S'))[0])
end = tuple(np.argwhere(height_map == ord('E'))[0])
# replace start and end
height_map[start] = ord('a')
height_map[end] = ord('z')
all_elements = {tuple(x) for x in np.transpose(height_map.nonzero())}
all_directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]

G = nx.DiGraph()

for e in all_elements:
    current_height = height_map[e]
    for d in all_directions:
        test_location = tuple_add(e, d)
        if test_location in all_elements and height_map[test_location] - current_height <= 1:
            G.add_edge(e, test_location)

r1 = nx.shortest_path_length(G, start, end)
print(r1)

# part2
all_low_elements = [tuple(x) for x in tuple(np.argwhere(height_map == ord('a')))]
all_path_lengths = []
for e in all_low_elements:
    try:
        all_path_lengths.append(nx.shortest_path_length(G, e, end))
    except nx.NetworkXNoPath:
        continue

r2 = min(all_path_lengths)
print(r2)
