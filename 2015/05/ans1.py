#!/usr/bin/env python3

import sys


def main() -> None:
    inputFile = sys.argv[1]

    strs = []
    with open(inputFile) as fin:
        for l in fin:
            l = l.strip()
            if not l:
                continue
            strs.append(l)

    cnt = 0
    for s in strs:
        if is_nice(s):
            # print(f'{s} is nice')
            cnt += 1
        else:
            # print(f'{s} is not nice')
            pass
    print(cnt)


def is_nice(s: str) -> bool:
    if not has_3_vowels(s):
        return False
    if not has_twice(s):
        return False
    if any(k in s for k in ["ab", "cd", "pq", "xy"]):
        return False
    return True


def has_3_vowels(s: str) -> bool:
    return sum(s.count(v) for v in "aeiou") >= 3


def has_twice(s: str) -> bool:
    return any(s[k] == s[k + 1] for k in range(0, len(s) - 1))

if __name__ == "__main__":
    main()
