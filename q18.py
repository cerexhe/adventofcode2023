import re
import math
from dataclasses import dataclass

PATTERN = re.compile(r'^(?P<direction>[UDLR]) (?P<distance>\d+) [(][#](?P<code>[a-fA-F0-9]+)[)]$')

DIRS = {
    'U': (0, -1),
    'D': (0, 1),
    'L': (-1, 0),
    'R': (1, 0),
}

CODE_TO_DIR = {
    0: DIRS['R'],
    1: DIRS['D'],
    2: DIRS['L'],
    3: DIRS['U'],
}

@dataclass
class Instruction:
    distance: int
    dx: int
    dy: int

@dataclass
class Boundary:
    minx: int
    maxx: int
    miny: int
    maxy: int

    def inside(self, pt: (int, int)) -> bool:
        x, y = pt
        return self.minx <= x <= self.maxx and self.miny <= y <= self.maxy

def read_data() -> (list[Instruction], list[Instruction]):
    instructions_v1 = []
    instructions_v2 = []
    # with open('baby18.txt') as f:
    with open('input18.txt') as f:
        for line in f.read().split('\n'):
            line = line.strip()
            if not line:
                continue
            m = PATTERN.match(line)
            assert m
            dist = int(m.group('distance'))
            dx,dy = DIRS[m.group('direction')]
            code = m.group('code')
            instructions_v1.append(Instruction(
                distance=dist,
                dx=dx,
                dy=dy))

            dist = int(code[:5], base=16)
            dx,dy = CODE_TO_DIR[int(code[-1])]
            instructions_v2.append(Instruction(
                distance=dist,
                dx=dx,
                dy=dy))
    return instructions_v1, instructions_v2

# right hand/clockwise turns
# TODO is clockwise an assumption about data?
# if first path starts anti-clockwise then "is reflex" should probably be _left_ turns?!
def is_reflex(i0: Instruction, i1: Instruction) -> bool:
    return \
        (i0.dx > 0 and i1.dy > 0) or \
        (i0.dx < 0 and i1.dy < 0) or \
        (i0.dy < 0 and i1.dx > 0) or \
        (i0.dy > 0 and i1.dx < 0)

def volume(instructions: list[Instruction]) -> int:
    total_area = 0

    previous = (0, 0)
    last_was_reflex = is_reflex(instructions[-1], instructions[0])
    for i, instruction in enumerate(instructions):
        dist = instruction.distance #  + 1 if i.dx < 0 or i.dy < 0 else i.distance

        i1 = instructions[i+1] if i < len(instructions) - 1 else instructions[0]
        assert (instruction.dx != 0) != (i1.dx != 0)
        next_is_reflex = is_reflex(instruction, i1)

        dmod = 0
        if next_is_reflex and last_was_reflex:
            dmod = 1
        elif not next_is_reflex and not last_was_reflex:
            dmod = -1

        last_was_reflex = next_is_reflex
        dist += dmod

        next_point = (previous[0] + dist * instruction.dx, previous[1] + dist * instruction.dy)

        x0,y0 = previous
        x1,y1 = next_point
        total_area += x0 * y1 - y0 * x1
        previous = next_point

    assert previous == (0, 0)
    x0,y0 = previous
    x1,y1 = (0, 0)
    total_area += x0 * y1 - y0 * x1

    return total_area // 2

def volume_slow(instructions: list[Instruction]) -> int:
    pos = (0, 0)
    grid = set([pos])
    for instruction in instructions:
        for _ in range(instruction.distance):
            pos = pos[0] + instruction.dx, pos[1] + instruction.dy
            grid.add(pos)

    boundary_size = len(grid)
    boundary = find_bounding_box(grid)
    outer_point = (boundary.minx, boundary.miny)
    outer_plus_boundary_size = len(floodfill(grid, boundary, outer_point))
    bounding_box_size = (boundary.maxx - boundary.minx + 1) * (boundary.maxy - boundary.miny + 1)
    inner_size = bounding_box_size - outer_plus_boundary_size
    return inner_size + boundary_size

def find_bounding_box(grid: set[(int, int)]) -> Boundary:
    minx = miny = 0
    maxx = maxy = 0
    for x,y in grid:
        minx = min(minx, x)
        maxx = max(maxx, x)
        miny = min(miny, y)
        maxy = max(maxy, y)
    return Boundary(
        minx=minx-1,
        maxx=maxx+1,
        miny=miny-1,
        maxy=maxy+1,
    )

def floodfill(outline: set[(int, int)], boundary: Boundary, start: (int, int)) -> set[(int, int)]:
    filled = set(outline)
    frontier = set([start])
    while frontier:
        new_frontier = set()
        for x,y in frontier:
            filled.add((x,y))
            for p2 in [(x+1, y), (x-1, y), (x, y-1), (x, y+1)]:
                if p2 not in filled and boundary.inside(p2) and p2 not in outline:
                    new_frontier.add(p2)
        frontier = new_frontier

    # for y in range(boundary.miny, boundary.maxy + 1):
    #     for x in range(boundary.minx, boundary.maxx + 1):
    #         print('#' if (x,y) in filled else '.', end='')
    #     print()
    return filled

data1, data2 = read_data()
print(volume(data1))
print(volume(data2))
