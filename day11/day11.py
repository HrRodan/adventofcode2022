import operator
import re
from collections import deque
from copy import deepcopy

import numpy as np

with open('input.txt') as f:
    monkeys_raw = f.read().strip().split('\n\n')

monkeys_start = {i: {'items': deque(), 'op': None, 'test': None, 'true_throw': None, 'false_throw': None} for i in
                 range(len(monkeys_raw))}


def get_op(number_re_in):
    if number_re_in:
        number = int(number_re_in.group(0))
        if '+' in line:
            return lambda x: x + number
        elif '*' in line:
            return lambda x: x * number
    else:
        if '+' in line:
            return lambda x: x + x
        elif '*' in line:
            return lambda x: x * x


for i, monkey_raw in enumerate(monkeys_raw):
    for j, line in enumerate(monkey_raw.split('\n')):
        if j == 1:
            monkeys_start[i]['items'].extend(int(x) for x in re.findall(r'\d+', line))
        if j == 2:
            monkeys_start[i]['op'] = get_op(re.search(r'\d+', line))
        if j == 3:
            monkeys_start[i]['test'] = int(re.search(r'\d+', line)[0])
        if j == 4:
            monkeys_start[i]['true_throw'] = int(re.search(r'\d+', line)[0])
        if j == 5:
            monkeys_start[i]['false_throw'] = int(re.search(r'\d+', line)[0])

monkeys_part1 = deepcopy(monkeys_start)

ROUNDS = 20
inspections = {i: 0 for i in range(len(monkeys_part1))}
for _ in range(ROUNDS):
    for m_number, m in monkeys_part1.items():
        while items := m['items']:
            item = items.popleft()
            inspections[m_number] += 1
            worry_level = m['op'](item) // 3
            test_bool = worry_level % m['test'] == 0
            if test_bool:
                monkeys_part1[m['true_throw']]['items'].append(worry_level)
            else:
                monkeys_part1[m['false_throw']]['items'].append(worry_level)

r1 = operator.mul(*sorted(inspections.values())[-2:])
print(r1)

# part2
monkeys_part2 = deepcopy(monkeys_start)
# all primes
#https://en.wikipedia.org/wiki/Modular_arithmetic#Properties
ALL_TESTS = [x['test'] for x in monkeys_part2.values()]
mod_all = np.prod(ALL_TESTS)


def get_divisors(number: int):
    return [x for x in ALL_TESTS if number % x == 0]


ROUNDS_part2 = 10000
inspections_part2 = {i: 0 for i in range(len(monkeys_part2))}
for _ in range(ROUNDS_part2):
    for m_number, m in monkeys_part2.items():
        while items := m['items']:
            item = items.popleft()
            inspections_part2[m_number] += 1
            worry_level = m['op'](item) % mod_all
            test_bool = worry_level % m['test'] == 0
            if test_bool:
                monkeys_part2[m['true_throw']]['items'].append(worry_level)
            else:
                monkeys_part2[m['false_throw']]['items'].append(worry_level)

r2 = operator.mul(*sorted(inspections_part2.values())[-2:])
print(r2)
