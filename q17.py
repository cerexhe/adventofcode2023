from heapq import heapify, heappush, heappop

def read_data() -> list[list[int]]:
    grid = []
    # with open('baby17b.txt') as f:
    with open('input17.txt') as f:
        for line in f.read().split('\n'):
            line = line.strip()
            if not line:
                continue
            grid.append([int(c) for c in line])
    return grid

DIRS = {
    (1,0): '>',
    (-1,0): '<',
    (0,-1): '^',
    (0,1): 'v',
}

def shortest_path(grid: list[list[int]], start: (int, int, int, int, int, int),
                  dest: (int, int), min_straights: int, max_straights: int) -> int:
    q = [start]
    heapify(q)
    parents = {}
    dists = {}

    while q:
        node = heappop(q)
        d,x,y,dx,dy,straights = node

        coord = (x,y)
        xx = (x,y,dx,dy,straights)
        if d < dists.get(xx, d+999):
            dists[xx] = d
            parents[coord] = (x-dx, y-dy)
        else:
            continue

        if coord == dest and straights >= min_straights:
            return d
        for step in neighbours(grid, node, min_straights, max_straights):
            (d2,x2,y2,dx2,dy2,straights) = step
            xx = (x2,y2,dx2,dy2,straights)
            if d2 < dists.get(xx, d2+999):
                heappush(q, step)

def in_bounds(grid: list[list[int]], x: int, y: int) -> bool:
    height = len(grid)
    width = len(grid[0])
    return 0 <= x < width and 0 <= y < height

def neighbours(grid, node, min_straights: int, max_straights: int) -> list:
    loss,x,y,dx,dy,straights = node
    n = []

    x2,y2 = x+dx,y+dy
    if straights < max_straights and in_bounds(grid, x2, y2):
        l2 = loss + grid[y2][x2]
        n.append((l2, x2, y2, dx, dy, straights+1))

    x3,y3 = x+dy,y+dx
    if straights >= min_straights and in_bounds(grid, x3, y3):
        l3 = loss + grid[y3][x3]
        n.append((l3, x3, y3, dy, dx, 0))

    x4,y4 = x-dy,y-dx
    if straights >= min_straights and in_bounds(grid, x4, y4):
        l4 = loss + grid[y4][x4]
        n.append((l4, x4, y4, -dy, -dx, 0))

    # print(f"neighbours of ({x},{y}) in ({dx},{dy}) w/ {straights}: {n}")
    return n

grid = read_data()
height, width = len(grid), len(grid[0])
print(shortest_path(grid, (0, 0, 0, 1, 0, 0), (width-1, height-1), min_straights=0, max_straights=2))
print(shortest_path(grid, (0, 0, 0, 1, 0, 0), (width-1, height-1), min_straights=3, max_straights=9))
