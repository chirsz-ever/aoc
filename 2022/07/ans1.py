#!/usr/bin/env python3

import sys
import re

inputFile = 'input'
if len(sys.argv) >= 2:
    inputFile = sys.argv[1]

reCmdCd = re.compile(r'\$ cd (\S+)')
reCmdLs = re.compile(r'\$ ls')
reDir = re.compile(r'dir (\S+)')
reFile = re.compile(r'(\d+) (\S+)')


def addDir(fs, cwds, newd):
    cwd = fs
    for d in cwds:
        cwd = cwd.setdefault(d, {})
    cwd.setdefault(newd, {})


def addFile(fs, cwds, name, size):
    cwd = fs
    for d in cwds:
        cwd = cwd.setdefault(d, {})
    cwd[name] = size


def parseFs(fs, fin, cwds):
    l = fin.readline().strip()
    if not l:
        return
    if m := reCmdCd.match(l):
        d = m[1]
        if d == "..":
            cwds.pop()
        elif d == "/":
            cwds.clear()
        else:
            cwds.append(d)
    elif m := reCmdLs.match(l):
        # always ls cwd
        pass
    elif m := reDir.match(l):
        d = m[1]
        addDir(fs, cwds, d)
    elif m := reFile.match(l):
        size, name = m.group(1, 2)
        addFile(fs, cwds, name, int(size))
    else:
        print(f"error: {l}")
        exit(1)
    parseFs(fs, fin, cwds)


fs = {}
with open(inputFile) as fin:
    parseFs(fs, fin, [])

# print(fs)

s100000 = 0
sizes = []
def sumdir(fs: dict):
    global s100000
    s = 0
    for k, v in fs.items():
        if isinstance(v, dict):
            s += sumdir(v)
        else:
            s += v
    if s <= 100000:
        s100000 += s
    sizes.append(s)
    return s

total_size = sumdir(fs)
need_delete = total_size - (70000000 - 30000000)
sizes.sort()

print(s100000)

for i, s in enumerate(sizes):
    if s >= need_delete:
        print(s)
        break
