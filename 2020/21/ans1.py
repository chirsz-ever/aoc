from sys import stdin
from itertools import chain
import re

line_re = re.compile(r'(.+?)\(contains (.+?)\)')

def read_input(f):
    foods = []
    for line in map(str.strip, f):
        if line:
            m = line_re.match(line)
            ingredients = m.group(1).split()
            allergens = [w.strip() for w in m.group(2).split(',')]
            foods.append((ingredients, allergens))
    return foods

def thinkfood(foods):
    d = dict()
    for ingredients, allergens in foods:
        for a in allergens:
            if a in d.keys():
                d[a].intersection_update(ingredients)
            else:
                d[a] = set(ingredients)
    next_as = set(a for a in d.keys() if len(d[a]) == 1)
    while next_as:
        confirmed_igs = set(chain.from_iterable(d[a] for a in next_as))
        next_as = set()
        for a in d.keys():
            if len(d[a]) > 1:
                d[a].difference_update(confirmed_igs)
                if len(d[a]) == 1:
                    next_as.add(a)
    return d

def main():
    foods = read_input(stdin)
    a2ig = thinkfood(foods)
    confirmed_igs = set(chain.from_iterable(a2ig.values()))
    cnt = sum(1 for ig in chain.from_iterable(igs for igs, _ in foods) if ig not in confirmed_igs)
    
    print(f'{cnt=}')

    sorted_igs = ','.join(chain.from_iterable(a2ig[a] for a in sorted(a2ig.keys())))
    print(f'{sorted_igs=}')

if __name__ == '__main__':
    main()
