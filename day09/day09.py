from typing import Tuple

with open('input.txt') as f:
    steps = [(x[0], int(x[1])) for line in f.readlines() for x in [line.strip().split()]]

POINT_TYP = Tuple[int, int]

DIRECTIONS = {
    'R': (1, 0),
    'L': (-1, 0),
    'U': (0, 1),
    'D': (0, -1)
}

sign = lambda x: -1 if x < 0 else (1 if x > 0 else 0)


def tuple_add(t1: POINT_TYP, t2: POINT_TYP):
    return (t1[0] + t2[0], t1[1] + t2[1])


def move_tail(current_tail: POINT_TYP, current_head: POINT_TYP):
    diff_x = current_head[0] - current_tail[0]
    diff_y = current_head[1] - current_tail[1]
    if -1 <= diff_x <= 1 and -1 <= diff_y <= 1:
        return (0, 0)
    else:
        return (sign(diff_x), sign(diff_y))


head = (0, 0)
tail = (0, 0)
visited = {(0, 0)}
for direction, count in steps:
    move_direction = DIRECTIONS[direction]
    for _ in range(count):
        head = tuple_add(head, move_direction)
        tail = tuple_add(tail, move_tail(tail, head))
        visited.add(tail)

print(len(visited))

# part 2
head = (0, 0)
knots = [(0, 0) for _ in range(9)]
visited_part2 = {(0, 0)}
for direction, count in steps:
    move_direction = DIRECTIONS[direction]
    for _ in range(count):
        head = tuple_add(head, move_direction)
        for i, knot in enumerate(knots):
            if i == 0:
                knots[0] = tuple_add(knot, move_tail(knot, head))
            else:
                knots[i] = tuple_add(knot, move_tail(knot, knots[i - 1]))
            if i == 8:
                visited_part2.add(knots[i])

print(len(visited_part2))
