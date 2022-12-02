from typing import Tuple

letter_map = {
    'X': 'A',
    'Y': 'B',
    'Z': 'C'
}

with open('input.txt') as f:
    strategy = [(z[0], letter_map[z[1]]) for line in f.readlines() for z in [line.strip().split()]]


score = {
    'A': 1,
    'B': 2,
    'C': 3
}

beats = {
    'A': 'C',
    'B': 'A',
    'C': 'B'
}


def get_score(turn: Tuple[str, str]):
    a, b = turn
    b_score = score[b]
    if a == b:
        return b_score + 3
    return b_score + 6 if beats[b] == a else b_score


r1 = sum(get_score(t) for t in strategy)
print(r1)

# part 2
looses = {value: key for key, value in beats.items()}


def get_round(strategy_line: Tuple[str, str]):
    a, result = strategy_line
    if result == 'A':
        return (a, beats[a])
    if result == 'B':
        return (a, a)
    if result == 'C':
        return (a, looses[a])


r2 = sum(get_score(get_round(t)) for t in strategy)
print(r2)
