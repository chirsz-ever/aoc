#!/usr/bin/env python3

import sys

def main() -> None:
    inputFile = 'input'
    if len(sys.argv) >= 2:
        inputFile = sys.argv[1]

    targets: list[int] = []
    numbers: list[list[int]] = []
    with open(inputFile) as fin:
        for l in fin:
            segs = l.strip().split()
            if len(segs) == 0:
                continue
            targets.append(int(segs[0][:-1]))
            numbers.append([int(s) for s in segs[1:]])

    s = 0
    for i in range(len(targets)):
        if has_answer(targets[i], numbers[i]):
            s += targets[i]
    print(f'{s=}')

def has_answer(target: int, numbers: list[int]) -> bool:
    assert len(numbers) > 0
    if len(numbers) == 1:
        return target == numbers[0]
    m = numbers[-1]
    if target % m == 0:
        if has_answer(target // m, numbers[:-1]):
            return True
    if target > m:
        if has_answer(target - m, numbers[:-1]):
            return True
        t = ten(m)
        l = (target - m) // t
        if target == l * t + m:
            if has_answer(l, numbers[:-1]):
                return True
    return False

def ten(m: int) -> int:
    return 10**len(str(m))

if __name__ == '__main__':
    main()
