#!/usr/bin/env python3

import sys
import hashlib


def main() -> None:
    content = sys.argv[1]
    zerolen = int(sys.argv[2]) if len(sys.argv) > 2 else 5
    prefix_zero = '0' * zerolen

    n = 0
    while True:
        s = content + str(n)
        h = hashlib.md5(s.encode()).hexdigest()
        if h.startswith(prefix_zero):
            break
        n += 1

    print('ans1:', n)
    print(f'md5("{s}") = {h}')

if __name__ == "__main__":
    main()
