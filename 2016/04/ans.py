#!/usr/bin/env python3

import sys
import re


reLine = re.compile(r"([a-z-]+)-(\d+)\[([a-z]+)\]")


def main() -> None:
    inputFile = sys.argv[1]

    ans1 = 0
    with open(inputFile) as fin:
        for l in fin:
            l = l.strip()
            if not l:
                continue
            m = reLine.match(l)
            assert m, l
            cname, sid, checksum = m[1], int(m[2]), m[3]
            cksm1 = gen_checksum(cname)
            # print(f'checksum of {cname} is {cksm1}')
            if cksm1 == checksum:
                ans1 += sid
                real_name = rot(cname, sid)
                if 'pole' in real_name:
                    print(f'ans2: {sid}')

    print(f'{ans1=}')

def gen_checksum(cname: str) -> str:
    letters = [ c for c in set(cname) if c.isalpha() ]
    letters.sort(key=lambda c: (-cname.count(c), c))
    return ''.join(letters)[:5]

def rot(s: str, n: int) -> str:
    return ''.join(chr((ord(c) - ord('a') + n) % 26 + ord('a')) if c != '-' else ' ' for c in s)

if __name__ == "__main__":
    main()
