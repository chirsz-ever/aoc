#!/usr/bin/env python3

import sys
from itertools import combinations

def main() -> None:
    inputFile = 'input'
    if len(sys.argv) >= 2:
        inputFile = sys.argv[1]

    data: list[int] = []
    with open(inputFile) as fin:
        data = [int(c) for c in fin.read().strip()]
    # print(data)
    disk: list[int] = []
    i = 0
    while i < len(data):
        disk += [ i // 2 ] * data[i]
        if i + 1 < len(data):
            disk += [ -1 ] * data[i + 1]
        i += 2
    # print(disk)
    l = 0
    r = len(disk) - 1
    while r > l:
        if disk[l] == -1:
            if disk[r] != -1:
                disk[l], disk[r] = disk[r], -1
                l += 1
                r -= 1
            else:
                r -= 1
        else:
            l += 1
    # print(disk)
    s = 0
    for i in range(len(disk)):
        if disk[i] >= 0:
            s += disk[i] * i
        else:
            break
    print(s)

if __name__ == '__main__':
    main()
