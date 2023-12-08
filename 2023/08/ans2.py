#!/usr/bin/env python3

import sys
from collections import Counter
from itertools import cycle
from functools import reduce
from math import lcm

inputFile = 'input'
if len(sys.argv) >= 2:
    inputFile = sys.argv[1]

insts: str = ''
node_map: dict[str, tuple[str, str]] = {}
with open(inputFile) as fin:
    for l in fin:
        l = l.strip()
        if len(l) == 0:
            continue
        if len(insts) == 0:
            insts = l
        else:
            src, tgts = l.split(' = ')
            t_l, t_r = tgts.strip()[1:-1].split(', ')
            node_map[src] = (t_l, t_r)

# print(f'{insts=}')
# print(f'{node_map=}')

# return: steps before enter loop, loop size, Z in loop
def get_stat(sn: str) -> tuple[int, int, list[int]]:
    histroy: list[tuple[str, int]] = []
    histroy_set: set[tuple[str, int]] = set()
    n = sn
    for i, inst in cycle(enumerate(insts)):
        h_unit = (n, i)
        if h_unit in histroy_set:
            loop_start = histroy.index(h_unit)
            loop_size = len(histroy) - loop_start
            # print(f'{n=} {histroy=} {loop_start=} {loop_size=}')
            zs = []
            for k in range(0, loop_size):
                if histroy[loop_start + k][0][-1] == 'Z':
                    zs.append(k)
            assert any(x[0][-1] == 'Z' for x in histroy)
            # print(f'{len(zs)=}')
            return loop_start, loop_size, zs

        histroy.append(h_unit)
        histroy_set.add(h_unit)
        n = node_map[n][0 if inst == 'L' else 1]

    raise RuntimeError()

start_nodes = [n for n in node_map.keys() if n[-1] == 'A']
sn_stats = list(map(get_stat, start_nodes))

# N = loop_start_i + z_offset_i (mod loop_size)

# result = chinese_remainder([(l_start + z_offset[-1], l_size) for l_start, l_size, z_offset in sn_stats])

# we can find that loop_start + z_offset == loop_size

loop_sizes = [t[1] for t in sn_stats]

print(f'{loop_sizes=}')

result = reduce(lcm, loop_sizes)

print(f'{result=}')
