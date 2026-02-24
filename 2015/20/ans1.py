#!/usr/bin/env python3

import sys
from itertools import count


def main() -> None:
    # inputFile = sys.argv[1]
    input_num = int(sys.argv[1])
    
    # print(f'psum({input_num}) = {psum(input_num)}')
    # return

    for n in count():
        ps = psum(n)
        if ps * 10 >= input_num:
            print(f'psum({n}) = {ps}')
            print(n)
            break

def psum(n: int) -> int:
    if n <= 3:
        return n
    pfs = prime_factors(n)
    # print(f'prime_factors({n}) = {pfs}')
    s = 1
    for p, k in pfs:
        s *= (p ** (k + 1) - 1) // (p - 1)
    return s

def prime_factors(n: int) -> list[tuple[int, int]]:
    pfs: list[tuple[int, int]] = []
    k2 = 0
    while n % 2 == 0:
        n //= 2
        k2 += 1

    if k2 > 0:
        pfs.append((2, k2))

    p = 3
    while True:
        k = 0
        while n % p == 0:
            n //= p
            k += 1
        if k > 0:
            pfs.append((p, k))
        p += 2
        if p % 3 == 0:
            p += 2
        if n == 1 or p > n ** 0.5:
            break
    if n != 1:
        pfs.append((n, 1))
    return pfs

if __name__ == "__main__":
    main()
