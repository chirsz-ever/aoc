#!/usr/bin/env python3

import sys
from itertools import takewhile
from typing import Iterable

inputFile = 'input'
if len(sys.argv) >= 2:
    inputFile = sys.argv[1]

entries : list[tuple[list[set[str]], list[str]]] = []
with open(inputFile) as fin:
    for line in fin:
        unique = []
        output = []
        beforeSplit = True
        for w in line.split():
            if beforeSplit:
                if w == '|':
                    beforeSplit = False
                else:
                    unique.append(set(w))
            else:
                output.append(w)
        entries.append((unique, output))

NSMAP: dict[int, set[str]] = {
    0: set("abcefg"),
    1: set("cf"),
    2: set("acdeg"),
    3: set("acdfg"),
    4: set("bcdf"),
    5: set("abdfg"),
    6: set("abdefg"),
    7: set("acf"),
    8: set("abcdefg"),
    9: set("abcdfg"),
}

allSeg = lambda: {chr(c) for c in range(ord('a'), ord('g') + 1)}

def update(wsMap: dict[str, set[str]], w: str, constrain: Iterable[str]):
    if w not in wsMap:
        wsMap[w] = allSeg()
    wsMap[w].intersection_update(constrain)
    if len(wsMap[w]) == 1:
        for w1 in wsMap.keys():
            if w1 != w:
                wsMap[w1].difference_update(wsMap[w])

def deduce(history: list[set[str]]) -> dict[tuple[str, ...], int]:
    wsMap: dict[str, set[str]] = {}
    nMap: dict[int, set[str]] = {}
    lens = [len(s) for s in NSMAP.values()]
    for h in history:
        lenh = len(h)
        if lens.count(lenh) == 1:
            n = sum(n for n, segs in NSMAP.items() if len(segs) == lenh)
            nMap[n] = h
            for wire in h:
                update(wsMap, wire, NSMAP[n])

    # dirty hack
    for wires in history:
        if len(wires) == 5 and wires.issuperset(nMap[1]):
            for w in wires - nMap[1]:
                update(wsMap, w, "adg")
            nMap[3] = wires
        elif len(wires) == 6 and wires.issuperset(nMap[4]):
            for w in wires - nMap[4]:
                update(wsMap, w, "ag")
            nMap[9] = wires
        elif len(wires) == 6 and wires.issuperset(nMap[1]):
            for w in wires - nMap[1]:
                update(wsMap, w, "abeg")
            nMap[0] = wires
        elif len(wires) == 6:
            c = (allSeg() - wires).pop()
            update(wsMap, c, 'c')

    while any(len(segs) > 1 for segs in wsMap.values()):
        for n1, wires1 in nMap.items():
            for n2, wires2 in nMap.items():
                for w in wires1 - wires2:
                    update(wsMap, w, (NSMAP[n1] - NSMAP[n2]))
                for w in wires1 & wires2:
                    update(wsMap, w, (NSMAP[n1] & NSMAP[n2]))
    swMap = {list(s)[0]: w for w, s in wsMap.items()}
    return {tuple(sorted(swMap[s] for s in segs)): n for n, segs in NSMAP.items()}

numbers: list[int] = []
for segs, encoded in entries:
    wnMap = deduce(segs)
    lineOutput = ''.join(str(wnMap[tuple(sorted(ws))]) for ws in encoded)
    # print(f"{lineOutput}")
    numbers.append(int(lineOutput))

print(f"{sum(numbers) = }")
