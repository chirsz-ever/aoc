from sys import stdin

nums = set()
for line in stdin:
    nums.add(int(line))


for n in nums:
    if 2020-n in nums:
        print(f"{n}+{2020-n}=2020, prod={n*(2020-n)}")
