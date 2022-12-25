import re
from os import path
from random import choice
from typing import Callable, Any
from re import Pattern, match
import requests

YEAR = 2022


def _downloadInput(day: int):
    dirPath = path.dirname(path.dirname(__file__))
    sessionFile = path.join(dirPath, 'session.conf')
    if not path.exists(sessionFile):
        print('[AoC]: No session.conf found')
        return

    with open(sessionFile) as f:
        sessionKey = f.read().strip()

    session = requests.Session()
    session.cookies.set('session', sessionKey)
    r = session.get(f'https://adventofcode.com/{YEAR}/day/{day}/input')
    if r.status_code != 200:
        print('[AoC]: Failed to download input', r.status_code)
        return

    return r.text

def _read(s: str, operation: list, typ: type):
    if operation:
        cop, *operation = operation
        if type(cop) is str:
            ts = s.split(cop)
        elif type(cop) is Pattern:
            ts = cop.findall(s)
        else:
            ts = cop(s)
        return [_read(x, operation, typ) for x in ts]
    else:
        return typ(s)


def read(name: str, operations: list = [], typ: type = str, lstrip: str = '', rstrip: str = None, download: bool = True):
    """
    Reads text file and transforms into specified shape and type
    `operations`: list of operations to perform on the input
        `str`: split by `str`
        `Pattern`: findall by `Pattern`
        `Callable`: call with input
    `typ`: type to cast to
    `lstrip`: `str` to lstrip
    `rstrip`: `str` to rstrip
    """

    inpPath = path.join(path.dirname(__file__), f'{name}.txt')

    if download and match(r'^i\d+$', name) and not path.exists(inpPath):
        print('[AoC]: Trying to download input')
        inpData = _downloadInput(int(name[1:]))
        if inpData:
            with open(inpPath, 'w') as f:
                f.write(inpData)

    with open(inpPath) as f:
        file = f.read().rstrip(rstrip).lstrip(lstrip)

    return _read(file, operations, typ)

field, instr = read('input/input', ['\n\n'])

field = [*map(list, field.split('\n'))]

countMoves = [*map(int, re.findall(r'\d+', instr))]
turnMoves = re.findall(r'\D+', instr)


def clamp(a: int, x: int, b: int):
    return max(a, min(x, b))


def splitByCount(s: str, c: int):
    return [s[i:i+c] for i in range(0, len(s), c)]


def qsorted(arr: list, cmp: Callable[[Any, Any], int]) -> list:
    """
    Quick sort list with a custom comparator
    Returns a new list
    """

    if len(arr) <= 1:
        return arr
    pivot = choice(arr)
    left = []
    middle = []
    right = []
    for x in arr:
        cv = cmp(x, pivot)
        if cv < 0:
            left.append(x)
        elif cv == 0:
            middle.append(x)
        else:
            right.append(x)
    return qsorted(left, cmp) + middle + qsorted(right, cmp)


def wrapFlat(x, y, dx, dy):
    while 0 <= y-dy < len(field) and \
            0 <= x-dx < len(field[y-dy]) and \
            field[y-dy][x-dx] != ' ':
        y -= dy
        x -= dx
    return x, y, dx, dy


def wrapCube(x, y, dx, dy):
    B = 50
    c = x // B
    r = y // B
    match (c, r, dx, dy):
        case (0, 1, -1, 0):
            return y % B, 2*B, 0, 1
        case (0, 1, 0, -1):
            return B, x % B + B, 1, 0
        case (2, 1, 1, 0):
            return y % B + 2*B, B-1, 0, -1
        case (2, 1, 0, 1):
            return 2*B-1, x % B + B, -1, 0
        case (1, 3, 1, 0):
            return y % B + B, 3*B-1, 0, -1
        case (1, 3, 0, 1):
            return B-1, x % B + 3*B, -1, 0
        case (0, 4, 0, 1):
            return x + 2*B, 0, 0, 1
        case (2, -1, 0, -1):
            return x - 2*B, 4*B-1, 0, -1
        case (2, 2, 1, 0):
            return 3*B - 1, B - 1 - y % B, -1, 0
        case (3, 0, 1, 0):
            return 2*B - 1, 3*B - 1-y % B, -1, 0
        case (-1, 2, -1, 0):
            return B, B - 1 - y % B, 1, 0
        case (0, 0, -1, 0):
            return 0, 3*B - 1 - y % B, 1, 0
        case (-1, 3, -1, 0):
            return B + y % B, 0, 0, 1
        case (1, -1, 0, -1):
            return 0, 3*B + x % B, 1, 0
    raise Exception(f'Invalid: {c}, {r}, {dx}, {dy}')


def toRot(dx, dy):
    match (dx, dy):
        case (1, 0): return 0
        case (0, 1): return 1
        case (-1, 0): return 2
        case (0, -1): return 3


def solve(wrap):
    x = field[0].index('.')
    y = 0

    dx = 1
    dy = 0
    for i in range(len(countMoves) + len(turnMoves)):
        if i % 2:
            match turnMoves[i // 2]:
                case 'L': dx, dy = dy, -dx
                case 'R': dx, dy = -dy, dx
        else:
            for _ in range(countMoves[i // 2]):
                nx, ny = x + dx, y + dy
                ndx, ndy = dx, dy
                if ny >= len(field) or ny < 0 or nx >= len(field[ny]) or nx < 0 or field[ny][nx] == ' ':
                    # Out of bounds
                    nx, ny, ndx, ndy = wrap(nx, ny, dx, dy)
                if field[ny][nx] == '#':
                    # Wall
                    break
                x, y, dx, dy = nx, ny, ndx, ndy

    return 1000 * (y+1) + 4 * (x+1) + toRot(dx, dy)


print('Part 1:', solve(wrapFlat))
print('Part 2:', solve(wrapCube))
