#!/usr/bin/env python3

import sys


def main() -> None:
    inputFile = sys.argv[1]

    sizes = []
    with open(inputFile) as fin:
        for l in fin:
            l = l.strip()
            if l:
                w, h, l = map(int, l.split("x"))
                sizes.append((w, h, l))

    s = sum(2 * (w * h + l * w + h * l) + min(w * h, h * l, l * w) for w, h, l in sizes)
    print("ans1:", s)

    s = sum(2 * min(w + l, l + h, h + w) + w * h * l for w, h, l in sizes)
    print("ans2:", s)


if __name__ == "__main__":
    main()
