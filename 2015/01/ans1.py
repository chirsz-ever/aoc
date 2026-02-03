#!/usr/bin/env python3

import sys

def main() -> None:
    inputFile = sys.argv[1]
    with open(inputFile) as fin:
        content = fin.read().strip()
    s = content.count('(') - content.count(')')
    print(s)


if __name__ == "__main__":
    main()
