#!/usr/bin/env python3

import sys
from itertools import permutations, combinations


def main() -> None:
    inputFile = sys.argv[1]

    G: dict[tuple[str, str], int] = {}
    cities: set[str] = set()
    with open(inputFile) as fin:
        for l in fin:
            l = l.strip()
            if not l:
                continue
            a, _, b, _, dist = l.split()
            G[a, b] = int(dist)
            G[b, a] = int(dist)
            cities.add(a)
            cities.add(b)
    for a, b in permutations(cities, 2):
        if (a, b) not in G:
            print(f'{(a, b)} not in G!')
            return

    def dfs(c: str, aval: set[str], t: str) -> int:
        if not aval:
            return G[c, t]
        return max(G[c, x] + dfs(x, aval.copy().difference([x]), t) for x in aval)

    min_dist = max(dfs(a, cities.copy().difference([a, b]), b) for a, b in combinations(cities, 2))
    print(min_dist)

if __name__ == "__main__":
    main()
