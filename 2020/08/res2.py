from sys import stdin
from typing import Tuple, List, Optional

def parse_line(line: str) -> Tuple[str, int]:
    t = line.split()
    return (t[0], int(t[1]))

instructions = [parse_line(sline) for line in stdin if len(sline:=line.strip()) != 0]

#print(instructions) 


def try_run(pc: int, acc: int, visited: List[bool]) -> Optional[int]:
    op, arg = instructions[pc]
    if op == 'nop':
        pc += arg
    elif op == 'jmp':
        pc += 1
    else:
        pass
    while pc < len(instructions):
        if visited[pc]:
            return None
        op, arg = instructions[pc]
        if op == 'acc':
            acc += arg
        elif op == 'nop':
            pass
        elif op == 'jmp':
            pc += arg
            continue
        else:
            print(f'warning: unknown instruction {op!r}')
        visited[pc] = True
        pc += 1
    else:
        return acc


def test_run() -> Optional[int]:
    pc = 0
    acc = 0
    visited = [False] * len(instructions)
    while pc < len(instructions):
        if visited[pc]:
            return None
        op, arg = instructions[pc]
        if op == 'acc':
            acc += arg
        elif op == 'nop':
            v = try_run(pc, acc, visited.copy())
            if v is not None:
                return v
        elif op == 'jmp':
            v = try_run(pc, acc, visited.copy())
            if v is not None:
                return v
            else:
                pc += arg
                continue
        else:
            print(f'warning: unknown instruction {op!r}')
        visited[pc] = True
        pc += 1
    else:
        return acc

acc = test_run()

print(f'{acc=}')
