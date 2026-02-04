#!/usr/bin/env python3

import sys


def main() -> None:
    inputFile = sys.argv[1]

    lines: list[str] = []
    with open(inputFile) as fin:
        for l in fin:
            l = l.strip()
            if not l:
                continue
            lines.append(l)

    s1 = sum(map(len, lines))
    s2 = sum(map(lambda l: len(eval(l)), lines))
    s3 = sum(map(lambda l: len(encode(l)), lines))
    print(f"{s1=}, {s2=}, {s3=}")
    print(f"{s1-s2=}, {s3-s1=}")


def encode(s: str) -> str:
    es = ['"']
    for c in s:
        if c == '"' or c == "\\":
            es.append("\\" + c)
        else:
            es.append(c)
    es.append('"')
    return "".join(es)


if __name__ == "__main__":
    main()
