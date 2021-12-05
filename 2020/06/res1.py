from sys import stdin

def count_options(grp):
    options = set()
    for p in grp:
        options.update(p)
    return len(options)

groups = []
grp = []
for line in stdin:
    line = line.strip()
    if len(line) == 0:
        groups.append(grp)
        grp = []
    else:
        grp.append(line)
else:
    if len(grp) != 0:
        groups.append(grp)

cnt = sum(count_options(grp) for grp in groups)

print(f"{cnt=}")
