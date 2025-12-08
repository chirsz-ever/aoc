#!/usr/bin/env python3

import sys

def show_diagram(diag: list[str]):
    for l in diag:
        print(l)

def main() -> None:
    inputFile = 'input'
    if len(sys.argv) >= 2:
        inputFile = sys.argv[1]

    diag: list[str] = []
    with open(inputFile) as fin:
        for l in fin:
            l = l.removesuffix('\n')
            if len(l) > 0:
                diag.append(l)

    j0 = diag[0].index('S')
    tbs = set([(0, j0)])
    timelines: dict[tuple[int, int], int] = {}
    timelines[(0, j0)] = 1
    for _ in range(1, len(diag)):
        new_tbs: set[tuple[int, int]] = set()
        for i, j in tbs:
            if diag[i + 1][j] == '.':
                p = (i + 1, j)
                new_tbs.add(p)
                timelines[p] = timelines.get(p, 0) + timelines[i, j]
            else:
                assert diag[i + 1][j] == '^'
                p0 = (i, j)
                p1 = (i + 1, j - 1)
                p2 = (i + 1, j + 1)
                new_tbs.add(p1)
                new_tbs.add(p2)
                timelines[p1] = timelines.get(p1, 0) + timelines[p0]
                timelines[p2] = timelines.get(p2, 0) + timelines[p0]
        tbs = new_tbs

    # show_diagram(diag)
    # print(f'{scnt=}')
    s = sum(cnt for (i, j), cnt in timelines.items() if i == len(diag) - 1)
    # print(f'{timelines=}')
    print(f'{s=}')

if __name__ == '__main__':
    main()
