#!/usr/bin/env python3

from typing import Union

import sys

def getArg(n, default):
    if len(sys.argv) >= n + 1:
        return sys.argv[n]
    return default

inputFile = getArg(1, 'input')
# print(f'{inputFile = }')

class Packet:
    def __init__(self, version: int, typeId: int):
        self.version = version
        self.typeId = typeId

class LitPacket(Packet):
    TYPEID = 4
    def __init__(self, version: int, litVal: int):
        super().__init__(version, LitPacket.TYPEID)
        self.litVal = litVal

class OpPacket(Packet):
    def __init__(self, version: int, typeId: int, args: list[Packet]):
        super().__init__(version, typeId)
        self.args = args

def substr(s: str, pos: int, length: int) -> str:
    if pos + length > len(s):
        raise RuntimeError(f"substr{(pos, length)} of \"{s}\" which length is {len(s)}")
    return s[pos:pos+length]

def parsePacket(s: str, o: int) -> tuple[Packet, int]:
    version = int(substr(s, o, 3), base=2)
    typeId = int(substr(s, o + 3, 3), base=2)
    p = o + 6
    # print(f'parse {s} from {o}')
    # print(f'{version = } {typeId = }')
    if typeId == LitPacket.TYPEID:
        lit = ''
        while True:
            m = s[p]
            p += 1
            lit += substr(s, p, 4)
            p += 4
            if m == '0':
                break
        litVal = int(lit, base=2)
        # print(f'literal packet, value = {litVal}')
        return LitPacket(version, litVal), p
    else:
        # print(f"operator packet")
        subpkts: list[Packet] = []
        if s[p] == '0':
            p += 1
            subpktlen = int(substr(s, p, 15), base=2)
            p += 15
            packetEnd = p + subpktlen
            while p < packetEnd:
                packet, p = parsePacket(s, p)
                subpkts.append(packet)
            assert p == packetEnd
        else:
            assert s[p] == '1'
            p += 1
            subpktCount = int(substr(s, p, 11), base=2)
            p += 11
            for _ in range(subpktCount):
                packet, p = parsePacket(s, p)
                subpkts.append(packet)
        return OpPacket(version, typeId, subpkts), p

def sumVersions(pkt: Packet) -> int:
    s = pkt.version
    if isinstance(pkt, OpPacket):
        s += sum(sumVersions(subPkt) for subPkt in pkt.args)
    return s


with open(inputFile) as fin:
    for line in fin:
        inHex = line.strip()
        inBin = ''.join(f"{int(h, base=16):04b}" for h in inHex)
        packet, _ = parsePacket(inBin, 0)
        print(f'{sumVersions(packet) = }')





