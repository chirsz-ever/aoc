#!/usr/bin/env python3

import sys
from functools import cmp_to_key

inputFile = 'input'
if len(sys.argv) >= 2:
    inputFile = sys.argv[1]

def read_input(fname):
    inputs = []
    with open(fname) as fin:
        left = None
        right = None
        for l in fin:
            # print(f"{l=}")
            # print(f"{left=}")
            # print(f"{right=}")
            l = l.strip()
            if len(l) == 0:
                continue
            if left == None:
                left = eval(l)
                continue
            if right == None:
                right = eval(l)
            inputs.append((left, right))
            left, right = None, None
    return inputs

def compare(left, right) -> int:
    if isinstance(left, int) and isinstance(right, int):
        return left - right
    elif isinstance(left, list) and isinstance(right, list):
        for l, r in zip(left, right):
            c = compare(l, r)
            if c != 0:
                return c
        return len(left) - len(right)
    elif isinstance(left, int) and isinstance(right, list):
        return compare([left], right)
    elif isinstance(left, list) and isinstance(right, int):
        return compare(left, [right])
    else:
        raise RuntimeError(f"try compare {left} and {right}")

inputs = read_input(inputFile)
# print(inputs)
# print(len(inputs))

allpackets: list = []
s = 0
for i, pair in enumerate(inputs):
    c = compare(*pair)
    # print(f"index {i + 1}: {c}: {pair[0]} vs {pair[1]}")
    if c < 0:
        s += i + 1
    allpackets.append(pair[0])
    allpackets.append(pair[1])
print(s)

allpackets.append([[2]])
allpackets.append([[6]])

allpackets.sort(key=cmp_to_key(compare))

# for p in allpackets:
#     print(p)

i1 = allpackets.index([[2]]) + 1
i2 = allpackets.index([[6]]) + 1
print(i1 * i2)
