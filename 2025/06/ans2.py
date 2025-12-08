#!/usr/bin/env python3

import sys

def prod(ns):
    p = 1
    for n in ns:
        p *= n
    return p

def main() -> None:
    global w, h
    inputFile = 'input'
    if len(sys.argv) >= 2:
        inputFile = sys.argv[1]

    chars: list[str] = []
    ops: list[str] = []
    with open(inputFile) as fin:
        for l in fin:
            l = l.removesuffix('\n')
            if l.strip()[0].isdecimal():
                chars.append(l)
            else:
                ops = l.strip().split()
                break

    # print(numbers)
    # print(ops)

    s = 0
    r = -1
    opi = len(ops) - 1
    col = ''
    for j in range(len(chars[0]) - 1, -1, -1):
        col = ''.join(chars[i][j] for i in range(0, len(chars)))
        if col.isspace():
            s += r
            r = -1
            opi -= 1
        else:
            op = ops[opi]
            if op == '+':
                r = 0 if r == -1 else r
                r += int(col.strip())
            else:
                assert op == '*'
                r = 1 if r == -1 else r
                r *= int(col.strip())
        # print(f'{r=}')
    else:
        if r != -1:
            s += r
    print(f'{s=}')

if __name__ == '__main__':
    main()
