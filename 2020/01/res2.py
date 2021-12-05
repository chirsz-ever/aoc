from sys import stdin
from itertools import permutations

nums = set()
for line in stdin:
    nums.add(int(line))

for m, n in permutations(nums, 2):
    o = 2020 - m - n
    if o in nums:
        print(f"{m} + {n} + {o} = 2020, prod={m*n*o}")
