#!/usr/bin/env python3

import sys
from dataclasses import dataclass
from collections import deque

@dataclass()
class Brick:
    position: tuple[int, int, int]
    size: tuple[int, int, int]
    name: str = ''

    def __hash__(self) -> int:
        return hash((self.position, self.size))

    def __eq__(self, value: object) -> bool:
        return isinstance(value, Brick) and hash(value) == hash(self)


def main() -> None:
    inputFile = sys.argv[1]

    bricks: list[Brick] = []
    name = ord("A")
    with open(inputFile) as fin:
        for l in fin:
            l = l.strip()
            if not l:
                continue
            p1, p2 = [[int(x) for x in p.split(",")] for p in l.split("~")]
            pos = tuple(map(min, zip(p1, p2)))
            size = tuple(abs(q1 - q2) + 1 for q1, q2 in zip(p1, p2))
            assert len(pos) == 3
            assert len(size) == 3
            # bricks.append(Brick(pos, size, chr(name)))
            bricks.append(Brick(pos, size))
            name += 1
    # print(bricks)

    # print("**********")
    # print_xz(bricks)
    # print("**********")
    # print_yz(bricks)

    bricks_by_top: dict[int, set[Brick]] = {}
    for b in bricks:
        bricks_by_top.setdefault(b.position[2] + b.size[2] - 1, set()).add(b)

    # Falling
    while True:
        bricks.sort(key=lambda x: x.position[2])
        fall_happen = False
        for b in bricks:
            if try_fall(b, bricks_by_top):
                # print(f'fall {b.name}')
                # print("**********")
                # print_xz(bricks)
                # print("**********")
                # print_yz(bricks)
                fall_happen = True
        if not fall_happen:
            break

    # print("----- after falling -----")
    # print_xz(bricks)
    # print("**********")
    # print_yz(bricks)

    bricks_by_low: dict[int, set[Brick]] = {}
    for b in bricks:
        bricks_by_low.setdefault(b.position[2], set()).add(b)

    s = 0
    for b in bricks:
        overlapped_top_bricks = get_overlapped_top_bricks(b, bricks_by_low)
        # print(f'overlapped_top_bricks of {b}: {overlapped_top_bricks}')
        if len(overlapped_top_bricks) == 0:
            s += 1
            # print(f'{b.name} can be disintegrated')
            continue
        may_support_bricks = bricks_by_top[b.position[2] + b.size[2] - 1]
        if len(may_support_bricks) <= 1:
            # print(f'{b.name} cannot be disintegrated')
            continue
        can_disintegrated = True
        for tb in overlapped_top_bricks:
            if sum(1 for mb in may_support_bricks if overlap_xy(mb, tb)) <= 1:
                can_disintegrated = False
                break
        s += int(can_disintegrated)
        # if can_disintegrated:
        #     print(f'{b.name} can be disintegrated')
        # else:
        #     print(f'{b.name} cannot be disintegrated')

    print("ans1:", s)

    # fall_num = {}
    # for b in reversed(bricks):
    #     falled_set = {b}
    #     while True:
    #         top_set: set[Brick] = set()
    #         for b1 in falled_set:
    #             top_set.update(get_overlapped_top_bricks(b1, bricks_by_low))
    #         top_set.difference_update(falled_set)
    #         updated = False
    #         new_falled_bricks = set()
    #         for tb in top_set:
    #             if tb.position[2] <= 1:
    #                 continue
    #             overlapped_bottom_bricks = set(get_overlapped_bottom_bricks(tb, bricks_by_top))
    #             overlapped_bottom_bricks.difference_update(falled_set)
    #             if len(overlapped_bottom_bricks) == 0:
    #                 new_falled_bricks.add(tb)
    #                 updated = True
    #         if not updated:
    #             break
    #         falled_set.update(new_falled_bricks)
    #     fall_num[b] = len(falled_set) - 1
    # print("ans2:", sum(fall_num.values()))

    # https://www.reddit.com/r/adventofcode/comments/18o7014/comment/keylpbi/
    s2 = 0
    for b in bricks:
        is_falling: set[Brick] = { b }
        queue: deque[Brick] = deque([b])
        while len(queue) > 0:
            b1 = queue.popleft()
            for tb in get_overlapped_top_bricks(b1, bricks_by_low):
                if tb in is_falling:
                    continue
                if will_fall(tb, is_falling, bricks_by_top):
                    is_falling.add(tb)
                    queue.append(tb)
                    s2 += 1
    print('ans2:', s2)

