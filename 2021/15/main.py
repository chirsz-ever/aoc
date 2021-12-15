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

Pos = tuple[int, int]

def getRisk(p: Pos) -> int:
    return riskMap[p[0]][p[1]]

def Adj(p: Pos) -> list[Pos]:
    pi, pj = p
    adjs = []
    for di, dj in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        if 0 <= pi + di < height and 0 <= pj +dj < width:
            adjs.append((pi + di, pj + dj))
    return adjs


def Dijkstra(src: Pos, dst: Pos):
    minRisk: dict[Pos, int] = defaultdict(lambda: 2**63)
    minRisk[src] = 0
    minRiskFrom: dict[Pos, Pos] = dict()
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
                minRiskFrom[v] = u
                Q.put((vRiskFromU, v))
    return minRisk[dst], minRiskFrom

minRisk, minRiskFrom = Dijkstra((0, 0), (height - 1, width - 1))

print(f'{minRisk = }')

