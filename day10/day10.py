from itertools import count

import matplotlib.pyplot as plt
import numpy as np

with open('input.txt') as f:
    commands = [(2, int(x[1])) if len(x) == 2 else (1, 0) for line in f.readlines() for x in [line.strip().split()]]

cycle = 1
signal_strength = 0
register_value = 1
cycle_to_count = count(20, 40)
next_cycle_to_count = next(cycle_to_count)
crt = [False for _ in range(240)]
crt_position = 0

for c, v in commands:
    cycle_previous = cycle
    cycle += c
    # part 1
    while cycle_previous <= next_cycle_to_count < cycle:
        signal_strength += next_cycle_to_count * register_value
        next_cycle_to_count = next(cycle_to_count)

    # part 2
    for _ in range(c):
        if register_value - 1 <= crt_position % 40 <= register_value + 1:
            crt[crt_position] = True
        crt_position += 1

    register_value += v

# part 1
print(signal_strength)

# part2
crt_array = np.array(crt).reshape(6, 40)
plt.imshow(crt_array)
plt.savefig('part2.png')
plt.show()
