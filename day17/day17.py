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
        self.cave = np.full(shape=(7, 3000), fill_value=False, dtype=bool)
        self.height = -1
        self.height_addon = 0
        self.height_total = self.height

    def add_rock_to_cave(self, rock: Rock):
        self.cave[tuple(np.transpose(rock.points))] = True
        self.height = np.max(np.argwhere(self.cave), axis=0)[1]
        if self.height > 2000:
            self.cave = np.hstack([self.cave[:, 1000:], np.full(shape=(7, 1000), fill_value=False)])
            self.height_addon += 1000
            self.height = self.height - 1000
        self.height_total = self.height + self.height_addon


patterns = set()


def populate_cave(number_rocks: int):
    jet_pattern_it = cycle(jet_pattern)
    rock_it = cycle([RockMinus, RockCross, RockEl, RockI, RockSquare])
    cave_to_populate = Cave()
    for _ in range(number_rocks):
        this_rock: Rock = next(rock_it)(cave_to_populate)
        while True:
            # jet
            this_jet = next(jet_pattern_it)
            if this_jet == '<':
                this_rock.move_left()
            elif this_jet == '>':
                this_rock.move_right()
            # down
            if not this_rock.move_down():
                cave_to_populate.add_rock_to_cave(this_rock)
                break

    return cave_to_populate


print(populate_cave(2022).height_total + 1)


# part 2
# find repetition

def find_repeating_pattern():
    jet_pattern_it_p2 = cycle(enumerate(jet_pattern))
    rock_it_p2 = cycle([RockMinus, RockCross, RockEl, RockI, RockSquare])
    cave_to_repeat = Cave()
    patterns_p2 = {}
    ii = 0
    while True:
        ii += 1
        this_rock: Rock = next(rock_it_p2)(cave_to_repeat)
        while True:
            # jet
            jet_index, this_jet = next(jet_pattern_it_p2)
            if this_jet == '<':
                this_rock.move_left()
            elif this_jet == '>':
                this_rock.move_right()
            # down
            if not this_rock.move_down():
                cave_to_repeat.add_rock_to_cave(this_rock)
                break
        if ii > 100:
            new_pattern = hash(tuple(
                (cave_to_repeat.cave[:,
                 min(0, cave_to_repeat.height - 100):cave_to_repeat.height + 1].flatten()))), type(this_rock), jet_index
            if new_pattern in patterns_p2:
                repeating_index_height = cave_to_repeat.height_total, ii
                break
            else:
                patterns_p2[new_pattern] = (cave_to_repeat.height_total, ii)

    return patterns_p2[new_pattern], repeating_index_height


# %%
a = find_repeating_pattern()

delta_height, delta_i = (y - x for x, y in zip(*a))

count_repeats, mod = divmod(1000000000000, delta_i)

r2 = count_repeats * delta_height + populate_cave(mod).height_total + 1
print(r2)
