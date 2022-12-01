
with open('input.txt') as f:
    calories = [[int(x) for x in y.split('\n')] for y in f.read().split('\n\n')]

calories_sum = [sum(x) for x in calories]

r1 = max(calories_sum)
print(r1)

r2 = sum(sorted(calories_sum)[-3:])
print(r2)