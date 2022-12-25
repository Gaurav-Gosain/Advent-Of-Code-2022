#!/usr/bin/env pypy3
from sys import stdin, exit
from copy import *
from heapq import *
from collections import *
from itertools import *
from functools import *
from math import *
import numpy as np
import os
import sys
import requests

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))


def submit(part: int, ans):
    res = input(f"Submit answer {ans}? [Y/n]")
    if 'N' in res or 'n' in res:
        return
    day = int(os.path.basename(os.path.dirname(os.path.realpath(__file__))))
    r = requests.post(f"https://adventofcode.com/2022/day/{day}/answer", data={
                      "level": part, "answer": ans}, cookies={"session": get_session()})
    res = r.text
    print(res)
    print(res.split("\n")[-16])


with open("input/input.txt", "r") as f:
    data = f.read().split('\n')[:-1]
    rock_data = """
####

.#.
###
.#.

..#
..#
###

#
#
#
#

##
##
""".strip().split("\n")
    rocks: list[list[tuple[int, int]]] = []
    rocks_h: list[int] = []
    cur = 0
    while cur < len(rock_data):
        if rock_data[cur] == "":
            cur += 1
        cur_rock: list[tuple[int, int]] = []
        r = 0
        while cur < len(rock_data) and rock_data[cur] != "":
            for c, x in enumerate(rock_data[cur]):
                if x == "#":
                    cur_rock.append((r, c))
            r -= 1
            cur += 1
        rocks.append(cur_rock)
        rocks_h.append(-r + 1)
    print(rocks)


def check_rock(filled: set[tuple[int, int]], rock: list[tuple[int, int]], r: int, c: int):
    for coord in rock:
        if coord[0] + r <= 0:
            return False
        if not 0 <= coord[1] + c < 7:
            return False
        if (coord[0] + r, coord[1] + c) in filled:
            return False
    return True


def part1():
    ans = 0
    filled: set[tuple[int, int]] = set()
    cur = 0
    for i in range(2022):
        rock = rocks[i % 5]
        r = ans + rocks_h[i % 5] + 2
        c = 2
        assert check_rock(filled, rock, r, c)
        while True:
            left = data[0][cur % len(data[0])] == "<"
            cur += 1
            if left and check_rock(filled, rock, r, c - 1):
                c -= 1
            elif not left and check_rock(filled, rock, r, c + 1):
                c += 1

            if not check_rock(filled, rock, r - 1, c):
                break
            r -= 1
        assert check_rock(filled, rock, r, c)
        for coord in rock:
            filled.add((coord[0] + r, coord[1] + c))
            ans = max(ans, coord[0] + r)
    # submit(1, ans)
    print(ans)


def part2():
    ans = 0
    skipped_ans = 0
    filled: set[tuple[int, int]] = set()
    cur = 0
    hist: dict[tuple[int, int], tuple[int, int]] = {}
    i = 0
    timeskipping = True
    target = 1000000000000
    while i < target:
        rock = rocks[i % 5]
        r = ans + rocks_h[i % 5] + 2
        c = 2
        assert check_rock(filled, rock, r, c)
        while True:
            left = data[0][cur % len(data[0])] == "<"
            cur += 1
            if left and check_rock(filled, rock, r, c - 1):
                c -= 1
            elif not left and check_rock(filled, rock, r, c + 1):
                c += 1

            if not check_rock(filled, rock, r - 1, c):
                break
            r -= 1
        assert check_rock(filled, rock, r, c)
        for coord in rock:
            filled.add((coord[0] + r, coord[1] + c))
            ans = max(ans, coord[0] + r)
        if i > 2022 and timeskipping:
            if (i % 5, cur % len(data[0])) in hist:
                x = hist[i % 5, cur % len(data[0])]
                drops = i - x[1]
                cycles = (target - i) // drops
                i += cycles * drops + 1
                skipped_ans = (ans - x[0]) * cycles
                timeskipping = False
                continue
            hist[i % 5, cur % len(data[0])] = (ans, i)
        i += 1
    # submit(2, ans + skipped_ans)
    print(ans + skipped_ans)

if __name__ == "__main__":
    part1()
    part2()
