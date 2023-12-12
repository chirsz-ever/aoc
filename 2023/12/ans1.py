#!/usr/bin/env python3

import sys

def log(s: str):
    if False:
        print(s)

def prefix_may_match(gs: list[int], rec1: list[str]) -> bool:
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

def calc_poss(rec: str, gs: list[int], rec1: list[str], k: int) -> int:
    assert k >= 0
    if k < len(rec) and rec[k] != '?':
        return calc_poss(rec, gs, rec1, k + 1)
    if not prefix_may_match(gs, rec1):
        log(f'{"".join(rec1)} cannot match {gs}')
        return 0
    else:
        if '?' not in rec1:
            log(f'{"".join(rec1)} may match {gs} --- *')
        else:
            log(f'{"".join(rec1)} may match {gs}')
    if k >= len(rec) or '?' not in rec1:
        return 1
    p = 0
    if rec[k] == '?':
        rec1[k] = '.'
        p += calc_poss(rec, gs, rec1, k + 1)
        rec1[k] = '#'
        p += calc_poss(rec, gs, rec1, k + 1)
        rec1[k] = '?'
    return p

def calc_possibilities(rec: str, gs: list[int]) -> int:
    rec1 = list(rec)
    p = calc_poss(rec, gs, rec1, 0)
    print(f'{p=}')
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
        s += calc_possibilities(rec, gs)
    print(f'{s=}')

if __name__ == '__main__':
    main()
