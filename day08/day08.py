from functools import reduce

import numpy as np

with open('input.txt') as f:
    forest = np.array([[int(x) for x in line.strip()] for line in f.readlines()]).astype(np.byte)

size = forest.shape[0]
visible_trees = np.full(shape=forest.shape, fill_value=False)

# horizontal
for k in (1, -1):
    forest_horizontal = forest.copy()
    visible_horizontal = np.full(shape=forest.shape, fill_value=False)
    for i in range(size):
        forest_horizontal[:, i] = np.max(forest_horizontal[:, i::k], axis=1)

    for i in range(size):
        if i in (size - 1, 0):
            visible_horizontal[:, i] = True
        else:
            visible_horizontal[:, i] = np.logical_and(forest[:, i] == forest_horizontal[:, i],
                                                      forest_horizontal[:, i] != forest_horizontal[:, i + k * 1])
    visible_trees = np.logical_or(visible_trees, visible_horizontal)

# vertical
for k in (1, -1):
    forest_vertical = forest.copy()
    visible_vertical = np.full(shape=forest.shape, fill_value=False)
    for i in range(size):
        forest_vertical[i, :] = np.max(forest_vertical[i::k, :], axis=0)

    for i in range(size):
        if i in (size - 1, 0):
            visible_vertical[i, :] = True
        else:
            visible_vertical[i, :] = np.logical_and(forest[i, :] == forest_vertical[i, :],
                                                    forest_vertical[i, :] != forest_vertical[i + k * 1, :])
    visible_trees = np.logical_or(visible_trees, visible_vertical)

print(visible_trees.sum())

all_trees = np.transpose(np.ones(forest.shape).nonzero())
tree_score = [np.zeros(forest.shape).astype(int) for _ in range(4)]

# part 2
for tree in all_trees:
    original_tree_height = forest[tuple(tree)]
    original_tree_tuple = tuple(tree)
    for i, k in enumerate(((1, 0), (-1, 0), (0, 1), (0, -1))):
        this_tree_as_tuple = tuple(tree)
        this_tree = tree
        while True:
            next_tree = this_tree + k
            next_tree_as_tuple = tuple(next_tree)
            if not (0 <= next_tree_as_tuple[0] <= size - 1 and 0 <= next_tree_as_tuple[1] <= size - 1):
                break
            next_tree_height = forest[next_tree_as_tuple]
            tree_score[i][original_tree_tuple] += 1
            if next_tree_height >= original_tree_height:
                break
            this_tree = next_tree

r1 = reduce(np.multiply, tree_score)
print(np.max(r1))
