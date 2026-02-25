#!/usr/bin/env python3

from dataclasses import dataclass
import sys


@dataclass
class Inst:
    op: str
    args: list[str]


class Computer:
    def __init__(self, insts: list[Inst]) -> None:
        self.regs = {"a": 0, "b": 0}
        self.ip = 0
        self.insts: list[Inst] = insts

    def run_step(self):
        inst = self.insts[self.ip]
        r = inst.args[0]
        if inst.op == "hlf":
            self.regs[r] = self.regs[r] // 2
        elif inst.op == "tpl":
            self.regs[r] = self.regs[r] * 3
        elif inst.op == "inc":
            self.regs[r] = self.regs[r] + 1
        elif inst.op == "jmp":
            self.ip = self.ip + int(r) - 1
        elif inst.op == "jie":
            if self.regs[r] % 2 == 0:
                offset = int(inst.args[1])
                self.ip = self.ip + offset - 1
        elif inst.op == "jio":
            if self.regs[r] == 1:
                offset = int(inst.args[1])
                self.ip = self.ip + offset - 1
        self.ip += 1

    def run(self):
        while 0 <= self.ip < len(self.insts):
            self.run_step()


def main() -> None:
    inputFile = sys.argv[1]

    insts: list[Inst] = []
    with open(inputFile) as fin:
        for l in fin:
            l = l.strip()
            if not l:
                continue
            segs = [s.removesuffix(",") for s in l.split()]
            insts.append(Inst(segs[0], segs[1:]))

    # print_translate(insts)
    # return

    m = Computer(insts)
    m.run()
    print(f"ans1: a={m.regs['a']}, b={m.regs['b']}")

    m.regs['a'] = 1
    m.regs['b'] = 0
    m.ip = 0
    m.run()
    print(f"ans2: a={m.regs['a']}, b={m.regs['b']}")


def print_translate(insts: list[Inst]):
    for i, inst in enumerate(insts):
        lineno = i + 1
        print(f'{lineno:02} ', end='')
        r = inst.args[0]
        if inst.op == "hlf":
            print(f'{r} = {r} // 2')
        elif inst.op == "tpl":
            print(f'{r} = {r} * 3')
        elif inst.op == "inc":
            print(f'{r} = {r} + 1')
        elif inst.op == "jmp":
            print(f'jmp {lineno + int(r)}')
        elif inst.op == "jie":
            tgtno = lineno + int(int(inst.args[1]))
            print(f'if {r} % 2 == 0: jmp {tgtno}')
        elif inst.op == "jio":
            tgtno = lineno + int(int(inst.args[1]))
            print(f'if {r} == 1: jmp {tgtno}')

if __name__ == "__main__":
    main()
