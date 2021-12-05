from sys import stdin
import re

def parseline(line):
    return [pair.split(':') for pair in line.split()]

allfields = {"byr","iyr","eyr","hgt","hcl","ecl","pid","cid"}

eye_colors = ["amb", "blu", "brn", "gry", "grn", "hzl", "oth"]

def check_year(yr, min, max):
    if re.fullmatch(r'\d{4}', yr):
        y = int(yr)
        return min <= y <= max
    return False

def check_height(hgt):
    if match := re.fullmatch(r'(\d+)(cm|in)', hgt):
        l = int(match.group(1))
        unit = match.group(2)
        if unit == 'cm':
            return 150 <= l <= 193
        elif unit == 'in':
            return 59 <= l <= 76
    return False


field_checkers = {
    "byr": lambda yr: check_year(yr, 1920, 2002),
    "iyr": lambda yr: check_year(yr, 2010, 2020),
    "eyr": lambda yr: check_year(yr, 2020, 2030),
    "hgt": check_height,
    "hcl": lambda hcl: bool(re.fullmatch(r'#[0-9a-f]{6}', hcl)),
    "ecl": lambda ecl: ecl in eye_colors,
    "pid": lambda pid: bool(re.fullmatch(r'\d{9}', pid)),
    "cid": lambda _: True,
}

def check_filed(field, value):
    return field_checkers.get(field, lambda _:True)(value)

def valid_passport(pssprt):
    diff = allfields - set(pssprt.keys())
    if not (len(diff) == 0 or diff == {'cid'}):
        return False
    return all(check_filed(field, value) for field in allfields if (value := pssprt.get(field)))

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

cnt = sum(1 for pssprt in passports if valid_passport(pssprt))

print(f"{cnt=}")
