#!/usr/bin/env python3

import sys
from collections import Counter

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

    rs2 = Counter(rs)
    total_distance = sum(l * rs2[l] for l in ls)
    print(total_distance)

if __name__ == '__main__':
    main()
