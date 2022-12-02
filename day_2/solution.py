x = "ABCXYZ"
p1, p2 = 0, 0
for i in open("input/input.txt").readlines():
    a, b = i.split()
    a, b = x.index(a), x.index(b)-3
    c = b + 1
    p1 += c + ((c - a) % 3) * 3
    p2 += (b * 3 + 1) + ((a + c + 1) % 3)

print(f"Part 1: {p1} \nPart 2: {p2}")
