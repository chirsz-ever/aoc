#!/usr/bin/env python3

from functools import cache
import sys
from dataclasses import dataclass


@dataclass
class Gate:
    op: str
    output: str
    inputs: list[str]


def main() -> None:
    inputFile = sys.argv[1]

    gates: dict[str, Gate] = {}
    with open(inputFile) as fin:
        for l in fin:
            l = l.strip()
            if not l:
                continue
            segs = l.split()
            if len(segs) == 3:
                g = Gate('CONST', segs[-1], [segs[0]])
            elif len(segs) == 4:
                assert segs[0] == 'NOT', l
                g = Gate('NOT', segs[-1], [segs[1]])
            elif len(segs) == 5:
                g = Gate(segs[1], segs[-1], [segs[0], segs[2]])
            else:
                raise RuntimeError(f'unknown gate: {l}')
            gates[g.output] = g


    @cache
    def eval_gate(o: str) -> int:
        if o.isdigit():
            return int(o)
        # print(f'try eval {o}')
        g = gates[o]
        if g.op == 'CONST':
            return eval_gate(g.inputs[0])
        elif g.op == 'AND':
            x = eval_gate(g.inputs[0])
            y = eval_gate(g.inputs[1])
            return x & y
        elif g.op == 'OR':
            x = eval_gate(g.inputs[0])
            y = eval_gate(g.inputs[1])
            return x | y
        elif g.op == 'LSHIFT':
            x = eval_gate(g.inputs[0])
            y = eval_gate(g.inputs[1])
            return x << y
        elif g.op == 'RSHIFT':
            x = eval_gate(g.inputs[0])
            y = eval_gate(g.inputs[1])
            return x >> y
        elif g.op == 'NOT':
            x = eval_gate(g.inputs[0])
            return ~x
        else:
            raise RuntimeError(f'unknown op {g.op}')

    out_a = eval_gate('a')
    print('ans1:', out_a)

    gates['b'] = Gate('CONST', 'b', [str(out_a)])
    eval_gate.cache_clear()
    out_a = eval_gate('a')
    print('ans2:', out_a)

if __name__ == "__main__":
    main()
