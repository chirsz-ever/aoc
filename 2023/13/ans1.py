#!/usr/bin/env python3

import sys

def log(s: str):
    return
    print(s)

Pattern = list[str]

def intersection(sets) -> set:
    it = iter(sets)
    s = set(next(it))
    for t in it:
        s.intersection_update(t)
    return s

def format_pat(p: Pattern) -> str:
    return '\n'.join(p)

# is_vertical, index
def find_refl(p: Pattern) -> tuple[bool, int] | None:
    height = len(p)
    width = len(p[0])
    # first try vertical
    refl_indxes = [[] for _ in range(height)]
    for r, row in enumerate(p):
        for c in range(1, width):
            if all(row[i] == row[refl_pos] for i in range(0, c) if (refl_pos := 2 * c - 1 - i) < width):
                refl_indxes[r].append(c)
    log(f'{refl_indxes=}')
    vertical_indexes: set[int] = intersection(refl_indxes)
    log(f'{vertical_indexes=}')
    if len(vertical_indexes) == 1:
        return True, vertical_indexes.pop()
    assert len(vertical_indexes) == 0, vertical_indexes

    # try horizontal
    refl_indxes = [[] for _ in range(width)]
    for c in range(0, width):
        for r in range(1, height):
            if all(p[i][c] == p[refl_pos][c] for i in range(0, r) if (refl_pos := 2 * r - 1 - i) < height):
                refl_indxes[c].append(r)
    log(f'{refl_indxes=}')
    horizontal_indexes: set[int] = intersection(refl_indxes)
    log(f'{horizontal_indexes=}')
    if len(horizontal_indexes) == 1:
        return False, horizontal_indexes.pop()
    assert len(horizontal_indexes) == 0, horizontal_indexes
    # raise RuntimeError(f"cannot find refecltion of\n{format_pat(p)}")
    print(f"cannot find refecltion of\n{format_pat(p)}", file=sys.stderr)
    return

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
                pats[-1].append(l)
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
