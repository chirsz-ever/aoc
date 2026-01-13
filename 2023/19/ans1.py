#!/usr/bin/env python3

import sys
from dataclasses import dataclass
import re

@dataclass
class Rule:
    op: str
    category: str
    value: int
    dest: str

@dataclass
class Workflow:
    rules: list[Rule]
    final: str

@dataclass
class Part:
    x: int
    m: int
    a: int
    s: int

def main() -> None:
    inputFile = sys.argv[1]

    workflows: dict[str, Workflow] = {}
    parts: list[Part] = []
    with open(inputFile) as fin:
        for l in fin:
            l = l.strip()
            if not l:
                continue
            if l.startswith('{'):
                parts.append(parse_part(l.strip()))
            else:
                parse_workflow(workflows, l)

    # print(workflows)
    # print(parts)

    accepted_parts = [ p for p in parts if run_workflows(p, workflows) == 'A' ]

    s = sum(p.x + p.m + p.a + p.s for p in accepted_parts)
    print(s)

def run_workflows(p: Part, workflows: dict[str, Workflow]) -> str:
    w = 'in'
    while w not in 'RA':
        wf = workflows[w]
        for r in wf.rules:
            if r.op == '<':
                if p.__dict__[r.category] < r.value:
                    w = r.dest
                    break
            else:
                assert r.op == '>', r.op
                if p.__dict__[r.category] > r.value:
                    w = r.dest
                    break
        else:
            w = wf.final
    return w

rePart = re.compile(r'\{x=(\d+),m=(\d+),a=(\d+),s=(\d+)\}')
def parse_part(l: str) -> Part:
    matches = rePart.fullmatch(l)
    assert matches, l
    x, m, a, s = map(int, (matches[k] for k in range(1, 5)))
    return Part(x, m, a, s)

reRule = re.compile(r'([xmas])([><])(\d+):(\w+)')
def parse_workflow(workflows: dict[str, Workflow], l: str) -> None:
    i = l.find('{')
    name = l[:i]
    rule_strs = l[i+1:-1].split(',')
    rules = []
    for r in rule_strs[:-1]:
        m = reRule.fullmatch(r)
        assert m, r
        rules.append(Rule(m[2], m[1], int(m[3]), m[4]))
    workflows[name] = Workflow(rules, rule_strs[-1])

if __name__ == '__main__':
    main()
