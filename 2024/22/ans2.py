#!/usr/bin/env python3

import sys
from collections import Counter

Seq4 = tuple[int, int, int, int]

def main() -> None:
    inputFile = sys.argv[1]

    with open(inputFile) as fin:
        secret_numbers = list(int(l.strip()) for l in fin if l.strip())

    seqs: Counter[Seq4] = Counter()
    for n in secret_numbers:
        this_buyer_seqs: Counter[Seq4] = Counter()
        price_changes: list[int] = []
        pre = 0
        for i in range(2000):
            n = step(n)
            p = n % 10
            price_changes.append(p - pre)
            pre = p
            if i >= 4:
                s: Seq4 = tuple(price_changes[-4:]) # type: ignore
                if s not in this_buyer_seqs:
                    this_buyer_seqs[s] = p
        for s, v in this_buyer_seqs.items():
            seqs[s] += v
    mk, mv = max(seqs.items(), key=lambda t: t[1])
    print('seqence:', mk)
    print('bananas', mv)

def step(n: int) -> int:
    n = ((n << 6) ^ n) & 0xFFFFFF
    n = ((n >> 5) ^ n) & 0xFFFFFF
    n = ((n << 11) ^ n) & 0xFFFFFF
    return n

if __name__ == '__main__':
    main()
