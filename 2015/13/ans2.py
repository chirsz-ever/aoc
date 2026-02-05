#!/usr/bin/env python3

import sys
from itertools import permutations


def main() -> None:
    inputFile = sys.argv[1]

    happiness: dict[tuple[str, str], int] = {}
    homoj: set[str] = set()
    with open(inputFile) as fin:
        for l in fin:
            l = l.strip()
            if not l:
                continue
            segs = l.split()
            a = segs[0]
            b = segs[-1][:-1]
            v = int(segs[3]) * (-1 if segs[2] == "lose" else 1)
            happiness[a, b] = v
            homoj.add(a)
            homoj.add(b)
    # print(happiness)

    assert 'Mi' not in homoj
    for p in homoj:
        happiness[p, 'Mi'] = 0
        happiness['Mi', p] = 0
    homoj.add('Mi')

    max_change = 0
    for p in permutations(homoj, len(homoj)):
        change = sum(happiness[p[i], p[(i + 1) % len(p)]] + happiness[p[i], p[(i - 1) % len(p)]] for i in range(len(p)))
        if change > max_change:
            max_change = change
    print(max_change)


if __name__ == "__main__":
    main()
