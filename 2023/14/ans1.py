#!/usr/bin/env python3

import sys

Map = list[list[str]]

def print_map(map: Map):
    for row in map:
        for grid in row:
            print(grid, end='')
        print()

def do_slide(map: Map):
    height = len(map)
    width = len(map[0])
    for col in range(0, width):
        slide_target: int|None = None
        for row in range(0, height):
            grid = map[row][col]
            match (grid, slide_target):
                case ('#', _):
                    slide_target = None
                case ('.', None):
                    slide_target = row
                case ('O', int()):
                    map[slide_target][col] = 'O'
                    map[row][col] = '.'
                    slide_target += 1

def calc_load(map: Map) -> int:
    height = len(map)
    load = 0
    for i, row in enumerate(map):
        load += (height - i) * row.count('O')
    return load

def main() -> None:
    inputFile = 'input'
    if len(sys.argv) >= 2:
        inputFile = sys.argv[1]

    input: Map = []
    with open(inputFile) as fin:
        for l in fin:
            l = l.strip()
            input.append(list(l))
            pass

    # print_map(input)
    do_slide(input)
    # print_map(input)
    print(f'load={calc_load(input)}')

if __name__ == '__main__':
    main()
