#!/usr/bin/env python3

import sys
import functools

def log(s: str):
    if False:
        print(s)

def prefix_may_match(gs: tuple[int,...], rec1: str) -> bool:
    if len(gs) == 0:
        return '#' not in rec1
    assert gs[0] != 0
    gi = 0
    ri = 0
    gc = 0
    while ri < len(rec1):
        if rec1[ri] == '?':
            return gi < len(gs) and gc <= gs[gi] or gi == len(gs) and gc == 0 and '#' not in rec1[ri:]
        elif rec1[ri] == '.':
            if gc > 0:
                if gi < len(gs) and gs[gi] == gc:
                    gc = 0
                    gi += 1
                else:
                    return False
        elif rec1[ri] == '#':
            gc += 1
        ri += 1
    return (rec1[-1] == '.' and gi == len(gs)) or (gi == len(gs) - 1 and gs[gi] == gc)

@functools.cache
def calc_possibilities(rec: str, gs: tuple[int,...]) -> int:
    # print(f'calc_possibilities("{rec}", {gs})')
    if len(rec) == 0:
        return len(gs) == 0

    assert len(gs) == 0 or gs[0] != 0

    if rec[0] == '.':
        k = 0
        while rec[k] == '.':
            k += 1
        return calc_possibilities(rec[k:], gs)

    if not prefix_may_match(gs, rec):
        log(f'{rec} cannot match {gs}')
        return 0
    else:
        if '?' not in rec:
            log(f'{rec} may match {gs} --- *')
        else:
            log(f'{rec} may match {gs}')

    if '?' not in rec:
        return 1

    p = 0
    if rec[0] == '#':
        # first group must start with begining
        if len(gs) == 0:
            return 0
        k = 0
        while k < len(rec) and k < gs[0] and rec[k] in '#?':
            k += 1
        if k < gs[0] or (k < len(rec) and rec[k] == '#'):
            return 0
        # now, k == gs[0] and rec[k] != '#'
        if k < len(rec):
            if rec[k] == '?':
                # rec[k] must be '.'
                k += 1
            while k < len(rec) and rec[k] == '.':
                k += 1
            p += calc_possibilities(rec[k:], gs[1:])
        else:
            return 1 if len(gs) == 1 else 0
    else: # rec[0] == '?'
        # rec[0] as '.'
        k = 1
        while k < len(rec) and rec[k] == '.':
            k += 1
        p += calc_possibilities(rec[k:], gs)

        # rec[0] as '#'
        if len(gs) > 0:
            rec1 = '#' + rec[1:]
            p += calc_possibilities(rec1, gs)
    return p

def main() -> None:
    inputFile = 'input'
    if len(sys.argv) >= 2:
        inputFile = sys.argv[1]

    records: list[tuple[str, list[int]]] = []
    with open(inputFile) as fin:
        for l in fin:
            r1, grps = l.split()
            records.append((r1, [int(s) for s in grps.split(',')]))

    s = 0
    for rec, gs in records:
        s += calc_possibilities('?'.join([rec]*5), tuple(gs*5))
    print(f'{s=}')

if __name__ == '__main__':
    main()
