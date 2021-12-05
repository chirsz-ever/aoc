from sys import stdin
import re

set_mask_syntax = re.compile(r'mask = ([X01]{36})')
set_mem_syntax = re.compile(r'mem\[(\d+)\] = (\d+)')

def parse_line(line):
    if m := set_mem_syntax.match(line):
        return ('SETMEM', int(m[1]), int(m[2]))
    elif m := set_mask_syntax.match(line):
        mask = parse_mask(m[1])
        return ('SETMASK', mask)
    else:
        print(f'unknown command: {line:r}')

def parse_mask(msk):
    return msk

def apply_mask(mask, v):
    return mask(v)

instructions = []
for line in stdin:
    if (sline := line.strip()) != '':
        instructions.append(parse_line(sline))

mem = dict()
mask = '0' * 36

def set_mem_i(mem, addr, mask, v, i):
    if i > 35:
        mem[addr] = v
        return
    if mask[i] == '0':
        set_mem_i(mem, addr, mask, v, i + 1)
    elif mask[i] == '1':
        naddr = addr | (1 << (35 - i))
        set_mem_i(mem, naddr, mask, v, i + 1)
    elif mask[i] == 'X':
        naddr = addr | (1 << (35 - i))
        set_mem_i(mem, naddr, mask, v, i + 1)
        naddr = addr & ((1 << 36) - 1 - (1 << (35 - i)))
        set_mem_i(mem, naddr, mask, v, i + 1)
    else:
        pass

def set_mem(mem, addr, mask, v):
    set_mem_i(mem, addr, mask, v, 0)

for inst in instructions:
    if inst[0] == 'SETMEM':
        _, addr, v = inst
        set_mem(mem, addr, mask, v)
    elif inst[0] == 'SETMASK':
        _, nmask = inst
        mask = nmask
    else:
        print(f'unknown command: {inst}')

print(f'{sum(mem.values())=}')
