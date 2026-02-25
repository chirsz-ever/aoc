#!/usr/bin/env python3

import sys
from itertools import combinations
from dataclasses import dataclass


@dataclass
class Item:
    cost: int = 0
    damage: int = 0
    armor: int = 0


@dataclass
class Player:
    hp: int = 0
    damage: int = 0
    armor: int = 0


weapons = [
    Item(8, 4, 0),
    Item(10, 5, 0),
    Item(25, 6, 0),
    Item(40, 7, 0),
    Item(74, 8, 0),
]


armors = [
    Item(0, 0, 0),
    Item(13, 0, 1),
    Item(31, 0, 2),
    Item(53, 0, 3),
    Item(75, 0, 4),
    Item(102, 0, 5),
]

rings = [
    Item(0, 0, 0),
    Item(0, 0, 0),
    Item(20, 0, 1),
    Item(25, 1, 0),
    Item(40, 0, 2),
    Item(50, 2, 0),
    Item(80, 0, 3),
    Item(100, 3, 0),
]


def main() -> None:
    inputFile = sys.argv[1]

    boss = Player()
    with open(inputFile) as fin:
        for l in fin:
            l = l.strip()
            if not l:
                continue
            p, v = l.split(": ")
            if p == "Hit Points":
                boss.hp = int(v)
            elif p == "Damage":
                boss.damage = int(v)
            elif p == "Armor":
                boss.armor = int(v)
            else:
                raise RuntimeError(f"unknown line: {l}")

    player = Player(100)
    min_cost = sum(i.cost for i in weapons + armors + rings)
    for w in weapons:
        for a in armors:
            for r1, r2 in combinations(rings, 2):
                items = [w, a, r1, r2]
                player.damage = sum(i.damage for i in items)
                player.armor = sum(i.armor for i in items)
                cost = sum(i.cost for i in items)
                if cost < min_cost and could_win(player, boss):
                    min_cost = cost
                    # print(f'{min_cost=} when choose {items}')
    print(f'{min_cost=}')
    
    max_cost = 0
    for w in weapons:
        for a in armors:
            for r1, r2 in combinations(rings, 2):
                items = [w, a, r1, r2]
                player.damage = sum(i.damage for i in items)
                player.armor = sum(i.armor for i in items)
                cost = sum(i.cost for i in items)
                if cost > max_cost and not could_win(player, boss):
                    max_cost = cost
                    # print(f'{min_cost=} when choose {items}')
    print(f'{max_cost=}')


def could_win(player: Player, boss: Player) -> bool:
    d1 = max(1, player.damage - boss.armor)
    d2 = max(1, boss.damage - player.armor)
    t1 = (boss.hp + d1 - 1) // d1
    t2 = (player.hp + d2 - 1) // d2
    return t1 <= t2

if __name__ == "__main__":
    main()
