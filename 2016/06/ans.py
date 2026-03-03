#!/usr/bin/env python3

import sys
from collections import Counter

def main() -> None:
    inputFile = sys.argv[1]

    input_message = []
    with open(inputFile) as fin:
        for l in fin:
            l = l.strip()
            if not l:
                continue
            input_message.append(l)

    cols = len(input_message[0])
    print('ans1', ''.join(Counter(l[k] for l in input_message).most_common(1)[0][0] for k in range(cols)))
    print('ans2', ''.join(Counter(l[k] for l in input_message).most_common()[-1][0] for k in range(cols)))


if __name__ == "__main__":
    main()
