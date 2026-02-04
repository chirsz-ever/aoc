#!/usr/bin/env python3

import sys

def main() -> None:
    input = sys.argv[1]
    repeat = int(sys.argv[2]) if len(sys.argv) > 2 else 40

    s = input
    for _ in range(repeat):
        s = step(s)
    # print(s)
    print(len(s))


def step(s: str) -> str:
    ns: list[str] = []
    last = ''
    cnt = 0
    for c in s:
        if c == last:
            cnt += 1
        else:
            if cnt > 0:
                ns.extend([str(cnt), last])
            cnt = 1
        last = c
    if cnt != 0:
        ns.extend([str(cnt), last])
    return ''.join(ns)

if __name__ == "__main__":
    main()
