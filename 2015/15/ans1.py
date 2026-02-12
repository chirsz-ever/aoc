#!/usr/bin/env python3

import sys


def main() -> None:
    inputFile = sys.argv[1]

    ingredients: list[list[int]] = []
    names: list[str] = []
    with open(inputFile) as fin:
        for l in fin:
            l = l.strip()
            if not l:
                continue
            segs = l.split()
            names.append(segs[0][:-1])
            ingredients.append(
                [int(segs[2][:-1]), int(segs[4][:-1]), int(segs[6][:-1]), int(segs[8][:-1]), int(segs[10])]
            )
    # print(names)
    # print(ingredients)

    nums = [0] * len(ingredients)
    max_score = 0

    def step(i: int) -> None:
        nonlocal max_score
        if i == len(nums) - 1:
            nums[i] = 100 - sum(nums[:-1])
            score = calc_score(ingredients, nums)
            if score > max_score:
                max_score = score
                # print(f'update {max_score=}, {nums=}')
            return

        for n in range(0, 100 - sum(nums[:i]) + 1):
            nums[i] = n
            step(i + 1)
    step(0)
    print(max_score)

def calc_score(ingredients: list[list[int]], nums: list[int]) -> int:
    s = 1
    # for j in range(len(ingredients[0])):
    for j in range(4):
        p = sum(nums[i] * ingredients[i][j] for i in range(len(nums)))
        if p <= 0:
            return 0
        s *= p
    return s

if __name__ == "__main__":
    main()
