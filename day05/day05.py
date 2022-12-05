import re
from collections import deque
from itertools import zip_longest, islice

with open('input.txt') as f:
    start_position_raw, movements_raw = f.read().split('\n\n')

#transpose array for easier reading
start_postion = []
for s in islice(zip_longest(*start_position_raw.split('\n')[:-1]), 1, None, 4):
    start_postion.append(deque(x for x in s if (x and x.strip())))

movements = [tuple(int(x) for x in re.findall(r'\d+',line.strip())) for line in movements_raw.strip().split('\n')]

current_postion = [s.copy() for s in start_postion]

for count_number, from_stack, to_stack in movements:
    for _ in range(count_number):
        current_postion[to_stack-1].appendleft(current_postion[from_stack-1].popleft())

top_crates = ''.join([x.popleft() for x in current_postion])
print(top_crates)

#part 2
current_postion_part2 = [s.copy() for s in start_postion]

for count_number, from_stack, to_stack in movements:
    crates_to_move = [current_postion_part2[from_stack-1].popleft() for _ in range(count_number)]
    current_postion_part2[to_stack-1].extendleft(crates_to_move[::-1])

top_crates_part2 = ''.join([x.popleft() for x in current_postion_part2])
print(top_crates_part2)