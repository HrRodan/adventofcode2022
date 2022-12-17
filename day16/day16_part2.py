import heapq
import re
from copy import copy
from functools import total_ordering
from itertools import product

with open('input.txt') as f:
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

    def all_valves_open(self):
        return all(self.valve_status.values())


start = 'AA'

# part 2

# key ((Point,  Point_elephant), time)
highest_rate = {((start, start), 0): 0}
time_states_to_visit = []

# heap q key: (-rate_total, -time)
heapq.heappush(time_states_to_visit, ((0, 0), ((start, start), ValveStatus())))

# Dijkstra's algorithm
while time_states_to_visit:
    (rate_current, time_current), (valve_current_tuple, valve_status_current) = heapq.heappop(time_states_to_visit)
    if time_current <= -26 or valve_status_current.all_valves_open():
        continue
    time_next = time_current - 1

    for command in product(['move', 'open'], repeat=2):
        # open command only possible if not already open and valve with rate
        if any(v in valves_without_rate or valve_status_current[v] for c, v in zip(command, valve_current_tuple) if
               c == 'open'):
            continue
        # cannot open the same valve twice
        if valve_current_tuple[0] == valve_current_tuple[1] and command == ('open', 'open'):
            continue
        valve_status_next = copy(valve_status_current)
        rate_next = rate_current
        valve_next_list = [[], []]
        for i, (c, valve_current) in enumerate(zip(command, valve_current_tuple)):
            if c == 'open' and not valve_status_next[valve_current]:
                # open valve
                valve_status_next[valve_current] = True
                rate_next = rate_next - (26 + time_next) * valves_with_rate[valve_current]
                valve_next_list[i].append(valve_current)
            if c == 'move':
                # visit next valves
                for valve_next in next_valves[valve_current]:
                    valve_next_list[i].append(valve_next)
        for valves_next in product(valve_next_list[0], valve_next_list[1]):
            next_tuple = (valves_next, time_next)
            if (next_tuple not in highest_rate or highest_rate[next_tuple] > rate_next):
                highest_rate[next_tuple] = rate_next
                heapq.heappush(time_states_to_visit, ((rate_next, time_next), (valves_next, valve_status_next)))

r2 = min(highest_rate.values())
print(-r2)
