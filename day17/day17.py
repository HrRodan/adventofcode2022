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
        self.cave = np.full(shape=(7, 5000), fill_value=False, dtype=bool)
        self.height = -1

    def add_rock_to_cave(self, rock: Rock):
        self.cave[tuple(np.transpose(rock.points))] = True
        self.height = np.max(np.argwhere(cave_part1.cave), axis=0)[1]



jet_pattern_it = cycle(jet_pattern)
rock_it = cycle([RockMinus, RockCross, RockEl, RockI, RockSquare])
cave_part1 = Cave()
for _ in range(2022):
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

print(cave_part1.height+1)
