#!/usr/bin/env python3

import sys

inputFile = 'input'
if len(sys.argv) >= 2:
    inputFile = sys.argv[1]

steps = []
boards = []
marks = []
with open(inputFile) as fin:
    steps = [int(w) for w in fin.readline().strip().split(',')]
    row = 0
    brd = []
    for line in (l.strip() for l in fin if len(l.strip()) != 0):
        row += 1
        brd.append([int(w) for w in line.split()])
        if row == 5:
            boards.append(brd)
            marks.append([[0 for _ in range(5)] for _ in range(5)])
            row = 0
            brd = []

# print(f'{steps = }')
# print(f'{boards = }')

def doMark(mark: list[list[int]], brd: list[list[int]], t: int):
    for i in range(len(brd)):
        for j in range(len(brd[i])):
            if brd[i][j] == t:
                mark[i][j] += 1

def isBingo(mark: list[list[int]], brd: list[list[int]]) -> list[int]:
    for i in range(len(mark)):
        if all(mark[i][j] != 0 for j in range(len(mark[i]))):
            return [brd[i][j] for j in range(len(brd[i]))]
    for j in range(len(mark[0])):
        if all(mark[i][j] != 0 for i in range(len(mark))):
            return [brd[i][j] for i in range(len(brd))]

winBoards = set()
for t in steps:
    for b in range(len(boards)):
        brd = boards[b]
        mrk = marks[b]
        doMark(mrk, brd, t)
        if bs := isBingo(mrk, brd):
            winBoards.add(b)
            if len(winBoards) == len(boards):
                r = sum(brd[i][j] for i in range(len(brd)) for j in range(len(brd[i])) if mrk[i][j] == 0) * t
                print(f'{winBoards = }')
                print(f'{t = }')
                print(f'{bs = }')
                print(f'{r = }')
                exit()
