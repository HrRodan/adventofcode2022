import re

import numpy as np

from utilities import POINT_TYP, tuple_add

with open('input.txt') as f:
    map_raw, path_raw = f.read().split('\n\n')

map_list = [list(line.rstrip()) for line in map_raw.split('\n')]
shape = (len(map_list), max(len(x) for x in map_list))
path = [int(x) if x.isdigit() else x for x in re.findall(r'\d+|[LR]', path_raw)]

map_np = np.zeros(shape=shape, dtype=np.byte)
for x, line in enumerate(map_list):
    for y, c in enumerate(line):
        if c == '.':
            map_np[(x, y)] = 1
        elif c == '#':
            map_np[(x, y)] = 2

map_np = np.pad(map_np, pad_width=1, constant_values=0, mode='constant')


def find_loop_position(np_array: np.array, position: POINT_TYP, direction: POINT_TYP):
    d_x, d_y = direction
    x, y = position
    if d_y == 1:
        return x, np.argwhere(np_array[x]).min()
    if d_y == -1:
        return x, np.argwhere(np_array[x]).max()
    if d_x == 1:
        return np.argwhere(np_array[:, y]).min(), y
    if d_x == -1:
        return np.argwhere(np_array[:, y]).max(), y


turn = {
    'R': {
        (1, 0): (0, -1),
        (0, -1): (-1, 0),
        (-1, 0): (0, 1),
        (0, 1): (1, 0)
    }
}
turn['L'] = {v: k for k, v in turn['R'].items()}

position = (1, np.argwhere(map_np[1]).min())
direction = (0, 1)
for m in path:
    if type(m) != int:
        direction = turn[m][direction]
        continue
    else:
        for _ in range(m):
            next_position = tuple_add(position, direction)
            v = map_np[next_position]
            if v == 1:
                position = next_position
            elif v == 2:
                break
            elif v == 0:
                next_position = find_loop_position(map_np, position, direction)
                v = map_np[next_position]
                if v == 2:
                    break
                else:
                    position = next_position

facing_value = {
    (0, 1): 0,
    (1, 0): 1,
    (0, -1): 2,
    (-1, 0): 3
}

r1 = 1000 * position[0] + 4 * position[1] + facing_value[direction]
print(r1)

# Part 2 by hard coding the edges - no time this christmas, see solution from reddit