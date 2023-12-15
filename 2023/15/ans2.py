#!/usr/bin/env python3

import sys

def my_hash(s: str) -> int:
    h = 0
    for c in s:
        n = ord(c)
        h += n
        h *= 17
        h %= 256
    return h

def main() -> None:
    inputFile = 'input'
    if len(sys.argv) >= 2:
        inputFile = sys.argv[1]

    with open(inputFile) as fin:
        inputs: list[str] = fin.read().strip().split(',')

    hm = [[] for _ in range(256)]
    for inst in inputs:
        if inst.endswith('-'):
            lbl = inst[:-1]
            box = hm[my_hash(lbl)]
            for i, (len_lbl, _) in enumerate(box):
                if len_lbl == lbl:
                    del box[i]
                    break
        else:
            lbl, new_foc = inst.split('=')
            box = hm[my_hash(lbl)]
            for i, (len_lbl, _) in enumerate(box):
                if len_lbl == lbl:
                    box[i] = (lbl, int(new_foc))
                    break
            else:
                box.append((lbl, int(new_foc)))

    result = 0
    for (i, box) in enumerate(hm):
        for j, (_, foc) in enumerate(box):
            result += (i + 1) * (j + 1) * foc
    print(f'{result=}')


if __name__ == '__main__':
    main()
