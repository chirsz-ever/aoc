#!/usr/bin/env python3

import sys
from functools import lru_cache

def main() -> None:
    inputFile = 'input'
    if len(sys.argv) >= 2:
        inputFile = sys.argv[1]

    graph: dict[str, set[str]] = {}
    with open(inputFile) as fin:
        for l in fin:
            segs = l.strip().split()
            if len(segs) == 0:
                continue
            key = segs[0][:-1]
            dsts = set(segs[1:])
            graph[key] = dsts

    reverse_graph: dict[str, set[str]] = {}
    for src, dsts in graph.items():
        for dst in dsts:
            reverse_graph.setdefault(dst, set())
            reverse_graph[dst].add(src)
    # print(f'{reverse_graph=}')

    @lru_cache
    def stat_path(node: str) -> int:
        if node == 'you':
            return 1
        return sum(stat_path(p) for p in reverse_graph.get(node, []))
    
    paths = stat_path('out')
    print(f'{paths=}')

if __name__ == '__main__':
    main()
