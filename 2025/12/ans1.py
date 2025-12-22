#!/usr/bin/env python3

from dataclasses import dataclass
import sys

Shape = list[str]

@dataclass
class Region:
    width: int
    height: int
    require_shapes: list[int]

    def __repr__(self) -> str:
        return f'{self.width}*{self.height}: {self.require_shapes}'

def main() -> None:
    inputFile = 'input'
    if len(sys.argv) >= 2:
        inputFile = sys.argv[1]

    shapes: list[Shape] = []
    regions: list[Region] = []
    with open(inputFile) as fin:
        for l in fin:
            segs = l.strip().split()
            if len(segs) == 0:
                continue
            seg0 = segs[0]
            if len(segs) == 1 and seg0[-1] == ':':
                assert int(seg0[:-1]) == len(shapes)
                shapes.append([])
            elif len(segs) == 1:
                shapes[-1].append(seg0)
            else:
                assert seg0[-1] == ':'
                w, h = map(int, seg0[:-1].split('x'))
                requires = list(map(int, segs[1:]))
                regions.append(Region(w, h, requires))

    present_count = [sum(sum(int(c == '#') for c in row) for row in s) for s in shapes]
    print(f'{present_count=}')
    s = 0
    for r in regions:
        if r.width * r.height >= sum(r.require_shapes[i] * present_count[i] for i in range(len(shapes))):
            s += 1
    print(s)

if __name__ == '__main__':
    main()
