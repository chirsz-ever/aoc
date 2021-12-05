from math import *

tst = input()

bids = [(int(bid), i) for i, bid in enumerate(input().split(',')) if bid.isdigit()]

print(bids)

mbids = [(bid, (bid - i) % bid) for bid, i in bids]

print(mbids)

def ex_gcd(a,b):
    if 0==b:
        return 1, 0, a
    x, y, q = ex_gcd(b, a % b)
    return y , x - a // b * y, q

def minv(a,b):
    return ex_gcd(a,b)[0]

def cn_remain(ps):
    M = prod(m for m, _ in ps)
    print(f"{M=}")
    x = sum(M//m * minv(M//m, m) * t for m, t in ps)
    print(f"{x=}")
    return x % M

answer = cn_remain(mbids)

print(f"{answer=}")
