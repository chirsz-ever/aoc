#!/usr/bin/env python3

import sys
from queue import PriorityQueue, Queue
from collections import defaultdict

def getArg(n, default):
    if len(sys.argv) >= n + 1:
        return sys.argv[n]
    return default

inputFile = getArg(1, 'input')
# print(f'{inputFile = }')

riskMap: list[list[int]] = []
with open(inputFile) as fin:
    for line in fin:
        riskMap.append(list(int(c) for c in line.strip()))

width = len(riskMap[0])
height = len(riskMap)

W = width * 5
H = height * 5

Pos = tuple[int, int]

def getRisk(p: Pos) -> int:
    pi = p[0] % height
    pj = p[1] % width
    inc = p[0] // height + p[1] // width
    return (riskMap[pi][pj] + inc - 1) % 9 + 1

def Adj(p: Pos) -> list[Pos]:
    pi, pj = p
    adjs = []
    for di, dj in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        if 0 <= pi + di < H  and 0 <= pj +dj < W:
            adjs.append((pi + di, pj + dj))
    return adjs


def Dijkstra(src: Pos, dst: Pos):
    minRisk: dict[Pos, int] = defaultdict(lambda: 2**63)
    minRisk[src] = 0
    # minRiskFrom: dict[Pos, Pos] = dict()
    Q: Queue[tuple[int, Pos]] = PriorityQueue()
    Q.put((0, src))
    S: set[Pos] = set()
    while dst not in S:
        _, u = Q.get()
        S.add(u)
        for v in Adj(u):
            vRiskFromU  = minRisk[u] + getRisk(v)
            if vRiskFromU < minRisk[v]:
                minRisk[v] = vRiskFromU
                # print(f'minRisk tp {v} in from {u}')
                # minRiskFrom[v] = u
                Q.put((vRiskFromU, v))
    return minRisk[dst]

minRisk = Dijkstra((0, 0), (H - 1, W - 1))

print(f'{minRisk = }')

