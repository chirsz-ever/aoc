#!/usr/bin/env python3

import sys
import re
from functools import cache

def getArg(n, default):
    if len(sys.argv) >= n + 1:
        return sys.argv[n]
    return default


inputFile = getArg(1, "input")

reStep = re.compile(
    r"""inp w
mul x 0
add x z
mod x 26
div z (?P<d>-?\d+)
add x (?P<a>-?\d+)
eql x w
eql x 0
mul y 0
add y 25
mul y x
add y 1
mul z y
mul y 0
add y w
add y (?P<b>-?\d+)
mul y x
add z y
"""
)


def main() -> None:
    inputFile = sys.argv[1]

    args: list[tuple[int, int, int]] = []
    with open(inputFile) as fin:
        insts = fin.read()
        cnt = 0
        for m in reStep.finditer(insts):
            cnt += 1
            d = int(m["d"])
            a = int(m["a"])
            b = int(m["b"])
            args.append((d, a, b))
            # print(f"{cnt:2}: {d = :3} {a = :3}, {b = :3}")

    assert len(args) == 14

    max_model_number = 0
    ds = [0] * 14

    @cache
    def dfs(n: int, z: int) -> bool:
        nonlocal max_model_number
        if n == 14:
            # print(f'{mn}: {z=}')
            if z == 0:
                mn = 0
                for d in ds:
                    mn = mn * 10 + d
                if max_model_number < mn:
                    max_model_number = mn
                return True
            return False

        if z // 26**(14-n) != 0:
            return False

        d, a, b = args[n]
        c = mod(z, 26) + a
        for w in range(1, 10):
            if w == c:
                nz = div(z, d)
            else:
                nz = 26 * div(z, d) + w + b
            ds[n] = w
            if dfs(n + 1, nz):
                return True
        return False

    dfs(0, 0)
    print(max_model_number)


# round to zero
def div(a: int, b: int) -> int:
    return int(a / b)


def mod(a: int, b: int) -> int:
    return a - int(a / b) * b


if __name__ == "__main__":
    main()
