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

    triples: set[tuple[str, str, str]] = set()
    for c1 in nmap.keys():
        for c2 in nmap[c1]:
            for c3 in nmap[c1].intersection(nmap[c2]):
                triples.add(tuple(sorted([c1, c2, c3]))) # type: ignore
    count = sum(int(any(c.startswith('t') for c in t)) for t in triples)
    print(count)

if __name__ == '__main__':
    main()
