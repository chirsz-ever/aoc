#!/usr/bin/env python3

import sys
import re
from typing import Optional

inputFile = 'input'
if len(sys.argv) >= 2:
    inputFile = sys.argv[1]

reLine1 = re.compile(r'(\w+): (-?\d+)')
reLine2 = re.compile(r'(\w+): (\w+) (.) (\w+)')

class Monkey:
    def __init__(self) -> None:
        self.n: Optional[int] = None
        self.expr = ('', '', '')

def read_input(fname) -> dict[str, Monkey]:
    monkeys: dict[str, Monkey] = dict()
    with open(fname) as fin:
        for l in fin:
            mk = Monkey()
            if m := reLine1.match(l):
                name = m[1]
                mk.n = int(m[2])
            elif m := reLine2.match(l):
                name = m[1]
                mk.expr = (m[2], m[3], m[4])
            else:
                raise RuntimeError(l)
            monkeys[name] = mk
    return monkeys

monkeys = read_input(inputFile)

def eval_with(name: str, humn: int) -> int:
    if name == 'humn':
        return humn
    mk = monkeys[name]
    if mk.n is None:
        a, op, b = mk.expr
        na = eval_with(a, humn)
        nb = eval_with(b, humn)
        if name == 'root':
            op = '-'
        n = eval(str(na) + op + str(nb))
        # print(f'{na}{op}{nb} = {n}')
        return n
    else:
        return mk.n

r = 10000000000000
l = -r

nl = eval_with('root', l)
nr = eval_with('root', r)

assert nl * nr < 0, f'{nl=}, {nr=}'

# print(nl)
# print(nr)

while l < r:
    if nl == 0:
        print(l)
        break
    elif nr == 0:
        print(r)
        break
    assert nl * nr < 0, f'{nl=}, {nr=}'
    m = (l + r) // 2
    nm = eval_with('root', m)
    if nm == 0:
        print(m)
        break
    elif nm * nl > 0:
        l = m
    else:
        r = m

