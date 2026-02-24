#!/usr/bin/env python3

import sys


target_sue = {
    "children": 3,
    "cats": 7,
    "samoyeds": 2,
    "pomeranians": 3,
    "akitas": 0,
    "vizslas": 0,
    "goldfish": 5,
    "trees": 3,
    "cars": 2,
    "perfumes": 1,
}


def main() -> None:
    inputFile = sys.argv[1]

    sue_list: list[dict[str, int]] = []
    with open(inputFile) as fin:
        for l in fin:
            l = l.strip()
            if not l:
                continue
            segs = l.split()
            sue = {}
            for i in range(2, len(segs), 2):
                prop = segs[i].removesuffix(":")
                # print(f'prop={prop}, ')
                value = int(segs[i + 1].removesuffix(","))
                sue[prop] = value
            sue_list.append(sue)
    # print(sue_list)
    
    def matches(sue: dict[str, int], k: str) -> bool:
        if k not in sue:
            return True
        v = sue[k]
        tk = target_sue[k]
        if k in ['cats', 'trees']:
            return tk < v
        if k in ['pomeranians', 'goldfish']:
            return tk > v
        return tk == v
    
    for i, sue in enumerate(sue_list):
        if all(matches(sue, k) for k in target_sue):
            print(f'{i+1}')


if __name__ == "__main__":
    main()
