import heapq
import re
from copy import copy
from functools import total_ordering

with open('input_test.txt') as f:
    valves = [(x.group(1), int(x.group(2)), x.group(3).split(', ')) for line in f.readlines() for x in
              [re.match(r'^Valve ([A-Z]{2}).+rate=(\d+).+valves? ([A-Z, ]+)+$', line.strip())]]

next_valves = {k: v for k, _, v in valves}
valves_with_rate = {k: v for k, v, _ in sorted(valves) if v != 0}
valves_without_rate = {k for k, v, _ in valves if v == 0}
max_rate = sum(valves_with_rate.values())


@total_ordering
class ValveStatus():
    def __init__(self):
        self.valve_status = {k: False for k in valves_with_rate}

    def __hash__(self):
        return hash(tuple(self.valve_status.values()))

    def __lt__(self, other):
        return sum(self.valve_status.values()) < sum(self.valve_status.values())

    def __eq__(self, other):
        return self.__hash__() == other.__hash__()

    def __repr__(self):
        return str(self.valve_status)

    def get(self, value, default):
        return self.valve_status.get(value, default)

    def __getitem__(self, arg):
        return self.valve_status[arg]

    def __setitem__(self, key, value):
        self.valve_status[key] = value

    def __copy__(self):
        new = ValveStatus()
        new.valve_status = self.valve_status.copy()
        return new

    def count(self):
        return sum(self.valve_status.values())

    def count_closed(self):
        return sum(not x for x in self.valve_status.values())


all_valves_closed = {k: False for k in valves_with_rate}

start = 'AA'

# key (Point, valve_status, time)
highest_rate = {(start, ValveStatus(), 0): 0}
time_states_to_visit = []

# heap q key: (-rate_total, -time)
heapq.heappush(time_states_to_visit, ((0, 0), (start, ValveStatus())))

# Dijkstra's algorithm
while time_states_to_visit:
    (rate_current, time_current), (valve_current, valve_status_current) = heapq.heappop(time_states_to_visit)
    if time_current <= -30:
        continue
    time_next = time_current - 1
    # open this valve
    if not valve_status_current.get(valve_current, True):
        valve_status_next = copy(valve_status_current)
        valve_status_next[valve_current] = True
        rate_next = rate_current - (30 + time_next) * valves_with_rate[valve_current]
        next_tuple = (valve_current, valve_status_next, time_next)
        if next_tuple not in highest_rate or highest_rate[next_tuple] > rate_next:
            highest_rate[next_tuple] = rate_next
            heapq.heappush(time_states_to_visit, ((rate_next, time_next), (valve_current, valve_status_next)))
    # visit next valves
    for valve_next in next_valves[valve_current]:
        valve_status_current_copy = copy(valve_status_current)
        next_tuple = (valve_next, valve_status_current_copy, time_next)
        if (next_tuple not in highest_rate or highest_rate[
            next_tuple] > rate_current):
            highest_rate[next_tuple] = rate_current
            heapq.heappush(time_states_to_visit, ((rate_current, time_next), (valve_next, valve_status_current_copy)))

r1 = min(highest_rate.values())
print(-r1)
