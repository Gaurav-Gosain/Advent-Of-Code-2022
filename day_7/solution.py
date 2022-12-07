dirs = {}
cwd = []
current = ""
CD = "$ cd "
ROOT = "/"

for line in open("input/input.txt").read().splitlines():
    if line.startswith(CD):
        if line.endswith(".."):
            cwd.pop()
        else:
            cwd.append(line.replace(CD, ""))
            current = ROOT.join(cwd)
            try:
                dirs[current]
            except:
                dirs[current] = 0
    if line[0].isnumeric():
        for index in range(len(cwd)):
            dirs[ROOT.join(cwd[:int(index)+1])] += int(line.split()[0])

toBeFreed = dirs["/"] - 4 * 10**7

print(f"Part 1: {sum(dirs[x] for x in dirs if dirs[x] <= 10**5)}\nPart 2: {sorted(dirs[x] for x in dirs.keys() if dirs[x] > toBeFreed)[0]}")
