from sys import stdin

pass2bin_dict = {
    'F': '0',
    'B': '1',
    'R': '1',
    'L': '0',
}

def pass2bin(p):
    return ''.join(pass2bin_dict[c] for c in p)

max_id = max(int(pass2bin(p.strip()), base=2) for p in stdin)

print(f"{max_id=}")
