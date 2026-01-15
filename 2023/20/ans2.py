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

    xr_cnt = 0
    kk_cnt = 0
    vt_cnt = 0
    fv_cnt = 0
    btn_cnt = 0
    while True:
        btn_cnt += 1
        queue: deque[tuple[str, str, Pulse]] = deque()
        queue.append(('button', 'broadcaster', 'off'))

        while len(queue) > 0:
            sender, receiver, p = queue.popleft()
            if (receiver, p) == ('xr', 'off'):
                print(f'xr <- low, {btn_cnt=}')
                xr_cnt = btn_cnt
            if (receiver, p) == ('kk', 'off'):
                print(f'kk <- low, {btn_cnt=}')
                kk_cnt = btn_cnt
            if (receiver, p) == ('vt', 'off'):
                print(f'vt <- low, {btn_cnt=}')
                vt_cnt = btn_cnt
            if (receiver, p) == ('fv', 'off'):
                print(f'fv <- low, {btn_cnt=}')
                fv_cnt = btn_cnt

            m = conf_graph.get(receiver)
            if not m:
                continue
            pn = m.receive(sender, p)
            if pn:
                for mr in m.destinations:
                    queue.append((receiver, mr, pn))
        if xr_cnt != 0 and kk_cnt != 0 and vt_cnt != 0 and fv_cnt != 0:
            break

    print(f'{xr_cnt*kk_cnt*vt_cnt*fv_cnt=}')

if __name__ == '__main__':
    main()
