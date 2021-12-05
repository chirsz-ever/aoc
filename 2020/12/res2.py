from sys import stdin
from math import *

instructions = []
for line in stdin:
    sline = line.strip()
    if len(sline) != 0:
        instructions.append((sline[0], int(sline[1:])))

#print(instructions)

x = 0
y = 0
wx = 10
wy = 1

for inst, arg in instructions:
    if inst == 'N':
        wy += arg
    elif inst == 'S':
        wy -= arg
    elif inst == 'W':
        wx -= arg
    elif inst == 'E':
        wx += arg
    elif inst == 'R':
        r = dist((wx, wy), (0, 0))
        d = atan2(wy, wx) - radians(arg)
        wx = round(r * cos(d))
        wy = round(r * sin(d))
    elif inst == 'L':
        r = dist((wx, wy), (0, 0))
        d = atan2(wy, wx) + radians(arg)
        wx = round(r * cos(d))
        wy = round(r * sin(d))
    elif inst == 'F':
        x += arg * wx
        y += arg * wy
    else:
        print(f'unknown instruction {inst:r}')
    # print(f'{(x, y)=}')
    # print(f'{(wx, wy)=}')

def mht(x, y):
    return abs(x) + abs(y)

print(f'{(x, y)=}')
print(f'{mht(x, y)=}')
