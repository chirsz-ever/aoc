#!/usr/bin/env python3

import sys
from functools import cache

def main() -> None:
    inputFile = sys.argv[1]
    blink_times = int(sys.argv[2])

    with open(inputFile) as fin:
        stones = [int(s) for s in fin.read().split()]

    cnt = 0
    for s in stones:
        cnt += count_blink(s, blink_times)
    print(f'{cnt=}')

@cache
def count_blink(s: int, blink_times: int) -> int:
    # print(f'count_blink({s}, {blink_times})')
    if blink_times == 1:
        if s == 0:
            return 1
        else:
            ss = str(s)
            h = len(ss) // 2
            if len(ss) % 2 == 0:
                return 2
            else:
                return 1
    else:
        if s == 0:
            return count_blink(1, blink_times - 1)
        else:
            ss = str(s)
            h = len(ss) // 2
            if len(ss) % 2 == 0:
                return count_blink(int(ss[:h]), blink_times - 1) + count_blink(int(ss[h:]), blink_times - 1)
            else:
                return count_blink(s * 2024, blink_times - 1)

if __name__ == '__main__':
    main()
