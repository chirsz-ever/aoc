from sys import stdin

allfields = {"byr","iyr","eyr","hgt","hcl","ecl","pid","cid"}

def parseline(line):
    return [pair.split(':') for pair in line.split()]

def validfileds(keys):
    diff = allfields.symmetric_difference(set(keys))
    return len(diff) == 0 or diff == {'cid'}

passports = []
pp = dict()
for line in stdin:
    line = line.strip()
    if len(line) == 0:
        passports.append(pp)
        pp = dict()
    else:
        pp.update(parseline(line))
else:
    if len(pp) != 0:
        passports.append(pp)

cnt = sum(1 for pssprt in passports if validfileds(pssprt.keys()))

print(f"{cnt=}")
