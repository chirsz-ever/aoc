#!/usr/bin/env python3

import sys
import hashlib

def main() -> None:
    door_id = sys.argv[1]
    index = 0
    pswd = ''
    while len(pswd) < 8:
        hs = hashlib.md5((door_id + str(index)).encode()).hexdigest()
        if hs.startswith('00000'):
            # print(index, hs)
            pswd += hs[5]
        index += 1
    print(pswd)


if __name__ == "__main__":
    main()
