from sys import stdin
from typing import TextIO, Dict, Tuple, Set
import re

Rule = Dict[str, int]
Graph = Dict[str, Set[str]]

def parse_rule(line: str) -> Tuple[str, Rule]:
    m1 = re.fullmatch(r'(.+?) bags contain(.+)', line)
    color = m1[1]
    subbags = m1[2]
    r = dict()
    for m in re.finditer(r'(\d+) (.+?) bags?[.,]', subbags):
        subcolor = m[2]
        count = int(m[1])
        r[subcolor] = count
    return (color, r)

def parse_rules(input_fd: TextIO) -> Dict[str, Rule]:
    return dict(parse_rule(str.strip(line)) for line in input_fd)

def r2g(rules: Dict[str, Rule]) -> Graph:
    g = dict()
    for v, ns in rules.items():
        for n in ns:
            g.setdefault(v, set()).add(n)
    return g

def reverse_edge(g: Graph) -> Graph:
    rg = dict()
    for v, ns in g.items():
        for n in ns:
            rg.setdefault(n, set()).add(v)
    return rg

def reachable(g: Graph, v: str) -> Set[str]:
    def step(vs: Set[str]) -> Set[str]:
        dr = set()
        for v in vs:
            dr.update(g.get(v, set()))
        dr -= r
        return dr
    r = g.get(v, set())
    dr = step(r)
    while len(dr) != 0:
        r.update(dr)
        dr = step(dr)
    return r

rules = parse_rules(stdin)

contained_by = reverse_edge(r2g(rules))

#print(f"{contained_by=}")

r = reachable(contained_by, 'shiny gold')

#print(f"{r=}")
print(f"{len(r)=}")
