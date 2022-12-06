import collections
from itertools import islice

with open('input.txt') as f:
    datastream = f.read().strip()


def sliding_window(iterable, n):
    # sliding_window('ABCDEFG', 4) --> ABCD BCDE CDEF DEFG
    it = iter(iterable)
    window = collections.deque(islice(it, n), maxlen=n)
    if len(window) == n:
        yield tuple(window)
    for x in it:
        window.append(x)
        yield tuple(window)


SEQUENCE_LENGTH_PART1 = 4


def check_for_duplicate_chars(input_string):
    observed_chars = set()
    for char_ in input_string:
        if char_ in observed_chars:
            return True
        else:
            observed_chars.add(char_)
    return False


def find_start_index(datastream_input, sequence_length):
    for i, window in enumerate(sliding_window(datastream_input, sequence_length)):
        if not check_for_duplicate_chars(window):
            return i + sequence_length


# part1
print(find_start_index(datastream, SEQUENCE_LENGTH_PART1))

# part2
SEQUENCE_LENGTH_PART2 = 14
print(find_start_index(datastream, SEQUENCE_LENGTH_PART2))
