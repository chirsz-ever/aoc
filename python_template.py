#!/usr/bin/env python3

import sys

def main() -> None:
    inputFile = 'input'
    if len(sys.argv) >= 2:
        inputFile = sys.argv[1]

    with open(inputFile) as fin:
        for l in fin:
            l = l.strip()
            pass

if __name__ == '__main__':
    main()
