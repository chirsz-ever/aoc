#!/usr/bin/env python3

import sys
import hashlib

def main() -> None:
    door_id = sys.argv[1]
    index = 0
    pswd = [''] * 8
    picked = 0
    while picked < 8:
        hs = hashlib.md5((door_id + str(index)).encode()).hexdigest()
        if hs.startswith('00000'):
            pos = int(hs[5], 16)
            if 0 <= pos < 8 and pswd[pos] == '':
                pswd[pos] = hs[6]
                picked += 1
                print(index, hs)
        index += 1
    print(''.join(pswd))


if __name__ == "__main__":
    main()
