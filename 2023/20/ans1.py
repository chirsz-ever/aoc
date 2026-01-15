#!/usr/bin/env python3

from typing import Literal, Protocol
import sys
import re
from collections import deque

Pulse = Literal['on', 'off']

def flip(p: Pulse) -> Pulse:
    return 'on' if p == 'off' else 'off'

class Module(Protocol):
    def __init__(self, destinations: list[str]) -> None:
        super().__init__()
        self.destinations = destinations

    destinations: list[str]

    def receive(self, sender: str, pulse: Pulse) -> Pulse | None:
        raise NotImplementedError()

class Broadcaster(Module):
    def __init__(self, destinations: list[str]) -> None:
        super().__init__(destinations)

    def receive(self, sender: str, pulse: Pulse) -> Pulse | None:
        return pulse

class FlipFlop(Module):
    def __init__(self, destinations: list[str]) -> None:
        super().__init__(destinations)
        self.status: Pulse = 'off'

    def receive(self, sender: str, pulse: Pulse) -> Pulse | None:
        if pulse == 'off':
            self.status = flip(self.status)
            return self.status

class Conjunction(Module):
    def __init__(self, destinations: list[str]) -> None:
        super().__init__(destinations)
        self.inputs: dict[str, Pulse] = {}

    def receive(self, sender: str, pulse: Pulse) -> Pulse | None:
        self.inputs[sender] = pulse
        if all(v == 'on' for v in self.inputs.values()):
            return 'off'
        return 'on'

def main() -> None:
    inputFile = sys.argv[1]

    reConf = re.compile(r'([%&]?)(\w+) -> (.*)')
    conf_graph: dict[str, Module] = {}
    with open(inputFile) as fin:
        for l in fin:
            l = l.strip()
            if not l:
                continue
            m = reConf.fullmatch(l)
            assert m, l
            t, name, dests = m[1], m[2], m[3]
            destinations = dests.split(', ')
            if t == '%':
                module = FlipFlop(destinations)
            elif t == '&':
                module = Conjunction(destinations)
            else:
                assert t == '' and name == 'broadcaster', l
                module = Broadcaster(destinations)
            conf_graph[name] = module
    for name, module in conf_graph.items():
        for d in module.destinations:
            md = conf_graph.get(d)
            if md and isinstance(md, Conjunction):
                md.inputs[name] = 'off'

    on_cnt = 0
    off_cnt = 0
    for _ in range(1000):
        queue: deque[tuple[str, str, Pulse]] = deque()
        queue.append(('button', 'broadcaster', 'off'))

        while len(queue) > 0:
            sender, receiver, p = queue.popleft()
            if p == 'on':
                on_cnt += 1
            else:
                off_cnt += 1

            m = conf_graph.get(receiver)
            if not m:
                continue
            pn = m.receive(sender, p)
            if pn:
                for mr in m.destinations:
                    queue.append((receiver, mr, pn))

    print(f'{on_cnt=}, {off_cnt=}, {on_cnt*off_cnt=}')

if __name__ == '__main__':
    main()
