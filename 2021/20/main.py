#!/usr/bin/env python3

from itertools import product
import sys


Coord = tuple[int, int]


class Image:
    def __init__(self, input_image: list[str]) -> None:
        self.light_pixels: set[Coord] = set(
            (i, j) for i in range(len(input_image)) for j in range(len(input_image[i])) if input_image[i][j] == "#"
        )
        self.min_i = min(i for i, j in self.light_pixels)
        self.min_j = min(j for i, j in self.light_pixels)
        self.max_i = max(i for i, j in self.light_pixels)
        self.max_j = max(j for i, j in self.light_pixels)
        self.default_light = False

    def apply_image_enhancement_algorithm(self, algorithm: str):
        visited: set[tuple[int, int]] = set()
        light_pixels_new: set[tuple[int, int]] = set()
        for i in range(self.min_i - 1, self.max_i + 2):
            for j in range(self.min_j - 1, self.max_j + 2):
                if (i, j) in visited:
                    continue
                n = 0
                for di in [-1, 0, 1]:
                    for dj in [-1, 0, 1]:
                        n *= 2
                        if self.is_light(i + di, j + dj):
                            n += 1
                if algorithm[n] == "#":
                    light_pixels_new.add((i, j))
                visited.add((i, j))

        self.light_pixels = light_pixels_new
        if self.default_light and algorithm[511] == ".":
            self.default_light = False
        elif not self.default_light and algorithm[0] == "#":
            self.default_light = True

        self.min_i -= 1
        self.min_j -= 1
        self.max_i += 1
        self.max_j += 1

    def is_light(self, i: int, j: int) -> bool:
        if self.min_i <= i <= self.max_i and self.min_j <= j <= self.max_j:
            return (i, j) in self.light_pixels
        return self.default_light

    def print(self):
        for i in range(self.min_i, self.max_i + 1):
            for j in range(self.min_j, self.max_j + 1):
                if self.is_light(i, j):
                    print("#", end="")
                else:
                    print(".", end="")
            print()


def main() -> None:
    inputFile = sys.argv[1]
    steps = int(sys.argv[2])

    input_image: list[str] = []
    algorithm = ""
    with open(inputFile) as fin:
        for lineno, l in enumerate(fin):
            l = l.strip()
            if lineno == 0:
                algorithm = l
                continue
            if not l:
                continue
            input_image.append(l)

    image = Image(input_image)
    for k in range(steps):
        image.apply_image_enhancement_algorithm(algorithm)
        # print(f'---------- after step {k} ----------')
        # image.print()
    print(len(image.light_pixels))


if __name__ == "__main__":
    main()
