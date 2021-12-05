from sys import stdin
from math import *

instructions = []
for line in stdin:
    sline = line.strip()
    if len(sline) != 0:
        instructions.append((sline[0], int(sline[1:])))

#print(instructions)

direction = (1, 0) # East
x = 0
y = 0

for inst, arg in instructions:
    if inst == 'N':
        y += arg
    elif inst == 'S':
        y -= arg
    elif inst == 'W':
        x -= arg
    elif inst == 'E':
        x += arg
    elif inst == 'R':
        r = atan2(direction[1], direction[0])
        r -= radians(arg)
        direction = (round(cos(r)), round(sin(r)))
    elif inst == 'L':
        r = atan2(direction[1], direction[0])
        r += radians(arg)
        direction = (round(cos(r)), round(sin(r)))
    elif inst == 'F':
        x += arg * direction[0]
        y += arg * direction[1]
    else:
        print(f'unknown instruction {inst:r}')
    #print(f'{(x, y)=}')

def mht(x, y):
    return abs(x) + abs(y)

print(f'{(x, y)=}')
print(f'{mht(x, y)=}')
