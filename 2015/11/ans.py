#!/usr/bin/env python3

import sys
import re


def main() -> None:
    input = sys.argv[1]
    repeat = int(sys.argv[2]) if len(sys.argv) > 2 else 40

    s = step(remove_iol(input))
    while not validate(s):
        s = step(s)
    print(s)
    
def remove_iol(s: str) -> str:
    for i, c in enumerate(s):
        if c in 'iol':
            return s[:i] + chr(ord(c) + 1) + 'a' * (len(s) - i - 1)
    return s


def validate(s: str) -> bool:
    for i, f in enumerate([validate_rule1, validate_rule2, validate_rule3]):
        if not f(s):
            # print(f'{s} not match rule {i}')
            return False
    return True


def validate_rule1(s: str) -> bool:
    for i in range(0, len(s) - 3):
        if ord(s[i]) == ord(s[i + 1]) - 1 == ord(s[i + 2]) - 2:
            return True
    return False


def validate_rule2(s: str) -> bool:
    return all(c not in s for c in "iol")


reRule3 = re.compile(r"(.)\1.*(.)\2")


def validate_rule3(s: str) -> bool:
    return reRule3.search(s) is not None


def step(s: str) -> str:
    if not s:
        return 'a'
    if s[-1] == 'z':
        return step(s[:-1]) + 'a'
    return s[:-1] + next_c(s[-1])

def next_c(c: str) -> str:
    c = chr(ord(c) + 1)
    if c in 'iol':
        c = chr(ord(c) + 1)
    return c

if __name__ == "__main__":
    main()
