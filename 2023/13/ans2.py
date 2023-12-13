#!/usr/bin/env python3

import sys

def log(s: str):
    return
    print(s)

Pattern = list[list[str]]

def find_may_fixed(refl_indxes: list[list[int]]) -> list[int]:
    cnt = {}
    for s in refl_indxes:
        for i in s:
            cnt[i] = cnt.get(i, 0) + 1
    return [i for i, c in cnt.items() if c == len(refl_indxes) - 1]

def format_pat(p: Pattern) -> str:
    return '\n'.join(''.join(row) for row in p)

# is_vertical, index
def find_refl(p: Pattern) -> tuple[bool, int]:
    height = len(p)
    width = len(p[0])
    # first try vertical
    refl_indxes: list[list[int]] = [[] for _ in range(height)]
    for r, row in enumerate(p):
        for c in range(1, width):
            if all(row[i] == row[refl_pos] for i in range(0, c) if (refl_pos := 2 * c - 1 - i) < width):
                refl_indxes[r].append(c)
    log(f'{refl_indxes=}')
    may_fixed_cols = find_may_fixed(refl_indxes)
    log(f'{may_fixed_cols=}')
    for c in may_fixed_cols:
        for r, cs in enumerate(refl_indxes):
            if c not in cs:
                log(f"try fix row {r}")
                if sum(p[r][i] == p[r][refl_pos] for i in range(0, c) if (refl_pos := 2 * c - 1 - i) < width) == min(c, width - c) - 1:
                    return True, c
                break

    # try horizontal
    refl_indxes = [[] for _ in range(width)]
    for c in range(0, width):
        for r in range(1, height):
            if all(p[i][c] == p[refl_pos][c] for i in range(0, r) if (refl_pos := 2 * r - 1 - i) < height):
                refl_indxes[c].append(r)
    log(f'{refl_indxes=}')
    may_fixed_rows = find_may_fixed(refl_indxes)
    log(f'{may_fixed_rows=}')
    for r in may_fixed_rows:
        for c, rs in enumerate(refl_indxes):
            if r not in rs:
                log(f"try fix column {c} with aix {r}")
                if sum(p[i][c] == p[refl_pos][c] for i in range(0, r) if (refl_pos := 2 * r - 1 - i) < height) == min(r, height - r) - 1:
                    return False, r
                break

    raise RuntimeError(f"cannot find refecltion of\n{format_pat(p)}")
    # print(f"cannot find refecltion of\n{format_pat(p)}", file=sys.stderr)

def main() -> None:
    inputFile = 'input'
    if len(sys.argv) >= 2:
        inputFile = sys.argv[1]

    pats: list[Pattern] = [[]]
    with open(inputFile) as fin:
        for l in fin:
            l = l.strip()
            if len(l) == 0:
                pats.append([])
            else:
                pats[-1].append(list(l))
    # print(pats)

    refls = [refl for p in pats if (refl := find_refl(p))]

    s = 0
    for is_vertical, index in refls:
        if is_vertical:
            s += index
        else:
            s += index * 100
    print(f'{s=}')

if __name__ == '__main__':
    main()
