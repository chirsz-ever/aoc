#!/usr/bin/env python3

import sys

def main() -> None:
    inputFile = 'input'
    if len(sys.argv) >= 2:
        inputFile = sys.argv[1]
    
    ls = []
    rs = []

    with open(inputFile) as fin:
        for l in fin:
            l = l.strip()
            if l:
                l, r = l.split()
                ls.append(int(l))
                rs.append(int(r))

    ls.sort()
    rs.sort()
    total_distance = sum(abs(l - r) for l, r in zip(ls, rs))
    print(total_distance)

if __name__ == '__main__':
    main()
