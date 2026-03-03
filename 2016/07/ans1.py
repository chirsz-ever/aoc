#!/usr/bin/env python3

import sys
from collections import Counter

def main() -> None:
    inputFile = sys.argv[1]

    s = 0
    with open(inputFile) as fin:
        for l in fin:
            l = l.strip()
            if not l:
                continue
            if support_tls(l):
                s += 1

    print(s)


def support_tls(l: str) -> bool:
    segs, hns = split(l)
    # print(segs, hns)
    return any(map(has_abba, segs)) and not any(map(has_abba, hns))

def split(l: str) -> tuple[list[str], list[str]]:
    segs = []
    hns = []
    a = 0
    while True:
        bl = l.find('[', a)
        if bl == -1:
            segs.append(l[a:])
            break
        br = l.find(']', bl)
        assert br > 0
        if bl > a:
            segs.append(l[a:bl])
        if br - bl > 1:
            hns.append(l[bl+1:br])
        a = br + 1
    return segs, hns

def has_abba(s: str) -> bool:
    for i in range(0, len(s) - 3):
        if s[i] != s[i+1] and s[i] == s[i+3] and s[i + 1] == s[i+2]:
            return True
    return False

if __name__ == "__main__":
    main()
