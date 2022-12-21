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

def get_monkey(name: str) -> int:
    global monkeys
    mk = monkeys[name]
    if mk.n is None:
        a, op, b = mk.expr
        na = get_monkey(a)
        nb = get_monkey(b)
        n = int(eval(str(na) + op + str(nb)))
        mk.n = n
    return mk.n

print(get_monkey('root'))
