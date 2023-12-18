def read_data() -> list[str]:
    lines = []
    with open('input16.txt') as f:
    # with open('baby16.txt') as f:
        for line in f.read().split('\n'):
            line = line.strip()
            if not line:
                continue
            lines.append(line)
    return lines

def count_energised(grid: list[str], initial_beam: (int,int,int,int)) -> int:
    beams = set([initial_beam])
    seen = set([])
    energised = set()
    while beams:
        beam = beams.pop()
        if beam in seen:
            continue
        x,y,dx,dy = beam
        seen.add(beam)
        energised.add((x,y))

        x2 = x+dx
        y2 = y+dy
        if 0 <= x2 < len(grid[0]) and 0 <= y2 < len(grid):
            # energised.add((x2, y2))
            # seen.add((x2,y2,dx,dy))
            c = grid[y2][x2]
            beam2s = None
            if c == '.':
                beam2s = [(x2,y2,dx,dy)]
            elif c == '|':
                if dx:
                    assert dy == 0
                    beam2s = [(x2,y2,0,-1), (x2,y2,0,1)]
                else:
                    beam2s = [(x2,y2,dx,dy)]
            elif c == '-':
                if dy:
                    assert dx == 0
                    beam2s = [(x2,y2,-1,0), (x2,y2,1,0)]
                else:
                    beam2s = [(x2,y2,dx,dy)]
            elif c == '/':
                if dx < 0:
                    dx,dy = 0, 1
                elif dx > 0:
                    dx,dy = 0, -1
                elif dy < 0:
                    dx,dy = 1, 0
                else:
                    assert dy > 0
                    dx,dy = -1 ,0
                beam2s = [(x2,y2,dx,dy)]
            elif c == '\\':
                if dx < 0:
                    dx,dy = 0, -1
                elif dx > 0:
                    dx,dy = 0, 1
                elif dy < 0:
                    dx,dy = -1, 0
                else:
                    assert dy > 0
                    dx,dy = 1, 0
                beam2s = [(x2,y2,dx,dy)]
            else:
                assert False
            for b in beam2s:
                beams.add(b)

    if False:
        for y,line in enumerate(grid):
            for x,c in enumerate(line):
                v = '#' if (x,y) in energised else c
                print(v, end='')
            print()

    x,y,_,_ = initial_beam
    energised.discard((x,y))
    return len(energised)

def count_max_energised(grid: list[str]) -> int:
    height = len(grid)
    width = len(grid[0])

    candidates = []
    for y in range(height):
        candidates.append((-1,y,1,0))
        candidates.append((width,y,-1,0))
    for x in range(width):
        candidates.append((x,-1,0,1))
        candidates.append((x,height,0,-1))

    best = 0
    for beam in candidates:
        score = count_energised(grid, beam)
        best = max(best, score)
    return best

data = read_data()
print(count_energised(data, (-1,0,1,0)))
print(count_max_energised(data))
