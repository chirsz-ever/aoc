#!/usr/bin/env python3

import sys
import re

reLine = re.compile(r"^Valve (\w+) .*=(\d+);.*to valves? (.*)$")


def main() -> None:
    inputFile = sys.argv[1]

    graph: dict[str, set[str]] = {}
    flow_rate: dict[str, int] = {}
    with open(inputFile) as fin:
        for l in fin:
            l = l.strip()
            if not l:
                continue
            m = reLine.match(l)
            assert m, l
            valve_name = m[1]
            rate = int(m[2])
            nbs = m[3].split(", ")
            graph[valve_name] = set(nbs)
            flow_rate[valve_name] = rate

    for v, nbs in graph.items():
        for n in nbs:
            assert v in graph[n], (v, n)
    assert flow_rate["AA"] == 0
    # print(graph)

    vertexes = list(graph.keys())

    # Floyd–Warshall algorithm
    min_dist: dict[tuple[str, str], int] = {}
    for u, nbs in graph.items():
        for v in nbs:
            min_dist[u, v] = 1
        min_dist[u, u] = 0
    for k in vertexes:
        for i in vertexes:
            for j in vertexes:
                if (
                    (k, j) in min_dist
                    and (i, k) in min_dist
                    and ((i, j) not in min_dist or min_dist[i, j] > min_dist[i, k] + min_dist[k, j])
                ):
                    min_dist[i, j] = min_dist[i, k] + min_dist[k, j]
    # print(min_dist)

    non_zero_vertexes = {v for v in vertexes if flow_rate[v] > 0}

    def dfs(
        current: str,
        current_pressure: int,
        aval_time: int,
        visited: set[str],
    ) -> list[tuple[set[str], int]]:
        # nonlocal max_pressure
        # print(f'dfs{(current,current_pressure,aval_time,visited)}')

        paths: list[tuple[set[str], int]] = [(visited, current_pressure)]

        no_next = False
        next_vs = set()
        if aval_time <= 2:
            no_next = True
        else:
            next_vs = {v for v in non_zero_vertexes.difference(visited) if min_dist[current, v] + 1 < aval_time}
            if len(next_vs) == 0:
                no_next = True

        if no_next:
            return paths

        for v in next_vs:
            t = min_dist[current, v]
            ps = dfs(
                v,
                current_pressure + (aval_time - t - 1) * flow_rate[v],
                aval_time - t - 1,
                visited.union([v]),
            )
            paths += ps
        return paths

    max_pressure = 0

    def dfs_with_max(current: str, current_pressure: int, aval_time: int, visited: set[str]):
        nonlocal max_pressure
        # print(f'dfs{(current,current_pressure,aval_time,visited)}')

        no_next = False
        next_vs = set()
        if aval_time <= 2:
            no_next = True
        else:
            next_vs = {v for v in non_zero_vertexes.difference(visited) if min_dist[current, v] + 1 < aval_time}
            if len(next_vs) == 0:
                no_next = True

        if no_next:
            if max_pressure < current_pressure:
                max_pressure = current_pressure
                # print(f'update {max_pressure=}')
            return

        if sum((aval_time - 2) * flow_rate[v] for v in next_vs) + current_pressure < max_pressure:
            return

        for v in next_vs:
            t = min_dist[current, v]
            dfs_with_max(
                v, current_pressure + (aval_time - t - 1) * flow_rate[v], aval_time - t - 1, visited.union([v])
            )

    paths1 = dfs("AA", 0, 26, set())
    print(f"{len(paths1)=}")
    # for p in paths1:
    #     print(p)
    print(f"{max(p[1] for p in paths1)=}")

    # dedup
    max_len_path_pairs: dict[int, tuple[set[str], int]] = {}
    visited: set[int] = set()
    for i1 in range(len(paths1)):
        if i1 in visited:
            continue
        visited.add(i1)
        max_len = paths1[i1][1]
        max_len_path_pairs[i1] = paths1[i1]
        for i2 in range(i1 + 1, len(paths1)):
            if paths1[i1][0] == paths1[i2][0]:
                visited.add(i2)
                if paths1[i2][1] > max_len:
                    max_len = paths1[i2][1]
                    max_len_path_pairs[i1] = paths1[i2]

    max_len_paths = list(max_len_path_pairs.values())
    print(f"{len(max_len_paths)=}")

    maxp = 0

    # pc = len(max_len_paths) // 10
    # for k, p in enumerate(max_len_paths):
    #     paths2 = dfs("AA", 0, 26, p[0])
    #     maxp = max(maxp, max(p[1] + p2[1] for p2 in paths2))
    #     if k % pc == 0:
    #         print(f"{k//pc*10}%")

    # pc = len(max_len_paths) // 10
    # for k, p in enumerate(max_len_paths):
    #     max_pressure = 0
    #     dfs_with_max("AA", 0, 26, p[0])
    #     maxp = max(maxp, p[1] + max_pressure)
    #     if k % pc == 0:
    #         print(f"{k//pc*10}%")

    pc = len(max_len_paths) // 10
    for i1 in range(len(max_len_paths)):
        for i2 in range(i1 + 1, len(max_len_paths)):
            p1 = max_len_paths[i1]
            p2 = max_len_paths[i2]
            if len(p1[0].intersection(p2[0])) == 0:
                if maxp < p1[1] + p2[1]:
                    maxp = p1[1] + p2[1]
        if i1 % pc == 0:
            print(f"{i1//pc*10}%")

    print(maxp)
    


if __name__ == "__main__":
    main()
