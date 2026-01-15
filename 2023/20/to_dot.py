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
    module_names: list[str] = []
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
            module_names.append(name)

    def node_name(name: str) -> str:
        m = conf_graph.get(name)
        if not m:
            return name
        if isinstance(m, FlipFlop):
            return '\\%' + name
        if isinstance(m, Conjunction):
            return '&' + name
        return name

    print('digraph G{')
    for name in module_names:
        m = conf_graph.get(name)
        if not m:
            continue
        dests = ', '.join(f'"{node_name(d)}"' for d in m.destinations)
        print(f'    "{node_name(name)}" -> {dests};')
    print('}')

if __name__ == '__main__':
    main()
