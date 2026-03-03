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
            if support_ssl(l):
                s += 1

    print(s)


def support_ssl(l: str) -> bool:
    segs, hns = split(l)
    # print(segs, hns)
    ab_pairs_ip = union_all(map(get_aba, segs))
    ab_pairs_rev_hn = { (b, a) for a, b in union_all(map(get_aba, hns)) }
    # print(l)
    # print(' ', segs, hns)
    # print(' ', ab_pairs_ip)
    # print(' ', ab_pairs_rev_hn)
    return bool(ab_pairs_ip.intersection(ab_pairs_rev_hn))

def union_all(ss):
    s = set()
    for s1 in ss:
        s.update(s1)
    return s

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

def get_aba(s: str) -> set[tuple[str, str]]:
    abas = set()
    for i in range(0, len(s) - 2):
        if s[i] != s[i+1] and s[i] == s[i+2]:
            abas.add((s[i], s[i+1]))
    return abas

if __name__ == "__main__":
    main()
