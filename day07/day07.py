import re
from collections import deque, defaultdict

with open('input.txt') as f:
    commands = [line.strip() for line in f.readlines()]


def parse_dir(commands_raw):
    current_path = deque()
    files = []
    dir_structure = defaultdict(set)
    for c in commands_raw:
        if c == "$ cd /":
            current_path = deque("/")
        elif c == "$ cd ..":
            current_path.pop()
        elif c.startswith("$ cd"):
            current_path.append(c.split()[-1])
        elif c.startswith("dir"):
            next_dir = current_path.copy()
            next_dir.append(c.split()[-1])
            next_dir_tuple = tuple(next_dir)
            dir_structure[tuple(current_path)].add(next_dir_tuple)
            if next_dir_tuple not in dir_structure:
                dir_structure[next_dir_tuple] = set()
        elif (x := re.match(r'(\d+) ([a-zA-Z\.]+)', c)):
            files.append((tuple(current_path), int(x.groups()[0]), x.groups()[1]))

    return dir_structure, files


def get_dir_sizes(files):
    dir_sizes = defaultdict(int)
    for dir_, file_size, _ in files:
        dir_sizes[dir_] += file_size
    return dir_sizes


def get_dir_sizes_total(directory_structure, directory_sizes):
    dir_sizes_total = defaultdict(int)
    # sort by depth of directory
    directory_structure_sorted = dict(sorted(directory_structure.items(), key=lambda x: -len(x[0])))
    # loop through deepest dirs first
    for top_dir, sub_dirs in directory_structure_sorted.items():
        dir_sizes_total[top_dir] += directory_sizes[top_dir]
        for sub_dir in sub_dirs:
            dir_sizes_total[top_dir] += dir_sizes_total[sub_dir] if directory_structure[sub_dir] else directory_sizes[
                sub_dir]

    return dir_sizes_total


dir_structure, all_files = parse_dir(commands_raw=commands)
dir_sizes = get_dir_sizes(all_files)
dir_sizes_total = get_dir_sizes_total(dir_structure, dir_sizes)

LIMIT = 100000
r1 = sum(value for value in dir_sizes_total.values() if value <= LIMIT)
print(r1)

# part 2
TOTAL_DISK_SPACE = 70000000
UPDATE_SPACE = 30000000

required_space = abs(TOTAL_DISK_SPACE - UPDATE_SPACE - dir_sizes_total[("/",)])
r2 = min(value for value in dir_sizes_total.values() if value >= required_space)
print(r2)
