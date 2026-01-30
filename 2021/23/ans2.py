#!/usr/bin/env python3

from dataclasses import dataclass, replace
import sys


Coord = tuple[int, int]


Amphipods = dict[Coord, str]


def main() -> None:
    inputFile = sys.argv[1]

    amphipods: dict[Coord, str] = {}
    with open(inputFile) as fin:
        for lineno, l in enumerate(fin):
            if lineno == 2 or lineno == 3:
                i = 2 if lineno == 2 else 5
                amphipods[i, 3] = l[3]
                amphipods[i, 5] = l[5]
                amphipods[i, 7] = l[7]
                amphipods[i, 9] = l[9]
    amphipods[3, 3] = "D"
    amphipods[3, 5] = "C"
    amphipods[3, 7] = "B"
    amphipods[3, 9] = "A"
    amphipods[4, 3] = "D"
    amphipods[4, 5] = "B"
    amphipods[4, 7] = "A"
    amphipods[4, 9] = "C"

    # print(amphipods)

    min_cost = 1000 * 14 * 16

    def dfs(amphipods: Amphipods, cost: int, indent=0) -> None:
        nonlocal min_cost
        # print(f'{indent=}')
        # print_amphipods(amphipods)
        if all_settled(amphipods):
            # print('  all_settled, cost=', cost)
            if cost < min_cost:
                print(f"update min_cost = {cost}")
                min_cost = cost
            return

        # try all simple move
        simple_move = False
        for c, ty in amphipods.items():
            ci, cj = c
            if ci == 1:
                targets = get_targets_1(amphipods, c, ty)
                if len(targets) == 1:
                    t = targets[0]
                    amphipods_1 = amphipods.copy()
                    do_move(amphipods_1, c, t)
                    new_cost = cost + calc_cost(c, t, ty)
                    simple_move = True
                    dfs(amphipods_1, new_cost, indent + 1)
            else:
                if r := can_move_u_path(amphipods, c):
                    amphipods_1 = amphipods.copy()
                    do_move(amphipods_1, c, r[0])
                    new_cost = cost + r[1]
                    simple_move = True
                    dfs(amphipods_1, new_cost, indent + 1)

        if not simple_move:
            for c, ty in amphipods.items():
                targets = get_targets_2(amphipods, c, ty)
                # if targets:
                # print(f'{targets=}')
                for t in targets:
                    # print(' ' * indent + f'try move {ty}: {c} -> {t}')
                    amphipods_1 = amphipods.copy()
                    do_move(amphipods_1, c, t)
                    new_cost = cost + calc_cost(c, t, ty)
                    dfs(amphipods_1, new_cost, indent + 1)

    dfs(amphipods, 0)
    print(min_cost)


def can_move_u_path(amphipods: Amphipods, c: Coord) -> tuple[Coord, int] | None:
    ci, cj = c
    if not 2 <= ci <= 5:
        return
    if (ci - 1, cj) in amphipods:
        return
    ty = amphipods[c]
    tj = type_target[ty]
    if cj == tj:
        return
    if any((1, j) in amphipods for j in range_exclusive(cj, tj)):
        return
    ti = 0
    for i in [5, 4, 3, 2]:
        tij = amphipods.get((i, tj))
        if tij == ty:
            continue
        if tij is None:
            ti = i
        break
    if ti != 0:
        cost = ((ci - 1) + abs(tj - cj) + (ti - 1)) * type_to_cost[ty]
        return ((ti, tj), cost)


def do_move(amphipods: Amphipods, c1: Coord, c2: Coord) -> None:
    amphipods[c2] = amphipods[c1]
    del amphipods[c1]


walls = [
    "#############",
    "#...........#",
    "###.#.#.#.###",
    "  #.#.#.#.#  ",
    "  #.#.#.#.#  ",
    "  #.#.#.#.#  ",
    "  #########  ",
]


def print_amphipods(amphipods: Amphipods) -> None:
    print("-" * 13)
    for i in range(7):
        for j in range(13):
            if walls[i][j] == ".":
                if a := amphipods.get((i, j)):
                    print(a, end="")
                else:
                    print(".", end="")
            else:
                print(walls[i][j], end="")
        print()


type_target = {
    "A": 3,
    "B": 5,
    "C": 7,
    "D": 9,
}


def get_targets_1(amphipods: Amphipods, c: Coord, ty: str) -> list[Coord]:
    ci, cj = c
    targets: list[Coord] = []
    if ci == 1:
        tj = type_target[ty]
        if all((1, j) not in amphipods for j in range_exclusive(cj, tj)):
            ti = 0
            for i in [5, 4, 3, 2]:
                tij = amphipods.get((i, tj))
                if tij == ty:
                    continue
                if tij is None:
                    ti = i
                break
            if ti != 0:
                targets.append((ti, tj))
    return targets


def range_exclusive(f: int, to: int):
    return range(f + 1, to) if to >= f else range(f - 1, to, -1)


def get_targets_2(amphipods: Amphipods, c: Coord, ty: str) -> list[Coord]:
    ci, cj = c
    if ci == 1:
        return []
    if (ci - 1, cj) in amphipods:
        return []
    tj = type_target[ty]
    if cj == tj and all(amphipods.get((i, tj)) == ty for i in range_exclusive(ci, 6)):
        return []
    targets: list[Coord] = []
    for j in range(cj + 1, 12):
        if j not in (3, 5, 7, 9):
            if (1, j) in amphipods:
                break
            targets.append((1, j))
    for j in range(cj - 1, 0, -1):
        if j not in (3, 5, 7, 9):
            if (1, j) in amphipods:
                break
            targets.append((1, j))
    return targets


type_to_cost = {
    "A": 1,
    "B": 10,
    "C": 100,
    "D": 1000,
}


def calc_cost(start: Coord, end: Coord, ty: str) -> int:
    return (abs(start[0] - end[0]) + abs(start[1] - end[1])) * type_to_cost[ty]


def all_settled(amphipods: Amphipods) -> bool:
    return all(2 <= c[0] <= 5 and c[1] == type_target[ty] for c, ty in amphipods.items())


if __name__ == "__main__":
    main()
