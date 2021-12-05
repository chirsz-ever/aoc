import re
import logging
import sys
from itertools import chain
from math import prod

property_name_re = re.compile(r'([^:]+):')
range_re = re.compile(r'(\d+)-(\d+)')

def parse_input(f):
    properties = dict()
    while len(line := f.readline().strip()) != 0:
        name = property_name_re.match(line)[1]
        ranges = [(int(m[1]), int(m[2])) for m in range_re.finditer(line)]
        properties[name] = ranges

    assert f.readline().strip() == "your ticket:"
    my_ticket = [int(w) for w in f.readline().strip().split(',')]

    f.readline()

    assert f.readline().strip() == "nearby tickets:"
    tickets = []
    while len(line := f.readline().strip()) != 0:
        tickets.append([int(w) for w in line.split(',')])

    return properties, my_ticket, tickets

def in_range(p, c):
    return any(l <= p <=h for (l, h) in c)

def is_valid_property(p, cs):
    return any(in_range(p, c) for c in cs)

def is_valid_ticket(tk, cs):
    return all(is_valid_property(p, cs) for p in tk)

def is_valid_pos(c, tickets, pos):
    return all(in_range(t[pos], c) for t in tickets)

def main():
    constraints, my_ticket, tickets = parse_input(sys.stdin)
    tickets.append(my_ticket)
    valid_tickets = [t for t in tickets if is_valid_ticket(t, constraints.values())]
    prop_pos = {p:list(range(len(constraints))) for p in constraints.keys()}
    for p in list(prop_pos.keys()):
        c = constraints[p]
        prop_pos[p] = [pos for pos in prop_pos[p] if is_valid_pos(c, valid_tickets, pos)]
    changed = True
    while changed:
        changed = False
        pos_settled = [ps[0] for ps in prop_pos.values() if len(ps) == 1]
        for p in [p for p in prop_pos.keys() if len(prop_pos[p]) != 1]:
            if any(pos in pos_settled for pos in prop_pos[p]):
                changed = True
                prop_pos[p] = [pos for pos in prop_pos[p] if pos not in pos_settled]
    print(f'{prop_pos=}')
    ans = 1
    for p in prop_pos.keys():
        if p.startswith('departure'):
            ans *= my_ticket[prop_pos[p][0]]
    print(f'{ans=}')

if __name__ == '__main__':
    main()
