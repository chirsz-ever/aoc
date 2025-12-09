#!/usr/bin/env python3

import sys

def main() -> None:
    inputFile = 'input'
    if len(sys.argv) >= 2:
        inputFile = sys.argv[1]

    coords: list[tuple[int, int]] = []
    with open(inputFile) as fin:
        for l in fin:
            l = l.removesuffix('\n')
            x, y = map(int, l.split(','))
            coords.append((x, y))
    
    def area(i, j):
        x0, y0 = coords[i]
        x1, y1 = coords[j]
        return (abs(x0 - x1) + 1) * (abs(y1 - y0) + 1)

    m = area(0, 1)
    mi, mj = 0, 1
    for i in range(len(coords)):
        for j in range(i + 1, len(coords)):
            a = area(i, j)
            if a > m:
                mi, mj, m = i, j, a
    print(coords[mi])
    print(coords[mj])
    print(m)

if __name__ == '__main__':
    main()
