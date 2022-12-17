#!/usr/bin/env python3

import sys

inputFile = 'input'
if len(sys.argv) >= 2:
    inputFile = sys.argv[1]

instructions = []

with open(inputFile) as fin:
    for l in fin:
        l = l.strip()
        if len(l) == 0:
            continue
        d, n_ = l.split()
        instructions.append((d, int(n_)))

# print(instructions)

inst2motion = {'L': (-1, 0), 'R': (1, 0), 'U': (0, 1), 'D': (0, -1)}

rope = [(0, 0) for _ in range(10)]

tail_coords = { rope[-1] }

def is_neighbor(c1, c2) -> bool:
    x1, y1 = c1
    x2, y2 = c2
    return -1 <= x1 - x2 <= 1 and -1 <= y1 - y2 <= 1 

def sign(x):
    if x < 0:
        return -1
    elif x == 0:
        return 0
    else:
        return 1

def calc_knot(k, k0):
    x, y = k
    x0, y0 = k0
    dx = x - x0
    dy = y - y0
    assert abs(dx) > 1 or abs(dy) > 1
    if abs(dx) > abs(dy):
        rcoord = (sign(dx), 0)
    elif abs(dy) > abs(dx):
        rcoord = (0, sign(dy))
    else:
        rcoord = (sign(dx), sign(dy)) 
    return (x0 + rcoord[0], y0 + rcoord[1])

def step(dx, dy):
    global rope
    rope[0] = (rope[0][0] + dx, rope[0][1] + dy)
    for i in range(1, 10):
        if not is_neighbor(rope[i - 1], rope[i]):
            rope[i] = calc_knot(rope[i], rope[i - 1])
        else:
            break


def print_map(l, r, u, d):
    for y in range(u, d - 1, -1):
        for x in range(l, r + 1):
            if (x, y) in rope:
                for i, c in enumerate(rope):
                    if c == (x, y):
                        if i == 0:
                            print('H', end='')
                        else:
                            print(i, end='')
                        break;
            elif (x, y) == (0, 0):
                print('s', end='')
            elif (x, y) in tail_coords:
                print('#', end='')
            else:
                print('.', end='')
        print()

for d, n in instructions:
    dx, dy = inst2motion[d]
    for _ in range(n):
        step(dx, dy)
        tail_coords.add(rope[-1])
        # print_map(0, 5, 4, 0)
    # print_map(-11, 14, 15, -5)
    # input()

# print_map(-11, 14, 15, -5)

print(len(tail_coords))

