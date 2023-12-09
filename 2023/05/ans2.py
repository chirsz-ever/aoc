#!/usr/bin/env python3

import sys
import re
from typing import Optional

inputFile = 'input'
if len(sys.argv) >= 2:
    inputFile = sys.argv[1]

# destination, source, range
ConvertRule = tuple[int, int, int]
# start, length
Range = tuple[int, int]

seeds: list[int] = []
maps: list[list[ConvertRule]] = []
with open(inputFile) as fin:
    for l in fin:
        l = l.strip()
        if len(l) == 0:
            continue
        words = l.split()
        if words[0] == 'seeds:':
            seeds = [int(w) for w in words[1:]]
        elif words[-1] == 'map:':
            maps.append([])
        else:
            r = tuple(int(w) for w in words)
            assert len(r) == 3
            maps[-1].append(r)

seed_ranges: list[Range] = [ (x, y) for x, y in zip(seeds[::2], seeds[1::2]) ]

# print(f'{seed_ranges=}')
# print(f'{maps=}')

# return unmapped, mapped
def apply_covert_rule(r: Range, cr: ConvertRule) -> tuple[list[Range], list[Range]]:
    r_start, r_length = r
    c_dst, c_src_start, c_length = cr
    r_stop = r_start + r_length - 1
    c_src_stop = c_src_start + c_length - 1
    if r_stop < c_src_start or r_start > c_src_stop:
        return ([r], [])
    unmapped = []
    if r_start < c_src_start:
        unmapped.append((r_start, c_src_start - r_start))
    if r_stop > c_src_stop:
        unmapped.append((c_src_stop + 1, r_stop - c_src_stop))
    mapped_start = max(r_start, c_src_start)
    mapped_stop = min(r_stop, c_src_stop)
    mapped_length = mapped_stop - mapped_start + 1
    mapped_dst_start = mapped_start - c_src_start + c_dst
    return (unmapped, [(mapped_dst_start, mapped_length)])

# return unmapped, mapped
def map_single_range(unmapped: list[Range], cr: ConvertRule) -> tuple[list[Range], list[Range]]:
    new_unmapped: list[Range] = []
    mapped: list[Range] = []
    for r in unmapped:
        u, m = apply_covert_rule(r, cr)
        new_unmapped.extend(u)
        mapped.extend(m)
    return new_unmapped, mapped

def map_ranges_once(rs: list[Range], rules: list[ConvertRule]) -> list[Range]:
    ts: list[Range] = []
    for rng in rs:
        unmapped = [rng]
        for rl in rules:
            # assumes all rules not overlap
            unmapped, mapped = map_single_range(unmapped, rl)
            ts.extend(mapped)
        ts.extend(unmapped)
    return ts

def map_seed_ranges(rs: list[Range]) -> list[Range]:
    t = rs
    # print('----------')
    # print(rs)
    for m in maps:
        nxt = map_ranges_once(t, m)
        # print(f' -> {nxt}')
        t = nxt
    return t

min_location = None
for sr in seed_ranges:
    final_seed_ranges = map_seed_ranges([sr])
    final_seed_ranges.sort()
    if min_location is not None:
        min_location = min(min_location, final_seed_ranges[0][0])
    else:
        min_location = final_seed_ranges[0][0]

print(f'{min_location=}')
