#!/usr/bin/env python3

import sys

Coord = tuple[int, int]  # (x, y)

Rock = list[str]

rock_seq: list[Rock] = [
    ['####'],
    ['.#.', '###', '.#.'],
    ['###', '..#', '..#'],
    ['#', '#', '#', '#'],
    ['##', '##'],
]

def main() -> None:
    inputFile = sys.argv[1]
    steps = int(sys.argv[2])

    with open(inputFile) as fin:
        jets = fin.read().strip()

    # x: left to right, y: bottom to top

    j = 0
    chamber: set[Coord] = set()

    for s in range(steps):
        rock = rock_seq[s % len(rock_seq)]
        x = 2
        y = get_highest_y(chamber) + 4

        while True:
            jet = jets[j % len(jets)]
            j += 1

            if jet == '<':
                if can_move(chamber, rock, x - 1, y):
                    x -= 1
            else:
                assert jet == '>'
                if can_move(chamber, rock, x + 1, y):
                    x += 1

            if can_move(chamber, rock, x, y - 1):
                y -= 1
            else:
                place_rock(chamber, rock, x, y)
                break

    print(get_highest_y(chamber) + 1)

def can_move(chamber: set[Coord], rock: Rock, x: int, y: int) -> bool:
    for dy, row in enumerate(rock):
        for dx, c in enumerate(row):
            if c == '#':
                rx = x + dx
                ry = y + dy
                if rx < 0 or rx >= 7 or ry < 0 or (rx, ry) in chamber:
                    return False
    return True


def place_rock(chamber: set[Coord], rock: Rock, x: int, y: int) -> None:
    for dy, row in enumerate(rock):
        for dx, c in enumerate(row):
            if c == '#':
                rx = x + dx
                ry = y + dy
                chamber.add((rx, ry))

def get_highest_y(chamber: set[Coord]) -> int:
    if not chamber:
        return -1
    return max(y for _, y in chamber)

if __name__ == "__main__":
    main()
