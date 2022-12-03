from itertools import islice, chain

with open('input.txt') as f:
    rucksacks = [[x[: len(x) // 2], x[len(x) // 2:]] for line in f.readlines() for l in [line.strip()] for x in
                 [list(l)]]

small_letter_score = dict(zip((chr(c) for c in range(ord('a'), ord('z') + 1)), range(1, 27)))
capital_letter_score = dict(zip((chr(c) for c in range(ord('A'), ord('Z') + 1)), range(27, 53)))
letter_score = small_letter_score | capital_letter_score

score = 0
for r in rucksacks:
    c1, c2 = r
    error_letter = set(c1).intersection(set(c2))
    score += letter_score[error_letter.pop()]

print(score)

# part 2
r_iter = iter(rucksacks)
score_part2 = 0

while (group := list(islice(r_iter, 3))):
    for i, g in enumerate(group):
        all_items = set(chain(*g))
        common_items = all_items if i == 0 else common_items & all_items
    score_part2 += letter_score[common_items.pop()]

print(score_part2)
