#!/usr/bin/env python3

from functools import cache
import sys

def main() -> None:
    inputFile = sys.argv[1]

    init_values: dict[str, int] = {}
    gates: dict[str, tuple[str, str, str]] = {}
    with open(inputFile) as fin:
        values_text, gates_text = fin.read().split('\n\n')
        for l in values_text.split('\n'):
            if l:
                name, value = l.split(': ')
                init_values[name] = int(value)
        for l in gates_text.split('\n'):
            if l:
                a1, op, a2, _, r = l.split()
                gates[r] = (op, a1, a2)

    @cache
    def calc(wire: str) -> int:
        if wire in init_values:
            return init_values[wire]
        op, a1, a2 = gates[wire]
        v1 = calc(a1)
        v2 = calc(a2)
        if op == 'AND':
            return v1 & v2
        elif op == 'OR':
            return v1 | v2
        else:
            assert op == 'XOR'
            return v1 ^ v2

    z_wires = {}
    for w in gates:
        if w.startswith('z'):
            z_wires[w] = calc(w)

    r = ''
    for w in sorted(z_wires.keys()):
        # print(f'{w}: {z_wires[w]}')
        r += str(z_wires[w])

    print(int(r[::-1], 2))

if __name__ == '__main__':
    main()
