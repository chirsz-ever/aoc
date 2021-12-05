from sys import stdin
from typing import TextIO, Dict, Tuple, Set

def parse_line(line: str) -> Tuple[str, int]:
    t = line.split()
    return (t[0], int(t[1]))

instructions = [parse_line(sline) for line in stdin if len(sline:=line.strip()) != 0]

#print(instructions)

pc = 0
visited = [False] * len(instructions)
acc = 0

while pc < len(instructions):
    if visited[pc]:
        break
    else:
        visited[pc] = True
    op, arg = instructions[pc]
    if op == 'nop':
        pass
    elif op == 'acc':
        acc += arg
    elif op == 'jmp':
        pc += arg
        continue
    else:
        print(f'warning: unknown instruction {op!r}')
    pc += 1

print(f'{acc=}')
