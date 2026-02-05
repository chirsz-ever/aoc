#!/usr/bin/env python3

import sys
from dataclasses import dataclass


@dataclass
class Reindeer:
    name: str
    v1: int
    t1: int
    t2: int


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
    max_dist = 0
    for r in reindeers:
        cycle_t = r.t1 + r.t2
        cycle_dist = r.v1 * r.t1
        tuta_dist = (
            tuta_tempo // cycle_t * cycle_dist + (tuta_tempo % cycle_t if tuta_tempo % cycle_t <= r.t1 else r.t1) * r.v1
        )
        print(f"{r.name} is at {tuta_dist} km")
        if tuta_dist > max_dist:
            max_dist = tuta_dist
    print(f"{max_dist=}")


if __name__ == "__main__":
    main()
