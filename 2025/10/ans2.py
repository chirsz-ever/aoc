#!/usr/bin/env python3

import sys
import math

def main() -> None:
    inputFile = 'input'
    if len(sys.argv) >= 2:
        inputFile = sys.argv[1]

    diagrams: list[str] = []
    schematics: list[list[list[int]]] = []
    joltages: list[list[int]] = []
    with open(inputFile) as fin:
        for l in fin:
            diag = ''
            schs = []
            jolt = []
            for seg in l.strip().split():
                if seg[0] == '[':
                    diag = seg[1:-1]
                elif seg[0] == '(':
                    schs.append([int(x) for x in seg[1:-1].split(',')])
                elif seg[0] == '{':
                    jolt = [int(x) for x in seg[1:-1].split(',')]
            diagrams.append(diag)
            schematics.append(schs)
            joltages.append(jolt)
    
    # print(f'{diagrams=}')
    # print(f'{schematics=}')
    # print(f'{joltages=}')
    
    # bag problem
    s = 0
    for i in range(len(diagrams)):
        jolt = joltages[i]
        schs = schematics[i]
        print(f'searching {i}')
        answer = find_answers(jolt, schs)
        # if math.answers:
        #     raise RuntimeError(f'not found answer {i}')
        # n = min(sum(a) for a in answers)
        print(f'{i}: {answer}')
        s += answer
    print(f's = {s}')

def is_match(jolt: list[int], schs: list[list[int]], choose: list[int]) -> bool:
    d = [0] * len(jolt)
    for i in range(len(schs)):
        if choose[i]:
            s = schs[i]
            for l in s:
                d[l] += 0 if choose[i] == -1 else choose[i]

    result = d == jolt
    # print(f'check {choose}: {result}')
    return result

def combinations(max_jolt: int, size: int):
    if size == 1:
        yield [max_jolt]
        return
    if size == 2:
        for x0 in range(0, max_jolt + 1):
            yield [x0, max_jolt - x0]
        return
    for x0 in range(0, max_jolt + 1):
        for cb in combinations(max_jolt - x0, size - 1):
            cb.append(x0)
            yield cb


def find_answers(lights: list[int], schs: list[list[int]]) -> int:
    min_answer = [math.inf]
    must_min_answer = max(lights)
    
    sch_cnts = [0] * len(lights)
    for i in range(0, len(lights)):
        sch_cnts[i] = sum(1 if i in sch else 0 for sch in schs)
    print(f'{sch_cnts=}')
    
    sorted_light_indexes = list(range(len(lights)))
    sorted_light_indexes.sort(key = lambda i: (sch_cnts[i], lights[i]))
    print(f'{sorted_light_indexes=}')

    found = [False]
    # check per light
    def step(i, choose: list[int]) -> None:
        if found[0]:
            return
        
        # print(f'step {i=} {choose=}')
        if i == len(lights):
            # if is_match(lights, schs, choose):
            min_answer[0] = min(min_answer[0], sum((c if c != -1 else 0) for c in choose))
            if min_answer[0] == must_min_answer:
                found[0] = True
            return

        index = sorted_light_indexes[i]
        target_jolt = lights[index]

        schs_p = []
        schs_np = []
        for j, s in enumerate(schs):
            if index in s:
                if choose[j] == -1:
                    schs_np.append(j)
                else:
                    schs_p.append(j)

        # print(f'{schs_p=} {schs_np=}')
        pinned_jolt = sum((choose[j] if choose[j] != -1 else 0) for j in schs_p)
        # print(f'{pinned_jolt=}')

        if pinned_jolt > target_jolt:
            return

        nps = len(schs_np)

        if pinned_jolt == target_jolt:
            new_choose = choose.copy()
            for k in range(nps):
                new_choose[k] = 0
            step(i + 1, new_choose)
            return

        # pinned_jolt < target_jolt

        if nps == 0:
            return

        avail = target_jolt - pinned_jolt
        if nps == 1:
            new_choose = choose.copy()
            new_choose[schs_np[0]] = avail
            step(i + 1, new_choose)
        else:
            if i == 0:
                print(f'{i}: combinations({avail}, {nps})')
            for comb in combinations(avail, nps):
                new_choose = choose.copy()
                for k, m in zip(schs_np, comb):
                    new_choose[k] = m
                step(i + 1, new_choose)
                if found[0]:
                    return

    step(0, [-1] * len(schs))
    return int(min_answer[0])

if __name__ == '__main__':
    main()
