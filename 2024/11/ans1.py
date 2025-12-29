#!/usr/bin/env python3

import sys
from functools import lru_cache

StoneSeq = list['int | StoneSeq']

def main() -> None:
    inputFile = sys.argv[1]
    blink_times = int(sys.argv[2])

    with open(inputFile) as fin:
        stones: StoneSeq = [int(s) for s in fin.read().split()]

    for _ in range(blink_times):
        blink(stones)
        # print(stones)
    cnt = count_stones(stones)
    print(f'{cnt=}')

def blink(stones: StoneSeq) -> None:
    for i in range(len(stones)):
        s = stones[i]
        if type(s) == int:
            if s == 0:
                stones[i] = 1
            else:
                ss = str(s)
                h = len(ss) // 2
                if len(ss) % 2 == 0:
                    stones[i] = [ int(ss[:h]), int(ss[h:]) ]
                else:
                    stones[i] = s * 2024
        else:
            assert type(s) == list
            blink(s)


def count_stones(stones: StoneSeq) -> int:
    cnt = 0
    for s in stones:
        if type(s) == int:
            cnt += 1
        else:
            assert type(s) == list
            cnt += count_stones(s)
    return cnt

if __name__ == '__main__':
    main()
