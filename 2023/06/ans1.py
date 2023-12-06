#!/usr/bin/env python3

import sys
import math

inputFile = 'input'
if len(sys.argv) >= 2:
    inputFile = sys.argv[1]

times: list[int] = []
records: list[int] = []
with open(inputFile) as fin:
    for l in fin:
        if len(times) == 0:
            times = [int(t) for t in l.split()[1:]]
        else:
            records = [int(t) for t in l.split()[1:]]

print(f'{times=}')
print(f'{records=}')

p = 1
for i in range(len(times)):
    t = times[i]
    r = records[i]
    d = t*t/4-r
    assert d >= 0
    t_min = int(math.floor(t*0.5-math.sqrt(d)+1))
    t_max = int(math.ceil(t*0.5+math.sqrt(d)-1))
    cnt = t_max - t_min + 1
    print(f'{i}: {t_min=} {t_max=} {cnt=}')
    p *= cnt

print(f"{p=}")
