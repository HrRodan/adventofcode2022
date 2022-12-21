import operator
import re
from copy import deepcopy
from typing import Dict

import sympy
from sympy import Eq
from sympy.parsing.sympy_parser import parse_expr

with open('input.txt') as f:
    monkeys_raw = [line.strip() for line in f.readlines()]

monkeys: Dict[str, Dict] = {}
for monkey in monkeys_raw:
    m = re.findall(r'[a-z]{4}', monkey)
    if len(m) == 1:
        m_value = re.search(r'\d+', monkey)[0]
        monkeys[m[0]] = {'type': 0, 'value': int(m_value)}
    if len(m) == 3:
        op = re.search(r'[+\-/*]', monkey)[0]
        op_py = None
        if op == '+':
            op_py = operator.add
        elif op == '*':
            op_py = operator.mul
        elif op == '/':
            op_py = operator.truediv
        elif op == '-':
            op_py = operator.sub
        monkeys[m[0]] = {'type': 1, 'op': op_py, 'op_raw': op, 'monkey1': m[1], 'monkey2': m[2]}


def traverse_monkey(start='root'):
    m = monkeys[start]
    if m['type'] == 0:
        return m['value']
    else:
        return m['op'](traverse_monkey(m['monkey1']), traverse_monkey(m['monkey2']))


r1 = traverse_monkey()
print(int(r1))
monkeys_part_2 = deepcopy(monkeys)
monkeys_part_2['root']['op_raw'] = '=='
monkeys_part_2['root']['op'] = operator.eq


def traverse_monkey_part2(start='root'):
    # always return wheter current branch contains me yelling
    if start == 'humn':
        return 'X', True
    m = monkeys_part_2[start]
    if m['type'] == 0:
        return m['value'], False
    m1, m1_contains_me = traverse_monkey_part2(m['monkey1'])
    m2, m2_contains_me = traverse_monkey_part2(m['monkey2'])
    if not m1_contains_me and not m2_contains_me:
        return int(m['op'](m1, m2)), False
    # prevent abundance of brackets
    m1_str = f'({m1})' if m1_contains_me else str(m1)
    m2_str = f'({m2})' if m2_contains_me else str(m2)
    return f'{m1_str}{m["op_raw"]}{m2_str}', True


r2_sym = Eq(*[parse_expr(x) for x in traverse_monkey_part2()[0].split('==')])
r2 = sympy.solve(r2_sym, 'X')[0]
print(r2)
