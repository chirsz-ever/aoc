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

@dataclass
class PartLimit:
    x: tuple[int, int]
    m: tuple[int, int]
    a: tuple[int, int]
    s: tuple[int, int]

def main() -> None:
    inputFile = sys.argv[1]

    workflows: dict[str, Workflow] = {}
    # parts: list[Part] = []
    with open(inputFile) as fin:
        for l in fin:
            l = l.strip()
            if not l:
                continue
            if l.startswith('{'):
                # parts.append(parse_part(l.strip()))
                pass
            else:
                parse_workflow(workflows, l)

    # pre: dict[str, set[str]] = {}
    # stack = [ 'in' ]
    # while len(stack) > 0:
    #     w = stack.pop()
    #     wf = workflows[w]
    #     for r in wf.rules:
    #         pre.setdefault(r.dest, set()).add(w)
    #         if r.dest not in 'RA':
    #             stack.append(r.dest)
    #         pre.setdefault(wf.final, set()).add(w)
    #         if wf.final not in 'RA':
    #             stack.append(wf.final)
    # print(pre)

    combinations = 0
    def visit(name: str, limit: PartLimit) -> None:
        nonlocal combinations
        # print(f'visit({name}, {limit})')
        if name == 'R':
            return
        if name == 'A':
            combinations += sum_limit(limit)
            return
        wf = workflows[name]
        l = PartLimit(limit.x, limit.m, limit.a, limit.s)
        for r in wf.rules:
            c = check_rule_with_limit(r, l)
            if c == True:
                visit(r.dest, l)
            elif c == False:
                continue
            else:
                m = add_limit_to_pass(l, r)
                if m:
                    visit(r.dest, m)
                l = add_limit_to_reject(l, r)
                if l is None:
                    break
        if l:
            visit(wf.final, l)

    visit('in', PartLimit((1, 4000), (1, 4000), (1, 4000), (1, 4000)))
    print(combinations)

def check_rule_with_limit(r: Rule, l: PartLimit) -> bool | None:
    limit_min, limit_max = l.__dict__[r.category]
    if r.op == '<':
        if limit_max < r.value: return True
        if limit_min >= r.value: return False
        return None
    elif r.op == '>':
        if limit_min > r.value: return True
        if limit_max <= r.value: return False
        return None

def add_limit_to_pass(l: PartLimit, r: Rule) -> PartLimit | None:
    limit_min, limit_max = l.__dict__[r.category]
    if r.op == '<':
        limit_max = r.value - 1
    elif r.op == '>':
        limit_min = r.value + 1
    if limit_min > limit_max:
        return None
    m = PartLimit(l.x, l.m, l.a, l.s)
    m.__dict__[r.category] = (limit_min, limit_max)
    return m

def add_limit_to_reject(l: PartLimit, r: Rule) -> PartLimit | None:
    limit_min, limit_max = l.__dict__[r.category]
    if r.op == '<':
        limit_min = r.value
    elif r.op == '>':
        limit_max = r.value
    if limit_min > limit_max:
        return None
    m = PartLimit(l.x, l.m, l.a, l.s)
    m.__dict__[r.category] = (limit_min, limit_max)
    return m

def sum_limit(l: PartLimit) -> int:
    return (l.x[1] - l.x[0] + 1) * (l.m[1] - l.m[0] + 1) * (l.a[1] - l.a[0] + 1) * (l.s[1] - l.s[0] + 1)

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
