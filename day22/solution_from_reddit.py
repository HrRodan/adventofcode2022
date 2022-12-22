# Source
# https://www.reddit.com/r/adventofcode/comments/zsct8w/2022_day_22_solutions/j194zzx/
# vanZuider
#
# Code (Python 3)
#
# Cube
#
# I don't think this counts as innovative, elegant or efficient (well, it runs in <0.2s) - but it means that I've
# finally caught up to the current puzzle after starting Day 1 on December 17.
#
# Uses no libraries except standard regular expressions (for parsing the movement input string). The playing field is
# an array of strings, padded with spaces on all four sides (which conveniently turns the actual playing field into a
# 1-based matrix, avoiding off-by-one errors when calculating the password).
#
# For part 2, the neighbor-finding function uses a lookup table (tailored to the puzzle data; part 2 does not work
# with the test data), which was carefully handcrafted utilizing the crude drawing posted above.


import re

testdata = """        ...#
        .#..
        #...
        ....
...#.......#
........#...
..#....#....
..........#.
        ...#....
        .....#..
        .#......
        ......#.

10R5L5R10L4R5L5"""

moves = None
field = []

joins = {}


def join(edge1, edge2, dir1, dir2):
    r1 = iter(edge1)
    r2 = iter(edge2)
    while True:
        try:
            p1 = next(r1)
            p2 = next(r2)
        except StopIteration:
            break
        joins[(p1, dir1)] = (p2, dir2)
        joins[(p2, (dir2 + 2) % 4)] = (p1, (dir1 + 2) % 4)


def ground(pos):
    return field[pos[0]][pos[1]]


def neigh(pos, dir):
    if (pos, dir) in joins:
        return joins[(pos, dir)]
    w = len(field[0])
    h = len(field)
    if dir == 0:  # right
        return ((pos[0], (pos[1] + 1) % w), dir)
    elif dir == 1:  # down
        return (((pos[0] + 1) % h, pos[1]), dir)
    elif dir == 2:  # left
        return ((pos[0], (pos[1] - 1) % w), dir)
    elif dir == 3:  # up
        return (((pos[0] - 1) % h, pos[1]), dir)
    else:  # default
        return (pos, dir)


def move(pos, dir):
    n, ndir = neigh(pos, dir)
    if ground(n) == " ":
        while ground(n) == " ":
            n, ndir = neigh(n, ndir)

    if ground(n) == ".":
        return (n, ndir)
    elif ground(n) == "#":
        return (pos, dir)


with open("input.txt", 'r') as f:
    # with StringIO(testdata) as f:
    while l := f.readline():
        if l[0] == '\n':
            continue
        elif l[0].isnumeric():
            moves_orig = l
        else:
            field.append(l[:-1])

width = max(map(len, field))
field = [" " * (width + 2), *[f" {l}".ljust(width + 2) for l in field], " " * (width + 2)]

start = (1, field[1].find('.'))
pos = start
moves = moves_orig
dir = 0

while m := re.match(r"(\d+)(.*)", moves):
    moves = m[2]
    for _ in range(int(m[1])):
        pos, dir = move(pos, dir)
    if m := re.match(r"([RL])(.*)", moves):
        moves = m[2]
        if m[1] == "R":
            dir = (dir + 1) % 4
        elif m[1] == "L":
            dir = (dir - 1) % 4
        else:
            raise Exception(f"Unknown direction token: {m[1]}")
    else:
        print(f"No more direction tokens, remaining string: '{moves}'")

print(dir, pos)
print(1000 * pos[0] + 4 * pos[1] + dir)

# join to cube (hardcoded)

#       a    b
#     f        c
#            d
#     g    d
#   g
# f        c
#        e
# a    e
#   b

# a
join([(1, x) for x in range(51, 101)], [(y, 1) for y in range(151, 201)], 3, 0)
# b
join([(1, x) for x in range(101, 151)], [(200, x) for x in range(1, 51)], 3, 3)
# c
join([(y, 150) for y in range(1, 51)], [(y, 100) for y in range(150, 100, -1)], 0, 2)
# d
join([(50, x) for x in range(101, 151)], [(y, 100) for y in range(51, 101)], 1, 2)
# e
join([(150, x) for x in range(51, 101)], [(y, 50) for y in range(151, 201)], 1, 2)
# f
join([(y, 1) for y in range(101, 151)], [(y, 51) for y in range(50, 0, -1)], 2, 0)
# g
join([(101, x) for x in range(1, 51)], [(y, 51) for y in range(51, 101)], 3, 0)

pos = start
dir = 0
moves = moves_orig

while m := re.match(r"(\d+)(.*)", moves):
    moves = m[2]
    for _ in range(int(m[1])):
        pos, dir = move(pos, dir)
    if m := re.match(r"([RL])(.*)", moves):
        moves = m[2]
        if m[1] == "R":
            dir = (dir + 1) % 4
        elif m[1] == "L":
            dir = (dir - 1) % 4
        else:
            raise Exception(f"Unknown direction token: {m[1]}")
    else:
        print(f"No more direction tokens, remaining string: '{moves}'")

print(dir, pos)
print(1000 * pos[0] + 4 * pos[1] + dir)
