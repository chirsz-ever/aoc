import re
import logging
import sys
from itertools import chain

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

def in_range(p, r):
    return any(l <= p <=h for (l, h) in r)

def is_valid(p, rs):
    return any(in_range(p, r) for r in rs)

def main():
    propertie_ranges, my_ticket, tickets = parse_input(sys.stdin)
    rate = 0
    for p in chain(*tickets):
        if not is_valid(p, propertie_ranges.values()):
            rate += p
    print(f'{rate=}')

if __name__ == '__main__':
    main()
