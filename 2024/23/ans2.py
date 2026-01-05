#!/usr/bin/env python3

import sys

def main() -> None:
    inputFile = sys.argv[1]

    nmap: dict[str, set[str]] = {}
    with open(inputFile) as fin:
        for l in fin:
            l = l.strip()
            f, t = l.split('-')
            nmap.setdefault(f, set()).add(t)
            nmap.setdefault(t, set()).add(f)

    max_cliques: list[set[str]] = []

    # from https://en.wikipedia.org/wiki/Bron%E2%80%93Kerbosch_algorithm
    def BronKerbosch1(R: set[str], P: set[str], X: set[str]):
        if len(P) == 0 and len(X) == 0:
            max_cliques.append(R)
            return
        for v in P.copy():
            BronKerbosch1(R.union({v}), P.intersection(nmap[v]), X.intersection(nmap[v]))
            P.remove(v)
            X.add(v)

    BronKerbosch1(set(), set(nmap.keys()), set())

    # print(sorted(map(len, max_cliques)))
    mclique = max(max_cliques, key=len)
    print(','.join(sorted(mclique)))

if __name__ == '__main__':
    main()
