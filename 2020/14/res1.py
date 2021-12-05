from sys import stdin
from math import *
import re

set_mask = re.compile(r'mask = ([X01]{36})')
set_mem = re.compile(r'mem\[(\d+)\] = (\d+)')

def parse_line(line):
    if m := set_mem.match(line):
        return ('SETMEM', int(m[1]), int(m[2]))
    elif m := set_mask.match(line):
        mask = parse_mask(m[1])
        return ('SETMASK', mask)
    else:
        print(f'unknown command: {line:r}')

def parse_mask(msk):
    and_mask = int(''.join(map(lambda c: '0' if c.isdigit() else '1', msk)), 2)
    or_mask = int(''.join(map(lambda c: c if c.isdigit() else '0', msk)), 2)
    def app_msk(v):
        return (and_mask & v) | or_mask
    return app_msk

def apply_mask(mask, v):
    return mask(v)

instructions = []
for line in stdin:
    if (sline := line.strip()) != '':
        instructions.append(parse_line(sline))

mem = dict()
mask = lambda v: v

for inst in instructions:
    if inst[0] == 'SETMEM':
        _, addr, v = inst
        mem[addr] = apply_mask(mask, v)
    elif inst[0] == 'SETMASK':
        _, nmask = inst
        mask = nmask
    else:
        print(f'unknown command: {inst}')

print(f'{sum(mem.values())=}')
