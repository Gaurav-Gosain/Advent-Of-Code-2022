
from collections import defaultdict
from queue import Queue
import os
import re
import sys
import time
from typing import Callable


SAMPLE = False


def force_sample():
    global SAMPLE
    SAMPLE = True


def cells(matrix):
    for x, row in enumerate(matrix):
        for y, v in enumerate(row):
            yield x, y, v


def measure(name, f):
    start = time.time()
    result = f()
    print(name, "time took", time.time() - start)
    return result


def sign(x):
    if x == 0:
        return 0
    return -1 if x < 0 else 1


def transpose(list2):
    return list(map(list, zip(*list2)))


def read_map_ints() -> list[list[int]]:
    return [list(map(int, line)) for line in read_lines()]


def read_map_dict() -> dict[tuple[int, int], int]:
    matrix = read_map_ints()
    return {(x, y): matrix[x][y] for x, y in cells(matrix)}


def flatten(list2):
    return [y for x in list2 for y in x]


def read_lines() -> list[str]:
    fh = open("input/input.txt", "r")
    try:
        return fh.read().splitlines()
    finally:
        fh.close()


def clean(line: str, trim):
    if not trim:
        return line
    if isinstance(trim, str):
        return line.replace(trim, " ")
    if isinstance(trim, list):
        for t in trim:
            line = line.replace(t, " ")
    return line


def read(sep: str = None, parse: Callable = None, trim=None) -> list:
    lines = [clean(line, trim) for line in read_lines()]
    return [parse(line) if parse else parse_values(line, sep) for line in lines]


def read_blocks(sep: str = None, parse: Callable = None, trim=None) -> list:
    lines = [clean(line, trim) for line in read_lines()]
    blocks = []
    block = []
    for line in lines:
        if not line:
            blocks.append(block)
            block = []
        else:
            block.append(parse(line) if parse else parse_values(line, sep))
    blocks.append(block)
    return blocks


def parse_values(s: str, sep: str = None):
    parts: list[str] = s.split() if sep is None else re.split(sep, s)
    return [parse_value(item) for item in parts if item != '']


def parse_value(s: str):
    i = try_parse_int(s)
    if i is not None:
        return i
    f = try_parse_float(s)
    if f is not None:
        return f
    return s


def try_parse_int(s: str):
    try:
        return int(s)
    except ValueError:
        return None


def try_parse_float(s: str):
    try:
        return float(s)
    except ValueError:
        return None


def batch(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i:i + n]


def ch_to_int(x):
    return (ord(x) - ord('a') + 1) if 'a' <= x <= 'z' else (ord(x) - ord('A') + 27)


class V:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        return V(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return V(self.x - other.x, self.y - other.y)

    def __mul__(self, other):
        assert isinstance(other, int)
        return V(self.x * other, self.y * other)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        return (self.x, self.y).__hash__()

    def __repr__(self):
        return (self.x, self.y).__repr__()

    def dist_to(self, other):
        return abs(self.x - other.x) + abs(self.y - other.y)

    def dist(self):
        return abs(self.x) + abs(self.y)

    def neighbors_8(self):
        for dx in range(-1, 2):
            for dy in range(-1, 2):
                if dx != 0 or dy != 0:
                    yield self + V(dx, dy)

    def neighbors_4(self):
        yield self + V(0, -1)
        yield self + V(0,  1)
        yield self + V(1,  0)
        yield self + V(-1, 0)

    def neighbors_8_in_box(self, n, m):
        for v in self.neighbors_8():
            if 0 <= v.x < n and 0 <= v.y < m:
                yield v

    def neighbors_4_in_box(self, n, m):
        for v in self.neighbors_4():
            if 0 <= v.x < n and 0 <= v.y < m:
                yield v

    def dir(self):
        return V(sign(self.x), sign(self.y))


class V3:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def __add__(self, other):
        return V3(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other):
        return V3(self.x - other.x, self.y - other.y, self.z + other.z)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y and self.z == other.z

    def __hash__(self):
        return (self.x, self.y, self.z).__hash__()

    def __repr__(self):
        return (self.x, self.y, self.z).__repr__()

    def dist_to(self, other):
        return abs(self.x - other.x) + abs(self.y - other.y) + abs(self.z - other.z)

    def neighbors_6(self):
        for d in [V3(-1, 0, 0), V3(1, 0, 0), V3(0, -1, 0), V3(0, 1, 0), V3(0, 0, -1), V3(0, 0, 1)]:
            yield self + d

    def neighbors_6_in_box(self, lx, rx, ly, ry, lz, rz):
        for d in [V3(-1, 0, 0), V3(1, 0, 0), V3(0, -1, 0), V3(0, 1, 0), V3(0, 0, -1), V3(0, 0, 1)]:
            v = self + d
            if lx <= v.x < rx and ly <= v.y < ry and lz <= v.z < rz:
                yield self + d

    def dir(self):
        return V3(sign(self.x), sign(self.y), sign(self.z))


def get_submasks(mask):
    x = mask
    while True:
        yield x
        if x == 0:
            break
        x = (x - 1) & mask

inp = read_lines()
dirs = {">": V(0, 1), "<": V(0, -1), "v": V(1, 0), "^": V(-1, 0)}
blizzards_x, blizzards_y = defaultdict(list), defaultdict(list)
n = len(inp) - 2
m = len(inp[0]) - 2
START, FINISH = V(-1, 0), V(n, m - 1)

for x, row in enumerate(inp[1:-1]):
    for y, cell in enumerate(row[1:-1]):
        if cell == ".":
            continue
        blizzard = (V(x, y), dirs[cell])
        if dirs[cell].x == 0:
            blizzards_x[x].append(blizzard)
        else:
            blizzards_y[y].append(blizzard)


def has_blizzard(pos: V, time: int) -> bool:
    for v, dir in [*blizzards_x[pos.x], *blizzards_y[pos.y]]:
        nx = (v.x + dir.x * time) % n
        ny = (v.y + dir.y * time) % m
        if pos == V(nx, ny):
            return True
    return False


def bfs(start, finish, start_time) -> int:
    q = Queue()
    visited = set()

    def add_to_queue(v):
        if v not in visited:
            q.put(v)
            visited.add(v)

    add_to_queue((start, start_time))

    while not q.empty():
        pos, time = q.get()
        if pos == finish:
            return time

        for to in pos.neighbors_4():
            in_box = (0 <= to.x < n and 0 <= to.y < m) or to == finish
            if in_box and not has_blizzard(to, time + 1):
                add_to_queue((to, time + 1))

        if not has_blizzard(pos, time + 1):
            add_to_queue((pos, time + 1))


time_1 = measure("one", lambda: bfs(START, FINISH, 0))
time_2 = measure("two", lambda: bfs(FINISH, START, time_1))
time_3 = measure("three", lambda: bfs(START, FINISH, time_2))

print("Part One", time_1)
print("Part Two", time_3)
