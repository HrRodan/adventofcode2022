import numpy as np

with open('input_test.txt') as f:
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

forest_padded = np.pad(forest, pad_width=((0,0), forest.shape), mode='constant', constant_values=99)
count_visible_trees = np.zeros(forest_padded.shape).astype(np.byte)

for k in (-1,1):
    found_max = np.full(forest_padded.shape, fill_value=-1).astype(np.byte)
    done_trees = np.full(forest_padded.shape, fill_value=False)
    for i in range(1, size):
        forest_padded_rolled = np.roll(forest_padded, k*i, axis=1)
        found_max = np.maximum(found_max, forest_padded_rolled)
        count_visible_trees_previous = count_visible_trees.copy()
        count_visible_trees = np.where(found_max < forest_padded,count_visible_trees + 1, count_visible_trees)

