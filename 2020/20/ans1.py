from sys import stdin
from typing import Tuple, List, TextIO, Dict
import re

Tile = List[str]
Id = int
Coord = Tuple[int, int]
TileSet = Dict[Id, Tile]
Pos = int # 四个旋转角度 × 翻转
TileMap = Dict[Coord, Tuple[Id, Pos]]

id_line_re = re.compile(r'Tile (\d+):')

def parse_tile(f: TextIO) -> Tuple[Id, Tile]:
    tid = 0
    if (m := id_line_re.match(f.readline())):
        tid = int(m[1])
    else:
        return (0, [])
    tile = []
    while (line := f.readline().strip()):
        tile.append(line)
    return (tid, tile)

def parse_input(f: TextIO) -> TileSet:
    tiles = dict()
    while any((tid, tile) := parse_tile(f)):
        tiles[tid] = tile

def find_answer(tiles: TileSet) -> TileMap:
    return find_answer1(tiles, {(0, 0): (next(iter(tiles.keys())), 0)})

def find_answer1(tiles: TileSet, pans: TileMap) -> TileMap:
    pass


def product_coners(tiles: TileMap) -> int:
    fst = lambda (x, y): x
    snd = lambda (x, y): y
    w = min(map(fst, tiles.keys()))
    e = max(map(fst, tiles.keys()))
    s = min(map(snd, tiles.keys()))
    n = max(map(snd, tiles.keys()))
    return tiles[e, n] * tiles[e, s] * tiles[w, s] * tiles[w, n]


def main():
    tiles = parse_input(stdin)
    ans = find_answer(tiles)
    print(f'{product_coners(ans)=}')

if __name__ == '__main__':
    main()
