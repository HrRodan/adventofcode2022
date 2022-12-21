from copy import deepcopy

from utilities import sliding_window

with open('input.txt') as f:
    MESSAGE = {i: int(x.strip()) for i, x in enumerate(f.readlines())}

ALL_KEYS = list(MESSAGE.keys())
LEN_KEYS = len(ALL_KEYS)

message_dict_start = {this: [prev, next_] for prev, this, next_ in
                      sliding_window([ALL_KEYS[-1]] + ALL_KEYS + [ALL_KEYS[0]], 3)}


def find_next_value(this_value: int, m: dict, message_original):
    next_value = this_value
    message_value = message_original[this_value]
    loop_length_base = abs(message_value) % (LEN_KEYS - 1)
    if message_value < 0:
        for _ in range(loop_length_base + 1):
            next_value, _ = m[next_value]
    else:
        for _ in range(loop_length_base):
            _, next_value = m[next_value]
    return next_value


def mix_message(message_start: dict, message_original=MESSAGE, repeat=1):
    message_dict = deepcopy(message_start)
    for _ in range(repeat):
        for value in ALL_KEYS:
            if message_original[value] == 0:
                continue
            prev, next_ = message_dict[value]
            move_after = find_next_value(value, message_dict, message_original)
            if move_after == prev:
                continue
            _, next_moved = message_dict[move_after]
            message_dict[prev][1] = next_
            message_dict[next_][0] = prev
            message_dict[move_after][1] = value
            message_dict[next_moved][0] = value
            message_dict[value] = [move_after, next_moved]

    return message_dict


def get_list_from_dict(m: dict, message_original=MESSAGE):
    start_value = next(i for i, x in message_original.items() if x == 0)
    message_list_ = [0]
    value_ = start_value
    while True:
        _, value_ = m[value_]
        if value_ == start_value:
            break
        message_list_.append(message_original[value_])

    return message_list_


message_list = get_list_from_dict(mix_message(message_dict_start))
r1 = sum(message_list[x % len(message_list)] for x in range(1000, 3001, 1000))
print(r1)

# Part 2

decryption_key = 811589153
MESSAGE_PART2 = {k: v * decryption_key for k, v in MESSAGE.items()}
message_list_part2 = get_list_from_dict(mix_message(message_dict_start, message_original=MESSAGE_PART2, repeat=10),
                                        message_original=MESSAGE_PART2)
r2 = sum(message_list_part2[x % len(message_list_part2)] for x in range(1000, 3001, 1000))
print(r2)
