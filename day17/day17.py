from copy import deepcopy
from itertools import cycle

import numpy as np

with open('input.txt') as f:
    jet_pattern = list(f.readline().strip())


class Rock():
    def __init__(self, cave):
        self.cave = cave
        self.start_height = cave.height + 4
        self.points = tuple()

    @property
    def left_point(self):
        return min(x for x, _ in self.points)

    @property
    def right_point(self):
        return max(x for x, _ in self.points)

    @property
    def low_point(self):
        return min(y for _, y in self.points)

    def move_right(self):
        point_test = tuple((x + 1, y) for x, y in self.points)
        if self.right_point != 6 and not any(self.cave.cave[x] for x in point_test):
            self.points = point_test

    def move_left(self):
        point_test = tuple((x - 1, y) for x, y in self.points)
        if self.left_point != 0 and not any(self.cave.cave[x] for x in point_test):
            self.points = point_test

    def move_down(self):
        point_test = tuple((x, y - 1) for x, y in self.points)
        if any(self.cave.cave[x] for x in point_test) or self.low_point == 0:
            return False
        self.points = point_test
        return True


class RockMinus(Rock):
    def __init__(self, cave):
        super().__init__(cave)
        self.points = (2, self.start_height), (3, self.start_height), (4, self.start_height), (5, self.start_height)


class RockCross(Rock):
    def __init__(self, cave):
        super().__init__(cave)
        self.points = (3, self.start_height), (2, self.start_height + 1), (3, self.start_height + 1), (
            4, self.start_height + 1), (3, self.start_height + 2)


class RockEl(Rock):
    def __init__(self, cave):
        super().__init__(cave)
        self.points = (2, self.start_height), (3, self.start_height), (4, self.start_height), (
            4, self.start_height + 1), (4, self.start_height + 2)


class RockI(Rock):
    def __init__(self, cave):
        super().__init__(cave)
        self.points = (2, self.start_height), (2, self.start_height + 1), (2, self.start_height + 2), (
            2, self.start_height + 3)


class RockSquare(Rock):
    def __init__(self, cave):
        super().__init__(cave)
        self.points = (2, self.start_height), (2, self.start_height + 1), (3, self.start_height), (
            3, self.start_height + 1)


class Cave():
    def __init__(self):
        self.cave = np.full(shape=(7, 300), fill_value=False, dtype=bool)
        self.height = -1
        self.height_addon = 0
        self.height_total = self.height

    def add_rock_to_cave(self, rock: Rock):
        self.cave[tuple(np.transpose(rock.points))] = True
        self.height = np.max(np.argwhere(cave_part1.cave), axis=0)[1]
        if self.height > 200:
            self.cave = np.hstack([self.cave[:, 100:], np.full(shape=(7, 100), fill_value=False)])
            self.height_addon += 100
            self.height = self.height - 100
        self.height_total = self.height + self.height_addon

patterns = set()
jet_pattern_it = cycle(jet_pattern)
rock_it = cycle([RockMinus, RockCross, RockEl, RockI, RockSquare])
cave_part1 = Cave()
for i in range(len(jet_pattern*6)):
    this_rock: Rock = next(rock_it)(cave_part1)
    while True:
        # jet
        this_jet = next(jet_pattern_it)
        if this_jet == '<':
            this_rock.move_left()
        elif this_jet == '>':
            this_rock.move_right()
        # down
        if not this_rock.move_down():
            cave_part1.add_rock_to_cave(this_rock)
            break

    new_pattern = tuple(cave_part1.cave[:, min(cave_part1.height - 100,0):].flatten()), type(this_rock)
    if new_pattern in patterns:
        print(i)
    else:
        patterns.add(new_pattern)

print(cave_part1.height_total + 1)

# part 2
# find repetition

jet_pattern_it = cycle(jet_pattern)
rock_it = cycle([RockMinus, RockCross, RockEl, RockI, RockSquare])
cave_part2 = Cave()

patterns = {}
repeating_structure = None
repeating_height = 0
repeating_index = 0

ii = 0
while True:
    ii += 1
    this_rock: Rock = next(rock_it)(cave_part2)
    while True:
        # jet
        this_jet = next(jet_pattern_it)
        if this_jet == '<':
            this_rock.move_left()
        elif this_jet == '>':
            this_rock.move_right()
        # down
        if not this_rock.move_down():
            cave_part2.add_rock_to_cave(this_rock)
            break
    new_pattern = tuple(cave_part2.cave[:, min(cave_part2.height - 100, 0):cave_part2.height+1].flatten()), type(this_rock)
    if new_pattern in patterns:
        repeating_structure = deepcopy(cave_part2)
        old_height = patterns[new_pattern]
        repeating_index = ii
        repeating_height = cave_part2.height_total
        break
    else:
        patterns[new_pattern] = cave_part2.height_total
