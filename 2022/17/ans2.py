#!/usr/bin/env python3

import sys
from itertools import count

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
    # steps = int(sys.argv[2])

    with open(inputFile) as fin:
        jets = fin.read().strip()

    # x: left to right, y: bottom to top

    j = 0
    chamber: set[Coord] = set()
    # highest_y = -1
    height_history: list[int] = []

    # (rock index, jet index) -> [step]
    rock_jet_pairs: dict[tuple[int, int], set[int]] = {}
    # [(rock index, jet index)]
    history10: list[tuple[int, int]] = []
    c2_step = -1
    c1_step = -1

    def match_history(current_step: int, size: int) -> bool:
        nonlocal c1_step, c2_step
        if len(history10) < size:
            return False
        if not all(rj in rock_jet_pairs and len(rock_jet_pairs[rj]) >= 1 for rj in history10[-size:]):
            return False
        q = [(step, 0) for step in rock_jet_pairs[history10[-size]] if step != current_step - size + 1]
        while q:
            (step, i) = q.pop()
            if i == size - 1 and step != s:
                c1_step = step
                c2_step = s
                return True
            for pre_step in rock_jet_pairs[history10[i-size+1]]:
                if pre_step == step + 1:
                    q.append((step + 1, i + 1))
        return False

    for s in count():
        rock = rock_seq[s % len(rock_seq)]
        hy = get_highest_y(chamber)
        height_history.append(hy)

        history10.append((s % len(rock_seq), j % len(jets)))
        if len(history10) > 10:
            history10.pop(0)
            assert len(history10) == 10

        if match_history(s, 10):
            break

        rock_jet_pairs.setdefault(history10[-1], set()).add(s)

        x = 2
        y = hy + 4

        if s % 100 == 0:
            chamber = remove_low_rows(chamber)

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

    c1_height = height_history[c1_step]
    c2_height = height_history[c2_step]

    print('Cycle detected at step', c2_step, ', rock:', history10[-1][0], ', jet:', history10[-1][1], ', height:', c2_height)
    print('First occurrence at step', c1_step, 'height', c1_height)

    cycle_length = c2_step - c1_step
    cycle_height = c2_height - c1_height
    total_height = height_history[c1_step + (1000000000001 - c1_step) % cycle_length] + \
        (1000000000001 - c1_step) // cycle_length * cycle_height
    print('Total height:', total_height)

def remove_low_rows(chamber: set[Coord]) -> set[Coord]:
    highest_ys = [-1] * 7
    hy = get_highest_y(chamber)
    for x in range(7):
        for y in range(hy, -1, -1):
            if (x, y) in chamber:
                highest_ys[x] = y
                break
    min_y = min(highest_ys) - 1
    new_chamber = set()
    for (x, y) in chamber:
        if y >= min_y:
            new_chamber.add((x, y))
    return new_chamber

def print_chamber(chamber: set[Coord], h: int) -> None:
    highest_y = get_highest_y(chamber)
    for y in range(highest_y, highest_y-h, -1):
        row = ''
        for x in range(7):
            if (x, y) in chamber:
                row += '#'
            else:
                row += '.'
        print(row)
    print()

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
