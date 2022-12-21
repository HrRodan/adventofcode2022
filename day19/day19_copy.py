import heapq
import operator
import re
from copy import deepcopy, copy
from functools import total_ordering, reduce
from typing import Optional

with open('input.txt') as f:
    blueprints = [tuple((x[0], (x[1], 0, 0, 0), (x[2], 0, 0, 0), (x[3], x[4], 0, 0), (x[5], 0, x[6], 0))) for line in
                  f.readlines()
                  for x in
                  [[int(x) for x in re.findall(r'\d+', line.strip())]]]


@total_ordering
class Robots():
    def __init__(self, blueprint, total_time=24):
        _, *self.robots_costs = blueprint
        self.max_costs = tuple(max(x) for x in zip(*self.robots_costs))
        self.count_robots = [1, 0, 0, 0]
        self.stock = (0, 0, 0, 0)
        self.minutes = 0
        self.total_time = total_time
        self.can_build = (0, 0, 0, 0)
        self.remaining = total_time
        self.buildable_robots = [None]

    def __hash__(self):
        return hash((self.count_robots_tuple, self.stock, self.minutes))

    def __eq__(self, other):
        return self.__hash__() == other.__hash__()

    def __lt__(self, other):
        return self.count_robots_tuple < other.count_robots_tuple

    @property
    def count_robots_tuple(self):
        return tuple(self.count_robots[::-1])

    @property
    def reversed_stock_count(self):
        return tuple(self.stock[::-1])

    @property
    def reversed_stock_count_negative(self):
        return tuple(-x for x in self.stock[::-1])

    @property
    def max_geodes(self):
        """Max geodes this state can produce given the remaining time and built robots"""
        return self.stock[3]+ self.remaining * self.count_robots[3]

    @property
    def max_geode_potential(self):
        """Max geodes this state can produce given the remaining time, built robots, and potential robots"""
        return self.max_geodes + self.remaining * (self.remaining - 1) // 2

    def run_one_minute(self, which_robot: Optional[int] = None):
        if which_robot is not None:
            self.stock = tuple(
                y - x + z for x, y, z in zip(self.robots_costs[which_robot], self.stock, self.count_robots))
            self.count_robots[which_robot] += 1
        else:
            self.stock = tuple(x + z for x, z in zip(self.stock, self.count_robots))
        self.can_build = tuple(all(y <= x for y, x in zip(self.robots_costs[i], self.stock)) for i in range(4))
        self.minutes += 1
        self.remaining = self.total_time - self.minutes
        self.buildable_robots = self.get_buildable_robots()

    def get_buildable_robots(self):
        buildable_robots = []
        if self.can_build[3]:
            buildable_robots.append(3)
        buildable_robots.extend(
            i for i, c, r in zip(range(3), self.max_costs, self.count_robots) if self.can_build[i] and r < c)

        return buildable_robots + [None]

    def copy_robot(self):
        new = copy(self)
        new.count_robots = copy(self.count_robots)
        return new


def get_highest_geode_count_from_blueprint(blueprint, total_time = 24):
    # heap q key: (-rate_total, -time)
    time_states_to_visit = []
    robots_current: Robots
    heapq.heappush(time_states_to_visit, (0, 0, 0, Robots(blueprint, total_time)))
    max_potential = 0
    max_geodes = 0
    visited = {hash(Robots(blueprint))}

    # key (time)
    # highest_geode_count = {(0, (0, 0, 0, 1)): (0, 0, 0, 0)}

    # Dijkstra's algorithm
    ii = 0
    while time_states_to_visit:
        ii += 1
        *_, robots_current = heapq.heappop(time_states_to_visit)
        if robots_current.minutes >= total_time:
            continue
        if ii % 100000 == 0:
            print(ii)
            print(len(time_states_to_visit))
            print(max_geodes)
        for next_robot_to_build in robots_current.buildable_robots:
            robots_next = robots_current.copy_robot()
            robots_next.run_one_minute(next_robot_to_build)
            time_next = robots_next.minutes
            max_potential_next = robots_next.max_geode_potential
            hash_val = hash(robots_next)
            if (time_next <= total_time and max_potential_next > max_geodes and hash_val not in visited):
                visited.add(hash_val)
                max_geodes_next = robots_next.max_geodes
                max_geodes = max(max_geodes, max_geodes_next)
                stock_count_next_reversed_negativ = robots_next.reversed_stock_count_negative
                heapq.heappush(time_states_to_visit,
                               (-time_next, stock_count_next_reversed_negativ[0:3], robots_next))

    return max_geodes


# r1 = sum(get_highest_geode_count_from_blueprint(b) * b[0] for b in blueprints)
# print(r1)

r2 = [get_highest_geode_count_from_blueprint(b, 32) for b in blueprints[:3]]
r2_result = reduce(operator.mul, r2)
print(r2_result)

# 1869 too low
# 1948 too low
