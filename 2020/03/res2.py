from sys import stdin

tree_map = list(map(str.strip, filter(lambda l:not len(l)==0, stdin)))


#print(f"rows={rows}, cols={cols}")

def count_trees(tree_map, col_step, row_step):
    rows = len(tree_map)
    cols = len(tree_map[0])
    r = 0
    c = 0
    cnt = 0
    while r < rows:
        if tree_map[r][c] == '#':
            #print(f"{r},{c} is #")
            cnt += 1
        else:
            # print(f"{r},{c} is .")
            pass
        r += row_step
        c = (c + col_step) % cols
    return cnt

p = 1
for col_step, row_step in [(1,1),(3,1),(5,1),(7,1),(1,2)]:
    p *= count_trees(tree_map, col_step, row_step)

print(p)
