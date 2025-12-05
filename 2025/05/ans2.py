#!/usr/bin/env python3

import sys

def main() -> None:
    global w, h
    inputFile = 'input'
    if len(sys.argv) >= 2:
        inputFile = sys.argv[1]

    ranges: list[tuple[int, int]] = []
    state = 0
    with open(inputFile) as fin:
        for l in fin:
            l = l.strip()
            if len(l) == 0:
                break
            l, h = map(int, l.split('-'))
            ranges.append((l, h))

    # print(ranges)

    uniqued_ranges: list[tuple[int, int]] = []
    for l0, h0 in ranges:
        new_ranges = [(l0, h0)]
        for l1, h1 in uniqued_ranges:
            new_ranges1 = []
            for l, h in new_ranges:
                if h < l1 or l > h1:
                    new_ranges1.append((l, h))
                else:
                    if l < l1:
                        new_ranges1.append((l, l1 - 1))
                    if h > h1:
                        new_ranges1.append((h1 + 1, h))
            new_ranges = new_ranges1
            if len(new_ranges) == 0:
                break
        uniqued_ranges.extend(new_ranges)

    # print(uniqued_ranges)
    s = sum(h - l + 1 for l, h in uniqued_ranges)
    print(f'{s=}')


if __name__ == '__main__':
    main()
