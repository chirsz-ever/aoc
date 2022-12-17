#!/usr/bin/env python3

import sys
import re

inputFile = 'input'
if len(sys.argv) >= 2:
    inputFile = sys.argv[1]


class Monkey:
    def __init__(self):
        self.items: list[int] = []
        self.operation: str = ""
        self.test_factor: int = 0
        self.on_test_true: int = 0
        self.on_test_false: int = 0

    def __str__(self):
        return f"Monky {{ items: {self.items}, operation: \"{self.operation}\", factor: {self.test_factor}, on_true: {self.on_test_true}, on_false: {self.on_test_false}}}"

reMonkeyN = re.compile(r"Monkey (\d+):")
reItems = re.compile(r"Starting items: (.*)")
reOperation = re.compile(r"Operation: new = (.*)");
reTest = re.compile(r"Test: divisible by (\d+)")
reTestTrue = re.compile(r"If true: throw to monkey (\d+)")
reTestFalse = re.compile(r"If false: throw to monkey (\d+)")

def read_monkey(fin, n) -> Monkey | None:
    l: str = fin.readline().strip()
    if not l:
        l = fin.readline().strip()
    if not l:
        return None
    mk = Monkey()
    m = reMonkeyN.match(l)
    assert m, f"fail to read \"{l}\""
    assert int(m[1]) == n

    l = fin.readline().strip()
    m = reItems.match(l)
    assert m, f"fail to read \"{l}\""
    mk.items = [int(i) for i in m[1].split(', ')]

    l = fin.readline().strip()
    m = reOperation.match(l)
    assert m, f"fail to read \"{l}\""
    mk.operation = m[1]

    l = fin.readline().strip()
    m = reTest.match(l)
    assert m, f"fail to read \"{l}\""
    mk.test_factor = int(m[1])

    l = fin.readline().strip()
    m = reTestTrue.match(l)
    assert m, f"fail to read \"{l}\""
    mk.on_test_true = int(m[1])

    l = fin.readline().strip()
    m = reTestFalse.match(l)
    assert m, f"fail to read \"{l}\""
    mk.on_test_false = int(m[1])

    return mk

monkeys = []

with open(inputFile) as fin:
    n = 0
    while mk := read_monkey(fin, n):
        monkeys.append(mk)
        n += 1

# print(list(map(str, monkeys)))

def do_operation(mk: Monkey, old: int) -> int:
    return eval(mk.operation)

inspect_stat = [0 for _ in monkeys]

for r in range(20):
    for i, mk in enumerate(monkeys):
        # print(f"Monkey {i}:")
        for it in mk.items:
            # print(f"  inspect item {it}")
            lvl = do_operation(mk, it)
            # print(f"    {it} -> {lvl}")
            # print(f"    {lvl} -> {lvl // 3}")
            lvl = lvl // 3
            # print(f"    {lvl} % {mk.test_factor} == {lvl % mk.test_factor}")
            divisible = lvl % mk.test_factor == 0
            if divisible:
                monkeys[mk.on_test_true].items.append(lvl)
            else:
                monkeys[mk.on_test_false].items.append(lvl)
            inspect_stat[i] += 1
        mk.items.clear()
    # print(f"after round {r +1}:")
    # for mk in monkeys:
    #     print(mk.items)
    # print()

print(f"{inspect_stat=}")
stat = sorted(inspect_stat)
print(stat[-1] * stat[-2])
