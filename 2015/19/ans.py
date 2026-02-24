#!/usr/bin/env python3

import sys
from collections import deque


def main() -> None:
    inputFile = sys.argv[1]

    rules: list[tuple[str, str]] = []
    molecule0 = ""
    with open(inputFile) as fin:
        for l in fin:
            l = l.strip()
            if not l:
                continue
            if "=>" in l:
                f, t = l.split(" => ")
                assert len(f) <= len(t), l
                assert all(t != t1 for _, t1 in rules), l
                rules.append((f, t))
            else:
                molecule0 = l
    # print(rules)
    # print(molecule0)

    m1s = set()
    for f, t in rules:
        for i in range(len(molecule0)):
            if molecule0.startswith(f, i):
                m1s.add(molecule0[:i] + t + molecule0[i + len(f) :])
    print(len(m1s))

    # def bfs() -> int:
    #     q = deque([('e', 0)])
    #     while len(q) > 0:
    #         m, cnt = q.popleft()
    #         for i in range(len(m)):
    #             for f, t in rules:
    #                 if m.startswith(f, i):
    #                     r = m[:i] + t + m[i+len(f):]
    #                     if r == molecule0:
    #                         return cnt + 1
    #                     if len(r) <= len(molecule0):
    #                         print(f'get {r} with {cnt+1} step')
    #                         q.append((r, cnt + 1))
    # cnt = bfs()
    # print(cnt)

    def bfs() -> int:
        q = deque([(molecule0, 0)])
        while len(q) > 0:
            m, cnt = q.popleft()
            r, steps = reverse_step_max(m, rules)
            if r == "e":
                return cnt + steps
            # print(f"get {r} with {cnt+steps} step")
            q.append((r, cnt + steps))
        return 0

    cnt = bfs()
    print(cnt)


def reverse_step_max(m: str, rules: list[tuple[str, str]]) -> tuple[str, int]:
    cnt = 0
    r = ''
    i = 0
    while i < len(m):
        if rule := find_match_rule(m, i, rules):
            r += rule[0]
            i += len(rule[1])
            cnt += 1
        else:
            r += m[i]
            i += 1
    return (r, cnt)

def find_match_rule(m: str, i: int, rules: list[tuple[str, str]]) -> None | tuple[str, str]:
    for f, t in rules:
        if m.startswith(t, i):
            return (f, t)
    return None

if __name__ == "__main__":
    main()
