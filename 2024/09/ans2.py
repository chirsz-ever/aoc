#!/usr/bin/env python3

from dataclasses import dataclass
import sys
from itertools import combinations

@dataclass
class Region:
    offset: int
    length: int
    value: int = 0

def main() -> None:
    inputFile = 'input'
    if len(sys.argv) >= 2:
        inputFile = sys.argv[1]

    data: list[int] = []
    with open(inputFile) as fin:
        data = [int(c) for c in fin.read().strip()]
    # print(data)

    spaces: list[Region] = []
    files: list[Region] = []
    offset = 0
    for i in range(0, len(data)):
        length = data[i]
        if length > 0:
            if i % 2 == 0:
                files.append(Region(offset, length, i//2))
            else:
                spaces.append(Region(offset, length))
            offset += length
    # print(f'{files=}')
    # print(f'{spaces=}')
    
    new_files: list[Region] = []

    for i in range(len(files) - 1, -1, -1):
        f = files[i]
        for j in range(len(spaces)):
            s = spaces[j]
            if s.offset >= f.offset:
                # print(f'keep {f} when meet {s}, spaces={spaces}')
                new_files.append(Region(f.offset, f.length, f.value))
                break
            if s.length >= f.length and s.value == 0:
                # print(f'move {f} to {s}')
                new_files.insert(j, Region(s.offset, f.length, f.value))
                s.offset += f.length
                s.length -= f.length
                break
        else:
            # print(f'keep {f}, spaces={spaces}')
            new_files.append(Region(f.offset, f.length, f.value))

    s = sum(sum((f.offset + i) * f.value for i in range(0, f.length)) for f in new_files)
    print(s)

if __name__ == '__main__':
    main()
