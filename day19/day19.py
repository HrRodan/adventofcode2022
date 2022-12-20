import heapq
import re
from copy import copy
from functools import total_ordering
from typing import Optional

with open('input_test.txt') as f:
    blueprints = [tuple((x[0], (x[1], 0, 0, 0), (x[2], 0, 0, 0), (x[3], x[4], 0, 0), (x[5], 0, x[6], 0))) for line in
                  f.readlines()
                  for x in
                  [[int(x) for x in re.findall(r'\d+', line.strip())]]]


@total_ordering
class Robots():
    def __init__(self, blueprint):
        self.blueprint_number, *self.robots_costs = blueprint
        self.max_costs = [max(x) for x in zip(*self.robots_costs)]
        self.count_robots = [1, 0, 0, 0]
        self.stock = [0, 0, 0, 0]
        self.minutes = 0

    def __hash__(self):
        return hash((self.count_robots_tuple, tuple(self.stock), self.minutes))

    def __eq__(self, other):
        return self.__hash__() == other.__hash__()

    def __lt__(self, other):
        return self.count_robots_tuple < other.count_robots_tuple

    @property
    def count_robots_tuple(self):
        return tuple(self.count_robots[::-1])

    @property
    def negative_geode_count(self):
        return -self.stock[3]

    @property
    def reversed_stock_count(self):
        return tuple(self.stock[::-1])

    @property
    def reversed_stock_count_negative(self):
        return tuple(-x for x in self.stock[::-1])

    @property
    def remaining(self):
        return 24 - self.minutes

    @property
    def max_geodes(self):
        """Max geodes this state can produce given the remaining time and built robots"""
        return (
                self.stock[3]
                + self.remaining * self.count_robots[3]
        )

    @property
    def max_geode_potential(self):
        """Max geodes this state can produce given the remaining time, built robots, and potential robots"""
        return self.max_geodes + self.remaining * (self.remaining - 1) // 2

    def run_one_minute(self, which_robot: Optional[int] = None):
        if which_robot is not None:
            new_stock = self.stock.copy()
            for i, costs, stock in zip(range(4), self.robots_costs[which_robot], self.stock):
                if costs > stock:
                    raise ValueError("Robot to expensive!")
                else:
                    new_stock[i] -= costs
            self.stock = new_stock
        for i, current_stock, robot in zip(range(4), self.stock, self.count_robots):
            self.stock[i] += robot
        self.minutes += 1
        if which_robot is not None:
            self.count_robots[which_robot] += 1

    def can_build(self, which_robot: int):
        return all(y <= x for y, x in zip(self.robots_costs[which_robot], self.stock))

    def get_buildable_robots(self):
        buildable_robots = []
        if self.can_build(3):
            buildable_robots.append(3)
        for i, c, r in zip(range(3), self.max_costs, self.count_robots):
            if self.can_build(i) and r < c:
                buildable_robots.append(i)
        return buildable_robots + [None]

    # def get_buildable_robots(self):
    #     buildable_robots = []
    #     if self.can_build(3):
    #         buildable_robots.append(3)
    #     buildable_robots.extend(i for i in range(2, 0, -1) if self.can_build(i) and self.count_robots[i] == 0)
    #     if self.count_robots[2] != 0:
    #         geode_ore, _, geode_obsidian, _ = self.robots_costs[3]
    #         if geode_ore / geode_obsidian > self.count_robots[0] / self.count_robots[2] and self.can_build(0):
    #             buildable_robots.append(0)
    #         elif geode_ore / geode_obsidian < self.count_robots[0] / self.count_robots[2] and self.can_build(2):
    #             buildable_robots.append(2)
    #     if self.count_robots[1] != 0:
    #         obsidian_ore, obsidian_clay, _, _ = self.robots_costs[2]
    #         if obsidian_ore / obsidian_clay > self.count_robots[0] / self.count_robots[1] and self.can_build(0):
    #             buildable_robots.append(0)
    #         elif obsidian_ore / obsidian_clay < self.count_robots[0] / self.count_robots[1] and self.can_build(1):
    #             buildable_robots.append(1)
    #     if len(buildable_robots) == 4:
    #         return buildable_robots
    #     if not buildable_robots and self.can_build(0):
    #         buildable_robots.append(0)
    #     return buildable_robots + [None] if buildable_robots else [None]

    def __copy__(self):
        new = Robots(blueprints[0])
        new.blueprint_number = self.blueprint_number
        new.robots_costs = self.robots_costs
        new.count_robots = self.count_robots.copy()
        new.stock = self.stock.copy()
        new.minutes = self.minutes
        return new

    # def run(self, rounds: int):
    #     for i in range(1, rounds + 1):
    #         a = self.get_next_robot_to_build_part1()
    #         self.run_one_minute(a)
    #         print(f"{i} : {a} : {self.stock} : {self.count_robots}")


def get_highest_geode_count_from_blueprint(blueprint):
    # heap q key: (-rate_total, -time)
    time_states_to_visit = []
    robots_current: Robots
    heapq.heappush(time_states_to_visit, ((0, 0), Robots(blueprint)))
    max_potential = 0
    max_geodes = 0
    visited = {Robots(blueprint)}

    # key (time)
    # highest_geode_count = {(0, (0, 0, 0, 1)): (0, 0, 0, 0)}

    # Dijkstra's algorithm
    ii = 0
    while time_states_to_visit:
        ii += 1
        (geode_count_current, time_current), robots_current = heapq.heappop(time_states_to_visit)
        if robots_current.minutes >= 24:
            continue
        if ii%100000==0:
            print(ii)
            print(len(time_states_to_visit))
            print(max_geodes)
            print(time_current)
        for next_robot_to_build in robots_current.get_buildable_robots():
            robots_next = copy(robots_current)
            robots_next.run_one_minute(next_robot_to_build)
            time_next = robots_next.minutes
            max_potential_next = robots_next.max_geode_potential
            if (time_next <= 24 and max_potential_next > max_geodes and robots_next not in visited):
                visited.add(robots_next)
                max_geodes_next = robots_next.max_geodes
                max_geodes = max(max_geodes, max_geodes_next)
                stock_count_next_reversed_negativ = robots_next.reversed_stock_count_negative
                heapq.heappush(time_states_to_visit,
                               ((-time_next, stock_count_next_reversed_negativ), robots_next))

    return max_geodes


r1 = sum(get_highest_geode_count_from_blueprint(b) * b[0] for b in blueprints)
print(r1)

# 1869 too low
