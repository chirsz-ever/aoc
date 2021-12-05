from sys import stdin
from typing import TextIO, Dict, Tuple, Set
from functools import lru_cache 
import re

Rule = Dict[str, int]
Graph = Dict[str, Set[str]]

def parse_rule(line: str) -> Tuple[str, Rule]:
    m1 = re.fullmatch(r'(.+?) bags contain(.+)', line)
    if m1 is None:
        raise RuntimeError('m1 is None')
    color = m1[1]
    subbags = m1[2]
    r: Rule = dict()
    for m in re.finditer(r'(\d+) (.+?) bags?[.,]', subbags):
        subcolor = m[2]
        count = int(m[1])
        r[subcolor] = count
    return (color, r)

def parse_rules(input_fd: TextIO) -> Dict[str, Rule]:
    return dict(parse_rule(str.strip(line)) for line in input_fd)

def r2g(rules: Dict[str, Rule]) -> Graph:
    g: Graph = dict()
    for v, ns in rules.items():
        for n in ns:
            g.setdefault(v, set()).add(n)
    return g

@lru_cache(maxsize=1024)
def sum_bags(color: str) -> int:
    r = rules.get(color, {})
    bags = sum((sum_bags(cl) + 1) * cnt for cl, cnt in r.items())
    return bags

rules = parse_rules(stdin)

#print(f"{contained_by=}")

bags = sum_bags('shiny gold')

#print(f"{r=}")
print(f"{bags=}")