def will_fall(b:Brick, is_falling: set[Brick], bricks_by_top: dict[int, set[Brick]]) -> bool:
    overlapped_bottom_bricks = set(get_overlapped_bottom_bricks(b, bricks_by_top))
    return all(bb in is_falling for bb in overlapped_bottom_bricks)

def get_overlapped_top_bricks(
    b: Brick, bricks_by_low: dict[int, set[Brick]]
) -> list[Brick]:
    return [
        b1
        for b1 in bricks_by_low.get(b.position[2] + b.size[2], [])
        if overlap_xy(b, b1)
    ]


def get_overlapped_bottom_bricks(
    b: Brick, bricks_by_top: dict[int, set[Brick]]
) -> list[Brick]:
    return [b1 for b1 in bricks_by_top.get(b.position[2] - 1, []) if overlap_xy(b, b1)]


def print_xz(bricks: list[Brick]):
    len_x = max(b.position[0] + b.size[0] - 1 for b in bricks) + 1
    len_z = max(b.position[2] + b.size[2] - 1 for b in bricks) + 1
    m = [["." for _ in range(len_x)] for _ in range(len_z)]
    for b in bricks:
        for x in range(b.position[0], b.position[0] + b.size[0]):
            for z in range(b.position[2], b.position[2] + b.size[2]):
                m[z][x] = b.name if m[z][x] == "." else "?"
    for z in range(len_z - 1, -1, -1):
        for x in range(0, len_x):
            print(m[z][x] if z != 0 else "-", end="")
        print()


def print_yz(bricks: list[Brick]):
    len_y = max(b.position[1] + b.size[1] - 1 for b in bricks) + 1
    len_z = max(b.position[2] + b.size[2] - 1 for b in bricks) + 1
    m = [["." for _ in range(len_y)] for _ in range(len_z)]
    for b in bricks:
        for y in range(b.position[1], b.position[1] + b.size[1]):
            for z in range(b.position[2], b.position[2] + b.size[2]):
                m[z][y] = b.name if m[z][y] == "." else "?"
    for z in range(len_z - 1, -1, -1):
        for y in range(0, len_y):
            print(m[z][y] if z != 0 else "-", end="")
        print()


def in_region(x, y, ax, ay, ax1, ay1) -> bool:
    return ax <= x <= ax1 and ay <= y <= ay1


def overlap_xy(a: Brick, b: Brick) -> bool:
    ax1, ay1 = a.position[0], a.position[1]
    ax2, ay2 = a.position[0] + a.size[0] - 1, a.position[1] + a.size[1] - 1
    bx1, by1 = b.position[0], b.position[1]
    bx2, by2 = b.position[0] + b.size[0] - 1, b.position[1] + b.size[1] - 1
    if ax2 < bx1 or bx2 < ax1 or ay2 < by1 or by2 < ay1:
        return False
    return True


def can_support(bricks_by_top: dict[int, set[Brick]], b: Brick, z: int) -> bool:
    low_bricks = bricks_by_top.get(z - 1)
    if low_bricks is None:
        return False
    return any(overlap_xy(b1, b) for b1 in low_bricks)


def try_fall(b: Brick, bricks_by_top: dict[int, set[Brick]]) -> bool:
    if b.position[2] <= 1:
        return False
    if can_support(bricks_by_top, b, b.position[2]):
        return False
    z = b.position[2] - 1
    while not can_support(bricks_by_top, b, z) and z > 1:
        z -= 1

    ztop_old = b.position[2] + b.size[2] - 1
    ztop_new = z + b.size[2] - 1
    bricks_by_top[ztop_old].remove(b)
    b.position = (b.position[0], b.position[1], z)
    bricks_by_top.setdefault(ztop_new, set()).add(b)
    return True


if __name__ == "__main__":
    main()
