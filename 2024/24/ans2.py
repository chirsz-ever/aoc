#!/usr/bin/env python3

from functools import cache
import sys
from itertools import combinations, product

def main() -> None:
    inputFile = sys.argv[1]

    init_values: dict[str, int] = {}
    gates: dict[str, tuple[str, str, str]] = {}
    inputs = set()
    with open(inputFile) as fin:
        values_text, gates_text = fin.read().split("\n\n")
        for line in values_text.split("\n"):
            if line:
                name, value = line.split(": ")
                init_values[name] = int(value)
        for line in gates_text.split("\n"):
            if line:
                a1, op, a2, _, r = line.split()
                gates[r] = (op, a1, a2)
                inputs.add(a1)
                inputs.add(a2)

    def calc(wire: str, input: dict[str, int], swap_pairs: dict[str, str]) -> int:
        if wire in input:
            return input[wire]
        if wire in swap_pairs:
            wire = swap_pairs[wire]
        op, a1, a2 = gates[wire]
        v1 = calc(a1, input, swap_pairs)
        v2 = calc(a2, input, swap_pairs)
        if op == "AND":
            return v1 & v2
        elif op == "OR":
            return v1 | v2
        else:
            assert op == "XOR"
            return v1 ^ v2

    def calc_correct_z(i: int, input: dict[str, int]) -> int:
        x = int("".join(str(input[f"x{k:02}"]) for k in range(0, i + 1))[::-1], 2)
        y = int("".join(str(input[f"y{k:02}"]) for k in range(0, i + 1))[::-1], 2)
        return int(f"{x + y:0{i + 1}b}"[-(i+1)])

    def checkall(i: int, swap_pairs: dict[str, str]) -> bool:
        if i == 0:
            for x, y in product([0, 1], repeat=2):
                input = { 'x00': x, 'y00': y }
                try:
                    z = calc('z00', input, swap_pairs)
                except KeyError:
                    return False
                correct_z = calc_correct_z(0, input)
                if z != correct_z:
                    # print(f"{z} != {correct_z} at {i} when {input=}")
                    return False
            return True
        elif i == len(zs) - 1:
            for x1, y1, x2, y2 in product([0, 1], repeat=4):
                input = {
                    f'x{i:02}': 0,
                    f'y{i:02}': 0,
                    f'x{i-1:02}': x1,
                    f'y{i-1:02}': y1,
                    f'x{i-2:02}': x2,
                    f'y{i-2:02}': y2,
                }
                for k in range(i-2):
                    input[f'x{k:02}'] = 0
                    input[f'y{k:02}'] = 0
                try:
                    z = calc(f'z{i:02}', input, swap_pairs)
                except KeyError:
                    return False
                correct_z = calc_correct_z(i, input)
                if z != correct_z:
                    # print(f"{z} != {correct_z} at {i} when {input=}")
                    return False
            return True

        for x1, y1, x2, y2 in product([0, 1], repeat=4):
            input = {
                f'x{i:02}': x1,
                f'y{i:02}': y1,
                f'x{i-1:02}': x2,
                f'y{i-1:02}': y2,
            }
            for k in range(i-1):
                input[f'x{k:02}'] = 0
                input[f'y{k:02}'] = 0
            try:
                z = calc(f'z{i:02}', input, swap_pairs)
            except KeyError:
                return False
            correct_z = calc_correct_z(i, input)
            if z != correct_z:
                # print(f"{z} != {correct_z} at {i} when {input=}")
                return False
        return True

    xs = sorted(g for g in inputs if g[0] == "x" and g[1:].isdigit())
    ys = sorted(g for g in inputs if g[0] == "y" and g[1:].isdigit())
    zs = sorted(g for g in gates.keys() if g[0] == "z" and g[1:].isdigit())

    assert len(xs) == len(ys) == len(zs) - 1

    swap_pairs = {}
    # for i in range(len(xs)-1, -1, -1):
    # for i in range(len(xs), -1, -1):
    for i in range(1, len(zs)):
        print(i)
        if not checkall(i, swap_pairs):
            print(f"error at {i}...")
            rgs = set(gates.keys())
            # print(f'{rgs=}')

            # @cache
            def has_circle(g: str, swap_pairs: dict[str, str]) -> bool:
                visited = set()
                def visit(h) -> bool:
                    if h not in gates:
                        return False
                    if h in visited:
                        return True
                    visited.add(h)
                    if h in swap_pairs:
                        op, a1, a2 = gates[swap_pairs[h]]
                    else:
                        op, a1, a2 = gates[h]
                    return visit(a1) or visit(a2)
                return visit(g)

            for g1, g2 in combinations(rgs, 2):
                # print(f'try {g1}, {g2}')
                sp = swap_pairs.copy()
                sp[g1] = g2
                sp[g2] = g1
                if has_circle(f'z{i:02}', sp):
                    continue
                if checkall(i, sp):
                    print(f'found pair: {g1}, {g2}')
                    swap_pairs = sp
                    break
            else:
                raise RuntimeError(f'cannot find swap pair at {i}')
                # print(f'cannot find swap pair at {i}')
    print(','.join(sorted(swap_pairs.keys())))


if __name__ == "__main__":
    main()
