#!/usr/bin/env python3

from argparse import ArgumentParser
from collections import deque

def parse_args() -> str:
    parser = ArgumentParser()
    parser.add_argument('input', default='input', nargs='?')
    n = parser.parse_args()
    return n.input

def read_input(fname) -> list[int]:
    with open(fname) as fin:
        return [int(l.rstrip()) for l in fin if len(l.rstrip()) != 0]

def find_origin_nth(ms: list[tuple[int, int]], n: int) -> tuple[int, int]:
    for k in range(len(ms)):
        if ms[k][0] == n:
            return k, ms[k][1]
    raise RuntimeError()

def do_move(ms: list, k: int, n: int):
    l = len(ms)
    i = (k + n) % (l - 1)
    t = ms[k]
    del ms[k]
    ms.insert(i, t)
    # print(f"{t[1]} moves")

def get_result(ms: list[tuple[int, int]]) -> int:
    i = 0
    l = len(ms)
    while i < len(ms):
        if ms[i][1] == 0:
            break
        i += 1
    assert ms[i][1] == 0
    i1000 = ms[(i + 1000) % l][1]
    i2000 = ms[(i + 2000) % l][1]
    i3000 = ms[(i + 3000) % l][1]
    # print(f"{i1000=}, {i2000=}, {i3000=}")
    return i1000 + i2000 + i3000


def main() -> None:
    inputFile = parse_args()
    ns = read_input(inputFile)
    ms: list[tuple[int, int]] = list(enumerate(ns))
    for i in range(len(ns)):
        k, n = find_origin_nth(ms, i)
        do_move(ms, k, n)
        # print([m[1] for m in ms])
    # print([m[1] for m in ms])
    result = get_result(ms)
    print(result)

if __name__ == '__main__':
    main()
