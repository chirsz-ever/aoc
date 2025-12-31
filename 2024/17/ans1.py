#!/usr/bin/env python3

import sys

class VM:
    def __init__(self) -> None:
        self.A: int = 0
        self.B: int = 0
        self.C: int = 0

    def combo(self, n: int) -> int:
        if 0 <= n <= 3:
            return n
        elif n == 4:
            return self.A
        elif n == 5:
            return self.B
        elif n == 6:
            return self.C
        else:
            raise RuntimeError(f'combo({n})')

    def run(self, instructions: list[int], ip: int, out: list[int]) -> None:
        while ip < len(instructions):
            opcode = instructions[ip]
            oprand = instructions[ip + 1]
            
            if opcode == 0:
                self.A >>= self.combo(oprand)
            elif opcode == 1:
                self.B ^= oprand
            elif opcode == 2:
                self.B = self.combo(oprand) % 8
            elif opcode == 3:
                if self.A != 0:
                    ip = oprand - 2
            elif opcode == 4:
                self.B ^= self.C
            elif opcode == 5:
                out.append(self.combo(oprand) % 8)
            elif opcode == 6:
                self.B = self.A >> self.combo(oprand)
            elif opcode == 7:
                self.C = self.A >> self.combo(oprand)
            else:
                raise RuntimeError(f'opcode = {opcode}')
            ip = ip + 2

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

    # print(vm)
    # print(instructions)
    out: list[int] = []

    vm.run(instructions, 0, out)
    print(','.join(map(str, out)))

def tests():
    vm = VM()
    vm.C = 9
    vm.run([2, 6], 0, [])
    assert vm.B == 1

    out = []
    vm.A = 10
    vm.run([5,0,5,1,5,4], 0, out)
    assert out == [0, 1, 2]

    out = []
    vm.A = 2024
    vm.run([0,1,5,4,3,0], 0, out)
    assert out == [4,2,5,6,7,7,7,7,3,1,0]
    assert vm.A == 0

    out = []
    vm.B = 29
    vm.run([1, 7], 0, out)
    assert vm.B == 26

    out = []
    vm.B = 2024
    vm.C = 43690
    vm.run([4, 0], 0, out)
    assert vm.B == 44354

if __name__ == '__main__':
    if sys.argv[1] == '--test':
        tests()
    else:
        main()
