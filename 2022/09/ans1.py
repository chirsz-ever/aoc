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
        d, n = l.split()
        instructions.append((d, int(n)))

# print(instructions)

inst2motion = {'L': (-1, 0), 'R': (1, 0), 'U': (0, 1), 'D': (0, -1)}

head = (0, 0)
tail = (0, 0)

tail_coords = { tail }

def is_neighbor(c1, c2) -> bool:
    x1, y1 = c1
    x2, y2 = c2
    return -1 <= x1 - x2 <= 1 and -1 <= y1 - y2 <= 1 


def step(dx, dy):
    global head, tail
    new_head = (head[0] + dx, head[1] + dy)
    if not is_neighbor(new_head, tail):
        tail = head
    head = new_head


for d, n in instructions:
    dx, dy = inst2motion[d]
    for _ in range(n):
        step(dx, dy)
        tail_coords.add(tail)

print(len(tail_coords))

