#!/usr/bin/env python3

import sys
from ans1 import VM

def main() -> None:
    inputFile = sys.argv[1]

    instructions: list[int] = []
    vm = VM()
    with open(inputFile) as fin:
        lines = list(map(str.strip, fin))
        vm.A = int(lines[0].split(': ')[1])
        vm.B = int(lines[1].split(': ')[1])
        vm.C = int(lines[2].split(': ')[1])

        instructions = list(map(int, lines[4].split(': ')[1].split(',')))

    for ip in range(0, len(instructions), 2):
        print(dasm(instructions[ip], instructions[ip + 1]))
    # return

    subinsts = instructions[:-2]
    prefixes: list[list[int]] = []
    for i, inst in enumerate(instructions):
        prefixes.append([])
        for a in range(0, 2**10 - 1):
            vm.A = a
            out = []
            vm.run(subinsts, 0, out)
            if out[0] == inst:
                # print(f'{i}: {inst} <- {a}')
                prefixes[-1].append(a)

    choose: list[int] = [0] * len(prefixes)
    
    def find_num(i: int, j: int) -> tuple[bool, int]:
        choose[i] = j
        if i == 0:
            n = prefixes[-1][choose[-1]]
            for k in range(len(prefixes)-2, -1, -1):
                n = n * 8 + prefixes[k][choose[k]] % 8
            return True, n
        x = prefixes[i][j]
        for lj, lx in enumerate(prefixes[i-1]):
            if (x & 0b1111111) == (lx >> 3):
                # print(f'{x} {(i, j)} can match {lx} {(i-1, lj)}')
                found, n = find_num(i - 1, lj)
                if found:
                    return found, n
        return False, 0

    for lj in range(len(prefixes[-1])):
        found, n = find_num(len(prefixes) - 1, lj)
        if found:
            vm.A = n
            out = []
            vm.run(instructions, 0, out)
            print(n)
            assert out == instructions, out
            break

def dasm_combo(n: int) -> str:
    if 0 <= n <= 3:
        return str(n)
    elif n == 4:
        return 'A'
    elif n == 5:
        return 'B'
    elif n == 6:
        return 'C'
    else:
        raise RuntimeError(f'combo({n})')

def dasm(opcode: int, oprand: int) -> str:
    if opcode == 0:
        return f'A = A >> {dasm_combo(oprand)}'
    elif opcode == 1:
        return f'B = B ^ {oprand}'
    elif opcode == 2:
        return f'B = {dasm_combo(oprand)} % 8'
    elif opcode == 3:
        return f'JNZ A'
    elif opcode == 4:
        return f'B = B ^ C'
    elif opcode == 5:
        return f'OUT {dasm_combo(oprand)} % 8'
    elif opcode == 6:
        return f'B = A >> {dasm_combo(oprand)}'
    elif opcode == 7:
        return f'C = A >> {dasm_combo(oprand)}'
    else:
        raise RuntimeError(f'opcode = {opcode}')

if __name__ == '__main__':
    main()
