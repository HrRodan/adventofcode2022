import re

with open('input.txt') as f:
    pairs = [[int(x) for x in re.findall(r'\d+', line.strip())]for line in f.readlines()]

count_contains = sum((a1 >= b1 and a2 <= b2) or (b1 >= a1 and b2 <= a2) for a1, a2, b1, b2 in pairs)

print(count_contains)


count_overlap = sum(b1 <= a1 <= b2 or b1 <= a2 <= b2 or a1 <= b1 <= a2 or a1 <= b2 <= a2 for a1, a2, b1, b2 in pairs)
print(count_overlap)