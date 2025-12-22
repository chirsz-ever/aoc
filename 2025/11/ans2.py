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
    def stat_path(src: str, dst: str, target: str) -> int:
        if target == src:
            return 1
        return sum(stat_path(src, dst, p) for p in reverse_graph.get(target, []))

    stat_pathes = lambda src, dst: stat_path(src, dst, dst)

    paths_mid = stat_pathes('fft', 'dac')
    # print(f'{paths_mid=}')
    if paths_mid > 0:
        paths_start = stat_pathes('svr', 'fft')
        paths_end = stat_pathes('dac', 'out')
        assert paths_start > 0
        assert paths_end > 0
    else:
        paths_mid = stat_pathes('dac', 'fft')
        assert paths_mid > 0
        paths_start = stat_pathes('svr', 'dac')
        paths_end = stat_pathes('fft', 'out')
        assert paths_start > 0
        assert paths_end > 0

    # print(f'{paths_start=}')
    # print(f'{paths_mid=}')
    # print(f'{paths_end=}')
    pathes = paths_start * paths_mid * paths_end
    print(f'{pathes=}')

if __name__ == '__main__':
    main()
