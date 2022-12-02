p = sorted(sum(map(int, x.split('\n')))
                     for x in open('input/input.txt').read().split("\n"*2))

print(f"Part 1: {p[-1]} \nPart 2: {sum(p[-3:])}")