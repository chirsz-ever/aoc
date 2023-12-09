#!/usr/bin/env python3

import sys

inputFile = 'input'
if len(sys.argv) >= 2:
    inputFile = sys.argv[1]

nums_list: list[list[int]] = []
with open(inputFile) as fin:
    for l in fin:
        nums_list.append([int(n) for n in l.split()])

# print(f'{nums_list=}')

def calc_diff_seq(ns: list[int]) -> list[int]:
    return [a2 - a1 for a1, a2 in zip(ns, ns[1:])]

# 0: a0[n+1] = a0[n]
# 1: a1[n+1] = a1[n] + a0[n]
# 2: a2[n+1] = a2[n] + a1[n]

def get_next(ns: list[int]) -> int:
    assert len(ns) != 0
    n0 = ns[0]
    if all(n == n0 for n in ns):
        return n0
    return ns[-1] + get_next(calc_diff_seq(ns))

def get_prev(ns: list[int]) -> int:
    assert len(ns) != 0
    n0 = ns[0]
    if all(n == n0 for n in ns):
        return n0
    return n0 - get_prev(calc_diff_seq(ns))

s1 = 0
for nums in nums_list:
    nxt = get_next(nums)
    # print(nxt)
    s1 += nxt

print(f'{s1=}')

s2 = 0
for nums in nums_list:
    prv = get_prev(nums)
    # print(prv)
    s2 += prv

print(f'{s2=}')
