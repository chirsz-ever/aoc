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

    tbs = set([(0, diag[0].index('S'))])
    scnt = 0
    for _ in range(1, len(diag)):
        new_tbs: set[tuple[int, int]] = set()
        for i, j in tbs:
            if diag[i + 1][j] == '.':
                new_tbs.add((i + 1, j))
            else:
                assert diag[i + 1][j] == '^'
                scnt += 1
                new_tbs.add((i + 1, j - 1))
                new_tbs.add((i + 1, j + 1))
        tbs = new_tbs

    # show_diagram(diag)
    print(f'{scnt=}')

if __name__ == '__main__':
    main()
