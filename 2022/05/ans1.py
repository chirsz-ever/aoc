#!/usr/bin/env python3

import sys
import re

inputFile = 'input'
if len(sys.argv) >= 2:
    inputFile = sys.argv[1]

reInst = re.compile(r'move (\d+) from (\d+) to (\d+)')

stacksInit: list[list[str]] = []
insts: list[tuple[int, int, int]] = []
with open(inputFile) as fin:
    beginInst = False
    for l in fin:
        if not beginInst:
            if l.strip() == "":
                beginInst = True
                continue
            if l[1].isdigit():
                continue
            for i, c in enumerate(l[1::4]):
                while len(stacksInit) <= i:
                    stacksInit.append([])
                if not c.isspace():
                    stacksInit[i].append(c)
        else:
            m = reInst.match(l)
            assert m
            insts.append((int(m[1]), int(m[2]), int(m[3])))

for stk in stacksInit:
    stk.reverse()

def copyStacks(stks: list[list[str]]):
    return [[x for x in l] for l in stks]

def step1(stks: list[list[str]], inst: tuple[int, int, int]):
    size, from_, to = inst
    from_ -= 1
    to -= 1
    assert size <= len(stks[from_])
    for _ in range(size):
        stks[to].append(stks[from_].pop())

def step2(stks: list[list[str]], inst: tuple[int, int, int]):
    size, from_, to = inst
    from_ -= 1
    to -= 1
    assert size <= len(stks[from_])
    stks[to].extend(stks[from_][-size:])
    del stks[from_][-size:]

# print(stacksInit)
# print(insts)

stks1 = copyStacks(stacksInit)

for inst in insts:
    step1(stks1, inst)

# print(stks1)
print(''.join(stk[-1] for stk in stks1))


stks2 = copyStacks(stacksInit)

for inst in insts:
    step2(stks2, inst)

# print(stks2)
print(''.join(stk[-1] for stk in stks2))
