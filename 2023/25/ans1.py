#!/usr/bin/env python3

import sys
import random

def main() -> None:
    inputFile = sys.argv[1]

    graph: dict[str, set[str]] = {}
    with open(inputFile) as fin:
        for l in fin:
            l = l.strip()
            if not l:
                continue
            s, ds = l.split(": ")
            for d in ds.split(" "):
                graph.setdefault(s, set()).add(d)
                graph.setdefault(d, set()).add(s)

    # print('graph G {')
    # record = set()
    # for k, v in graph.items():
    #     for d in v:
    #         if (d, k) not in record:
    #             print(f'    {k} -- {d};')
    #             record.add((k, d))
    # print('}')

    vertices = set(graph.keys())
    edges: set[tuple[str, str]] = {
        (v1, v2) if v1 <= v2 else (v2, v1) for v1 in vertices for v2 in graph[v1]
    }

    print(f"{len(vertices)=}")
    print(f"{len(edges)=}")

    # for e1, e2, e3 in combinations(edges, 3):
    #     pass
    # count = sum(1 for _ in combinations(edges, 2))
    # print(f'{count=}')

    # Karger's algorithm
    count = 0
    while True:
        count += 1
        vertices = [{k} for k in graph.keys()]
        while len(vertices) > 2:
            u = random_pick(vertices)
            v = random_pick_neighbor(graph, vertices, u)
            vertices.append(u | v)
        u, v = vertices
        if edge_count(graph, u, v) == 3:
            break
        # if count % 10 == 0:
        #     print(f'try {count} times')
    print(f'try {count} times')
    # print(f'{u}')
    print(f'{len(u)=}')
    # print(f'{v}')
    print(f'{len(v)=}')
    print(f'{len(u) * len(v)=}')

def random_pick[T](arr: list[T]) -> T:
    k = random.randint(0, len(arr) - 1)
    v = arr[k]
    del arr[k]
    return v

def random_pick_neighbor(graph: dict[str, set[str]], vertices: list[set[str]], u: set[str]) -> set[str]:
    found = False
    nv = ''
    for n in u:
        for nn in graph[n]:
            if nn not in u:
                found = True
                nv = nn
                break
    assert found
    for k in range(0, len(vertices)):
        if nv in vertices[k]:
            v = vertices[k]
            del vertices[k]
            return v
    raise RuntimeError(f'cannot found {nv}')

def edge_count(graph: dict[str, set[str]], u: set[str], v: set[str]) -> int:
    return sum(1 for x in u for y in v if y in graph[x])

if __name__ == "__main__":
    main()
