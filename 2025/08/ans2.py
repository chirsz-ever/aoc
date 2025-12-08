#!/usr/bin/env python3

import sys

def distance2(p0, p1):
    x0, y0, z0 = p0
    x1, y1, z1 = p1
    return (x0 - x1)**2 + (y0 - y1)**2 + (z0 - z1)**2

def main() -> None:
    inputFile = 'input'
    if len(sys.argv) >= 2:
        inputFile = sys.argv[1]

    jbs: list[tuple[int, int, int]] = []
    with open(inputFile) as fin:
        for l in fin:
            l = l.removesuffix('\n')
            if len(l) > 0:
                x, y, z = map(int, l.split(','))
                jbs.append((x, y, z))
                
    sorted_circuit_pairs = [(i, j) for i in range(0, len(jbs) - 1) for j in range(i + 1, len(jbs))]
    sorted_circuit_pairs.sort(key = lambda p: distance2(jbs[p[0]], jbs[p[1]]))

    circuits: list[set[int]] = [set([b]) for b in range(0, len(jbs))]

    i = -1
    while True:
        i += 1
        # connect the two junction boxes which are closest together but aren't already directly connected
        b0, b1 = sorted_circuit_pairs[i]
        # print(f'{b0=} {b1=}')
        ci0 = ci1 = 0
        c0 = c1 = circuits[0]
        for ci, c in enumerate(circuits):
            if b0 in c:
                c0 = c
                ci0 = ci
                break
        for ci, c in enumerate(circuits):
            if b1 in c:
                c1 = c
                ci1 = ci
                break
        
        if c0 == c1:
            continue
        if ci0 > ci1:
            ci0, ci1 = ci1, ci0
            c0, c1 = c1, c0
        circuits[ci0] = c0.union(c1)
        del circuits[ci1]
        if len(circuits) == 1:
            print(jbs[b0][0] * jbs[b1][0])
            break

if __name__ == '__main__':
    main()
