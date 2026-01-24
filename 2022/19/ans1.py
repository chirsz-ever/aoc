#!/usr/bin/env python3

import sys
import re

Robot = list[int]
Blueprint = list[Robot]

reRobot = re.compile(r'Each (\w+) robot costs (.+?)\.')
reBlueprint = re.compile(r'Blueprint (\d+):')

resource_names = ['ore', 'clay', 'obsidian', 'geode']
resource_index = {name: i for i, name in enumerate(resource_names)}

def main() -> None:
    inputFile = sys.argv[1]
    part = sys.argv[2] if len(sys.argv) >= 3 else '1'

    with open(inputFile) as fin:
        content = fin.read().strip()

    blueprints: list[Blueprint] = []
    parse_pos = 0
    while True:
        # skip whitespace
        while parse_pos < len(content) and content[parse_pos] in '\r\n ':
            parse_pos += 1
        if m := reBlueprint.match(content, parse_pos):
            parse_pos = m.end()
            blueprints.append([[0, 0, 0, 0] for _ in range(4)])
        elif m := reRobot.match(content, parse_pos):
            parse_pos = m.end()
            robot_type_index = resource_index[m.group(1)]
            cost_desc = m.group(2)
            cost_parts = cost_desc.split(' and ')
            for p in cost_parts:
                num_s, res_s = p.split(' ')
                num = int(num_s)
                res_idx = resource_index[res_s]
                blueprints[-1][robot_type_index][res_idx] = num
        else:
            if parse_pos >= len(content):
                break
            else:
                raise ValueError(f"Cannot parse at position {parse_pos}: '{content[parse_pos:parse_pos+40]}'")
    # for i, b in enumerate(blueprints):
    #     print("Blueprint", i + 1)
    #     for rtype, costs in zip(resource_names, b):
    #         print(f"  {rtype} robot costs: {costs}")

    # sum_quality_levels = 0
    # for bp_index, blueprint in enumerate(blueprints):
    #     print(f"Simulating blueprint {bp_index + 1}...")
    #     max_geodes = simulate_blueprint(blueprint, 24)
    #     print(f"Blueprint {bp_index + 1}: {max_geodes} geodes")
    #     sum_quality_levels += (bp_index + 1) * max_geodes

    if part == '1':
        sum_quality_levels = sum((i + 1) * simulate_blueprint(bp, 24) for i, bp in enumerate(blueprints))
        print(f"sum_quality_levels: {sum_quality_levels}")
    else:
        assert part == '2', part
        product_geodes = 1
        for bp in blueprints[:3]:
            max_geodes = simulate_blueprint(bp, 32)
            print(f"Max geodes for blueprint: {max_geodes}")
            product_geodes *= max_geodes
        print(f"product_geodes: {product_geodes}")

# see https://www.reddit.com/r/adventofcode/comments/zpihwi/comment/j1vj08v/
def simulate_blueprint(blueprint: Blueprint, total_minutes: int) -> int:
    max_geodes = 0
    max_robots = [max(blueprint[r][i] for r in range(4)) for i in range(4)]
    # print(f"Max costs: {max_cost}")

    def dfs(remaining: int, resources: tuple[int, int, int, int], robots: tuple[int, int, int, int]) -> None:
        # print(f"{' '*(total_minutes-remaining)}Remaining: {remaining}, resources: {resources}, robots: {robots}")
        nonlocal max_geodes
        if remaining == 0:
            if resources[3] > max_geodes:
                max_geodes = resources[3]
            return
        if remaining == 1:
            geodes = resources[3] + robots[3]
            if geodes > max_geodes:
                max_geodes = geodes
            return

        # Upper bound estimation
        potential_geodes = resources[3] + robots[3] * remaining + (remaining * (remaining - 1)) // 2
        if potential_geodes <= max_geodes:
            return

        # if we can stably build geode robots, do it
        if all(robots[i] >= blueprint[3][i] for i in range(4)):
            if all(resources[i] >= blueprint[3][i] for i in range(4)):
                result = resources[3] + robots[3] * remaining + (remaining * (remaining - 1)) // 2
            else:
                result = resources[3] + robots[3] * remaining + (remaining - 1) * (remaining - 2) // 2
            if result > max_geodes:
                max_geodes = result
            return

        # Try to build each type of robot
        for robot_type in reversed(range(4)):
            if robot_type < 3 and robots[robot_type] >= max_robots[robot_type]:
                continue

            costs = blueprint[robot_type]

            if any(costs[res] > 0 and robots[res] == 0 for res in range(4)):
                continue

            wait_time = 0
            for res in range(4):
                if costs[res] > 0 and resources[res] < costs[res]:
                    needed = costs[res] - resources[res]
                    wait_time = max(wait_time, (needed + robots[res] - 1) // robots[res])

            wait_time += 1  # plus one minute to build
            if wait_time >= remaining:
                continue

            new_resources = tuple(resources[i] + robots[i] * wait_time - costs[i] for i in range(4))
            new_robots = list(robots)
            new_robots[robot_type] += 1
            new_robots = tuple(new_robots)
            # print(f"Minute {t}: Build {resource_names[robot_type]} robot, wait {wait_time}")
            dfs(remaining - wait_time, new_resources, new_robots)

        # wait to end
        geodes = resources[3] + robots[3] * remaining
        if geodes > max_geodes:
            max_geodes = geodes

    dfs(total_minutes, (0, 0, 0, 0), (1, 0, 0, 0))

    return max_geodes

def should_try_wait(can_build: list[bool]) -> bool:
    return not can_build[0] or not can_build[0]

if __name__ == "__main__":
    main()
