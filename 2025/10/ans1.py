#!/usr/bin/env python3

import sys

def main() -> None:
    inputFile = 'input'
    if len(sys.argv) >= 2:
        inputFile = sys.argv[1]

    diagrams: list[str] = []
    schematics: list[list[list[int]]] = []
    joltages: list[list[int]] = []
    with open(inputFile) as fin:
        for l in fin:
            diag = ''
            schs = []
            jolt = []
            for seg in l.strip().split():
                if seg[0] == '[':
                    diag = seg[1:-1]
                elif seg[0] == '(':
                    schs.append([int(x) for x in seg[1:-1].split(',')])
                elif seg[0] == '{':
                    jolt = [int(x) for x in seg[1:-1].split(',')]
            diagrams.append(diag)
            schematics.append(schs)
            joltages.append(jolt)
    
    # print(f'{diagrams=}')
    # print(f'{schematics=}')
    # print(f'{joltages=}')
    
    # 0-1 bag problem
    s = 0
    for i in range(len(diagrams)):
        diag = diagrams[i]
        schs = schematics[i]
        for n in range(1, len(schs) + 1):
            # print(f'searching {i} {n}')
            if has_answer(diag, schs, n):
                s += n
                # print(f'{i}: {n}')
                break
        else:
            raise RuntimeError(f'not found answer {i}')
    print(f's = {s}')

M = '.#'

def is_match(diag: str, schs: list[list[int]], choose: list[int]) -> bool:
    d = [0] * len(diag)
    for i in range(len(schs)):
        if choose[i]:
            s = schs[i]
            for l in s:
                d[l] = 1-d[l]

    result = all(M[dd] == ll for ll, dd in zip(diag, d))
    # print(f'check {choose}: {result}, {d}')
    return result

def has_answer(diag: str, schs: list[list[int]], n: int) -> bool:
    size = len(schs)
    choose = [0] * size
    def step(i, avail, c):
        if i > 0:
            choose[i - 1] = c
        if i == size:
            return is_match(diag, schs, choose)
        assert i < size
        assert i + avail <= size
        if i + avail == size:
            return step(i + 1, avail - 1, 1)
        elif avail == 0:
            return step(i + 1, avail, 0)
        return step(i + 1, avail - 1, 1) or step(i + 1, avail, 0)
    return step(0, n, 0)

if __name__ == '__main__':
    main()
