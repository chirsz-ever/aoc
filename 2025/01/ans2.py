#!/usr/bin/env python3

import sys

def zero_click(dial, step):
    if step > 0:
        return (dial + step) // 100
    if step < 0:
        k = (dial + step) // -100 + 1
        if dial == 0:
            k -= 1
        return k
    return 0

def main() -> None:
    inputFile = 'input'
    if len(sys.argv) >= 2:
        inputFile = sys.argv[1]

    dial = 50
    t = 0
    with open(inputFile) as fin:
        for l in fin:
            l = l.strip()
            step = -int(l[1:]) if l[0] == 'L' else int(l[1:])
            zk = zero_click(dial, step)
            if zk != 0:
                print(f'{dial} {l} clicks {zk}')
            t += zk
            dial = (dial + step) % 100
    print(f'{t=}')

if __name__ == '__main__':
    main()
