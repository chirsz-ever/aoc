#!/usr/bin/env python3

import sys
from dataclasses import dataclass


@dataclass
class Reindeer:
    name: str
    v1: int
    t1: int
    t2: int
    pos: int = 0
    points: int = 0


def main() -> None:
    inputFile = sys.argv[1]
    tuta_tempo = int(sys.argv[2]) if len(sys.argv) > 2 else 2503

    reindeers: list[Reindeer] = []
    with open(inputFile) as fin:
        for l in fin:
            l = l.strip()
            if not l:
                continue
            segs = l.split()
            name = segs[0]
            v1 = int(segs[3])
            t1 = int(segs[6])
            t2 = int(segs[13])
            reindeers.append(Reindeer(name, v1, t1, t2))

    # print(reindeers)
    for t in range(0, tuta_tempo):
        for r in reindeers:
            if t % (r.t1 + r.t2) < r.t1:
                r.pos += r.v1
        max_pos = max(r.pos for r in reindeers)
        for r in reindeers:
            if r.pos == max_pos:
                r.points += 1
    for r in reindeers:
        print(f"{r.name} get {r.points} points")
    max_points = max(r.points for r in reindeers)
    print(f"{max_points=}")


if __name__ == "__main__":
    main()
