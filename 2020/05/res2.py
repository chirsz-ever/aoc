from sys import stdin

pass2bin_dict = {
    'F': '0',
    'B': '1',
    'R': '1',
    'L': '0',
}

def pass2bin(p):
    return ''.join(pass2bin_dict[c] for c in p)

ids = sorted(int(pass2bin(p.strip()), base=2) for p in stdin)

last_i = None
for i in ids:
    if last_i is not None and i - last_i == 2:
        my_id = i - 1
        break
    last_i = i


print(f"{my_id=}")
