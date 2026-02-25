#!/usr/bin/env python3

import sys
from dataclasses import dataclass, field
import copy
from typing import Protocol
import heapq


class Spell(Protocol):
    def can_play(self, state: GameState) -> bool:
        return True

    def play(self, state: GameState) -> None:
        pass


@dataclass
class Player:
    hp: int = 50
    mana: int = 500


@dataclass
class Boss:
    hp: int = 0
    damage: int = 0
    armor: int = 0


@dataclass(order=True)
class GameState:
    player: Player = field(compare=False)
    boss: Boss = field(compare=False)
    turn: int = field(compare=False, default=0)
    cost: int = 0
    effect_shield: int = field(compare=False, default=0)
    effect_poison: int = field(compare=False, default=0)
    effect_recharge: int = field(compare=False, default=0)


class Missile:
    cost = 53

    def can_play(self, state: GameState) -> bool:
        return state.player.mana >= self.cost

    def play(self, state: GameState) -> None:
        state.player.mana -= self.cost
        state.cost += self.cost
        state.boss.hp -= 4


class Drain:
    cost = 73

    def can_play(self, state: GameState) -> bool:
        return state.player.mana >= self.cost

    def play(self, state: GameState) -> None:
        state.player.mana -= self.cost
        state.cost += self.cost
        state.boss.hp -= 2
        state.player.hp += 2


class Shield:
    cost = 113

    def can_play(self, state: GameState) -> bool:
        return state.player.mana >= self.cost and state.effect_shield == 0

    def play(self, state: GameState) -> None:
        state.player.mana -= self.cost
        state.cost += self.cost
        state.effect_shield = 6


class Poison:
    cost = 173

    def can_play(self, state: GameState) -> bool:
        return state.player.mana >= self.cost and state.effect_poison == 0

    def play(self, state: GameState) -> None:
        state.player.mana -= self.cost
        state.cost += self.cost
        state.effect_poison = 6


class Recharge:
    cost = 229

    def can_play(self, state: GameState) -> bool:
        return state.player.mana >= self.cost and state.effect_recharge == 0

    def play(self, state: GameState) -> None:
        state.player.mana -= self.cost
        state.cost += self.cost
        state.effect_recharge = 5


spells: list[Spell] = [
    Missile(),
    Drain(),
    Shield(),
    Poison(),
    Recharge(),
]


def main() -> None:
    inputFile = sys.argv[1]

    boss = Boss()
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

    ans(boss, False)
    ans(boss, True)


def ans(boss_stats: Boss, is_ans2: bool):
    # BFS
    queue = [GameState(Player(), copy.deepcopy(boss_stats))]
    while len(queue) > 0:
        state = heapq.heappop(queue)

        if state.boss.hp <= 0:
            print(state.cost)
            return

        # player turn
        if is_ans2:
            state.player.hp -= 1
            if state.player.hp <= 0:
                # print('player lose')
                continue
        run_game_turn_start(state)
        if state.boss.hp <= 0:
            print(state.cost)
            return

        for spell in spells:
            if spell.can_play(state):
                new_state = copy.deepcopy(state)
                spell.play(new_state)
                if new_state.boss.hp <= 0:
                    heapq.heappush(queue, new_state)
                    continue

                # boss turn
                run_game_turn_start(new_state)
                if new_state.boss.hp <= 0:
                    print(new_state.cost)
                    return
                player_armor = 7 if new_state.effect_shield > 0 else 0
                new_state.player.hp -= max(1, new_state.boss.damage - player_armor)
                if new_state.player.hp > 0:
                    heapq.heappush(queue, new_state)
                else:
                    # print('player lose')
                    pass


def run_game_turn_start(state: GameState) -> None:
    if state.effect_shield > 0:
        state.effect_shield -= 1

    if state.effect_poison > 0:
        state.boss.hp -= 3
        state.effect_poison -= 1

    if state.effect_recharge > 0:
        state.player.mana += 101
        state.effect_recharge -= 1


if __name__ == "__main__":
    main()
