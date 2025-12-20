#!/usr/bin/env python3
# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "sympy>=1.4",
# ]
# ///

import sys
import sympy as sp
from itertools import product

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

def gauss_elimination(m: list[list[int]]) -> list[list[int]]:
    m1 = sp.Matrix(m)
    rref, pivots = m1.rref()
    ds = { sp.fraction(x)[1] for x in rref }
    # print(f'{ds=}')
    if len(ds) > 1:
        d = sp.ilcm(*ds)
        print(f"{d=}")
        rref *= d
    return [[int(rref[i, j]) for j in range(rref.cols)] for i in range(rref.rows)]

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

def check_choose_valid(m: list[list[int]], choose: list[int|None]) -> bool:
    for i in range(len(m)):
        s = sum((choose[j] or 0) * m[i][j] for j in range(len(choose)))
        if s > m[i][-1]:
            return False
    return True

def find_answers(target_jolts: list[int], schs: list[list[int]]) -> int:
    raw_matrix = [ [ int(i in s) for s in schs ] + [target_jolts[i]] for i in range(len(target_jolts)) ]
    # for r in matrix:
    #     print(r)
    m = gauss_elimination(raw_matrix)
    rows = len(m)
    cols = len(m[0])
    assert rows == len(target_jolts)
    assert cols == len(schs) + 1
    for r in range(rows):
        print(' ', m[r])

    min_answer = None
    must_min_answer = max(target_jolts)
    max_choose = max(target_jolts)

    found_last_row = False
    last_row = None
    last_col = None
    for r in range(rows - 1, -1, -1):
        for c in  range(0, cols):
            if m[r][c] != 0:
                found_last_row = True
                last_row = r
                last_col = c
                break
        if found_last_row:
            break
    assert found_last_row
    assert last_row is not None and last_col is not None
    assert last_row < cols - 1

    if last_row == cols - 1:
        return sum(row[-1] for row in m)

    free_variables: list[int] = [c for c in range(last_col + 1, cols - 1)]
    last_first_col = last_col
    for r in range(last_row - 1, -1, -1):
        first_col = -1
        row = m[r]
        for c in range(0, cols):
            if row[c] != 0:
                first_col = c
                break
        free_variables += [c for c in range(first_col + 1, last_first_col)]
        last_first_col = first_col

    print(f'{free_variables=}')
    # if len(free_variables) == 0:
    #     min_answer = 

    for pinned in product(range(0, max_choose), repeat=len(free_variables)):
        choose = [0] * len(schs)
        for i in range(len(free_variables)):
            choose[free_variables[i]] = pinned[i]
        good = True
        for r in range(rows - 1, -1, -1):
            row = m[r]
            first_col = -1
            for c in range(0, cols):
                if row[c] != 0:
                    first_col = c
                    break
            if first_col == -1:
                continue
            need = row[-1] - sum(choose[c] * row[c] for c in range(cols - 1))
            first_v = row[first_col]
            # print(f'{r=} {first_col=} {first_v=}')
            if need % first_v != 0 or need // first_v < 0:
                good = False
                break
            choose[first_col] = need // first_v
        if good:
            choose_sum = sum(choose)
            if choose_sum == must_min_answer:
                return must_min_answer
            if min_answer is None:
                min_answer = choose_sum
            else:
                min_answer = min(min_answer, choose_sum)
    assert min_answer is not None
    return min_answer

if __name__ == '__main__':
    main()
