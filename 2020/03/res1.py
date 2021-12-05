from sys import stdin

tree_map = list(map(str.strip, filter(lambda l:not len(l)==0, stdin)))

r = 0
c = 0
rows = len(tree_map)
cols = len(tree_map[0])

print(f"rows={rows}, cols={cols}")

tree_cnt = 0

while r < rows:
    if tree_map[r][c] == '#':
        #print(f"{r},{c} is #")
        tree_cnt += 1
    else:
        # print(f"{r},{c} is .")
        pass
    r += 1
    c = (c + 3) % cols

print(tree_cnt)
