#!/usr/bin/env python3

import sys
import itertools
from typing import TypeVar, Iterable

T = TypeVar('T')

def flatten(list_of_lists: Iterable[Iterable[T]]) -> list[T]:
    return list(itertools.chain.from_iterable(list_of_lists))

Coord = tuple[int, int]

def main() -> None:
    inputFile = sys.argv[1]

    with open(inputFile) as fin:
        codes = list(l.strip() for l in fin if l.strip())

    min_key_presses = [min_keys(code) for code in codes]
    s = sum(len(min_key_presses[i]) * int(codes[i][:-1]) for i in range(len(codes)))
    print(f'{s=}')

def min_keys(code: str) -> str:
    seqs2 = all_keys(code, keymap_2)
    seqs1 = flatten(all_keys(s, keymap_1) for s in seqs2)
    seqs0 = flatten(all_keys(s, keymap_1) for s in seqs1)
    
    c0 = min(seqs0, key=len)

    # print(c0)
    # print(c1)
    # print(c2)

    # print(f'{code}: {len(c0)}\n  {c0}')
    # print(seqs0)
    # print(seqs1)
    # print(seqs2)
    return c0

keymap_2 = {
    '7': (0, 0), '8': (0, 1), '9': (0, 2),
    '4': (1, 0), '5': (1, 1), '6': (1, 2),
    '1': (2, 0), '2': (2, 1), '3': (2, 2),
                 '0': (3, 1), 'A': (3, 2),
}

keymap_1 = {
                 '^': (0, 1), 'A': (0, 2),
    '<': (1, 0), 'v': (1, 1), '>': (1, 2),
}

def straight_move(start: Coord, end: Coord) -> str:
    if start[0] == end[0]:
        key = '>' if end[1] > start[1] else '<'
        count = abs(end[1] - start[1])
    else:
        key = 'v' if end[0] > start[0] else '^'
        count = abs(end[0] - start[0])
    return key * count

def get_move_direction(start: Coord, end: Coord) -> int:
    if start[0] == end[0]:
        return 0
    return 1

def all_keys(code: str, keymap: dict[str, tuple[int, int]]) -> list[str]:
    key_seqs = ['']
    def append(key_seqs: list[str], t: str):
        return [s + t for s in key_seqs]
    for i in range(-1, len(code) - 1):
        start_key = code[i] if i >= 0 else 'A'
        end_key = code[i + 1]
        if start_key == end_key:
            key_seqs = append(key_seqs, 'A')
            continue
        start = keymap[start_key]
        end = keymap[end_key]
        # print(f'[{start_key}]{start} -> [{end_key}]{end}')
        if start[0] == end[0] or start[1] == end[1]:
            key_seqs = append(key_seqs, straight_move(start, end) + 'A')
        elif (start[0], end[1]) not in keymap.values():
            key_seqs = append(key_seqs, straight_move(start, (end[0], start[1])) + straight_move((end[0], start[1]), end) + 'A')
        elif (end[0], start[1]) not in keymap.values():
            key_seqs = append(key_seqs, straight_move(start, (start[0], end[1])) + straight_move((start[0], end[1]), end) + 'A')
        else:
            # print(f'[{start_key}]{start} -> [{end_key}]{end} split')
            s1 = append(key_seqs, straight_move(start, (start[0], end[1])) + straight_move((start[0], end[1]), end) + 'A')
            s2 = append(key_seqs, straight_move(start, (end[0], start[1])) + straight_move((end[0], start[1]), end) + 'A')
            key_seqs = s1 + s2
    return key_seqs

if __name__ == '__main__':
    main()
