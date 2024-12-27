#!/usr/bin/env python3

import sys

def is_safe(r: list[int]) -> bool:
    last: None | int = None
    direction: None | bool = None
    for i in range(len(r)):
        if last is not None:
            if not 1 <= abs(r[i] - last) <= 3:
                return False
            if direction is not None:
                if (r[i] > last) != direction:
                    return False
            direction = r[i] > last
        last = r[i]
    return True

def is_safe_1(r: list[int]) -> bool:
    if is_safe(r):
        return True
    for i in range(len(r)):
        r1 = r.copy()
        r1.pop(i)
        if is_safe(r1):
            return True
    return False

def main() -> None:
    inputFile = 'input'
    if len(sys.argv) >= 2:
        inputFile = sys.argv[1]
    
    reports: list[list[int]] = []

    with open(inputFile) as fin:
        for l in fin:
            l = l.strip()
            if l:
                reports.append([int(x) for x in l.split()])
    # for r in reports:
    #     print(f'{r} -> {is_safe(r)}')
    result = sum(1 for r in reports if is_safe_1(r))
    print(result)


if __name__ == '__main__':
    main()
