from functools import cache
from aoc import *

tunnels: dict[str, list[str]] = {}
valves_with_rate: dict[str, int] = {}
valves_with_rate_index: dict[str, int] = {}
dist: dict[str, dict[str, int]] = {}


inp = read(trim=["Valve", "has flow rate=", ";", "tunnels",
           "tunnel", "leads to", "lead to ", "valves", "valve", ","])
for line in inp:
    valve = line[0]
    rate = line[1]
    if rate or valve == "AA":
        valves_with_rate_index[valve] = len(valves_with_rate)
        valves_with_rate[valve] = rate
    for to in line[2:]:
        tunnels[valve] = line[2:]

n = len(valves_with_rate)


for x in tunnels.keys():
    dist[x] = {}
    for y in tunnels.keys():
        dist[x][y] = 1000000000

for x, ys in tunnels.items():
    for y in ys:
        dist[x][y] = 1

for k in tunnels.keys():
    for x in tunnels.keys():
        for y in tunnels.keys():
            dist[x][y] = min(dist[x][y], dist[x][k] + dist[k][y])


def get_total_rate(mask: int) -> int:
    total = 0
    for valve, rate in valves_with_rate.items():
        index = valves_with_rate_index[valve]
        if (1 << index) & mask:
            total += rate
    return total


@cache
def calc(mask: int, pos: str, minutes: int, minutes_max: int) -> int:
    if minutes > minutes_max:
        return -1

    if minutes == minutes_max:
        if pos == "AA" and mask == 0:
            return 0
        else:
            return -1

    best = -1
    delta = get_total_rate(mask)

    if (x := calc(mask, pos, minutes + 1, minutes_max)) != -1:
        best = max(best, delta + x)

    for new_pos in valves_with_rate.keys():
        if (x := calc(mask, new_pos, minutes + dist[pos][new_pos], minutes_max)) != -1:
            best = max(best, delta * dist[pos][new_pos] + x)

    if (index := valves_with_rate_index.get(pos)) is not None and (mask & (1 << index)):
        if (x := calc(mask - (1 << index), pos, minutes + 1, minutes_max)) != -1:
            best = max(best, delta + x)

    return best


def solve():
    best = -1
    for msk in range(0, (1 << n)):
        for pos in valves_with_rate.keys():
            best = max(best, calc(msk, pos, 1, 30))
    return best


def solve_2():
    best = {}
    for msk in range(0, (1 << n)):
        best_x = -1
        for pos in valves_with_rate.keys():
            x = calc(msk, pos, 1, 26)
            if x >= 0:
                best_x = max(x, best_x)
        best[msk] = best_x

    answer = -1
    for msk in range(0, (1 << n)):
        if best[msk] == -1:
            continue
        for msk_2 in get_submasks(((1 << n) - 1) - msk):
            if best[msk_2] == -1:
                continue
            answer = max(answer, best[msk] + best[msk_2])
    return answer


ans = measure("part one", solve)
print("Part One", ans)

ans = measure("part two", solve_2)
print("Part two", ans)
