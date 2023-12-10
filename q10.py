import math
from enum import Enum

Node = (int, int)

class Tile(str, Enum):
    VERTICAL = '|'
    HORIZONTAL = '-'
    NE = 'L'
    NW = 'J'
    SW = '7'
    SE = 'F'
    GROUND = '.'
    START = 'S'

def read_data() -> (Node, list[list[Tile]]):
    with open('input10.txt') as f:
        graph = []
        start = None
        row = 0
        for line in f.read().split('\n'):
            line = line.strip()
            if not line:
                continue
            line = [ Tile(c) for c in line ]
            if Tile.START in line:
                col = line.index(Tile.START)
                assert not start
                start = (col, row)
            graph.append(line)
            row += 1
        return start, graph

def find_neighbours(start, graph):
    col, row = start
    tile = graph[row][col]
    if tile == Tile.START: # unclear, reverse search neighbours
        candidates = []
        for x in range(-1, 2):
            for y in range(-1, 2):
                if (x != 0 or y != 0) and 0 <= row + y < len(graph) and 0 <= col + x < len(graph[0]):
                    candidate = (col + x, row + y)
                    if start in find_neighbours(candidate, graph):
                        candidates.append(candidate)
        return candidates
    elif tile == Tile.VERTICAL:
        return [(col, row-1), (col, row+1)]
    elif tile == Tile.HORIZONTAL:
        return [(col-1, row), (col+1, row)]
    elif tile == Tile.NE:
        return [(col, row-1), (col+1, row)]
    elif tile == Tile.NW:
        return [(col, row-1), (col-1, row)]
    elif tile == Tile.SW:
        return [(col, row+1), (col-1, row)]
    elif tile == Tile.SE:
        return [(col, row+1), (col+1, row)]
    else:
        assert tile == Tile.GROUND
        return []

def ground_neighbours(prior, current, graph, loop) -> (list[Node], list[Node]):
    acol, arow = prior
    col, row = current
    tile = graph[row][col]
    lefts = []
    rights = []

    if tile == Tile.START: # HACK: we'll fix this with a floodfill from a neighbour instead
        pass
    elif tile == Tile.VERTICAL:
        l = (col-1, row)
        r = (col+1, row)
        if arow < row:
            l, r = r, l
        lefts.append(l)
        rights.append(r)
    elif tile == Tile.HORIZONTAL:
        l = (col, row-1)
        r = (col, row+1)
        if acol > col:
            l, r = r, l
        lefts.append(l)
        rights.append(r)
    elif tile == Tile.NE:
        l = [(col-1, row), (col-1, row+1), (col, row+1)]
        r = [(col+1, row-1)]
        if arow < row:
            l, r = r, l
        lefts.extend(l)
        rights.extend(r)
    elif tile == Tile.NW:
        l = [(col-1, row-1)]
        r = [(col+1, row), (col+1, row+1), (col, row+1)]
        if arow < row:
            l, r = r, l
        lefts.extend(l)
        rights.extend(r)
    elif tile == Tile.SW:
        l = [(col-1, row+1)]
        r = [(col+1, row), (col+1, row-1), (col, row-1)]
        if acol < col:
            l, r = r, l
        lefts.extend(l)
        rights.extend(r)
    elif tile == Tile.SE:
        l = [(col-1, row), (col-1, row-1), (col, row-1)]
        r = [(col+1, row+1)]
        if acol > col:
            l, r = r, l
        lefts.extend(l)
        rights.extend(r)
    else:
        assert tile == Tile.GROUND
        return []

    lefts =  [ n for n in lefts if n not in loop ]
    rights =  [ n for n in rights if n not in loop ]
    return lefts, rights


def is_boundary(node, graph) -> bool:
    col, row = node
    return col == 0 or row == 0 or row == len(graph) - 1 or col == len(graph[0]) - 1

def in_boundary(node, graph) -> bool:
    col, row = node
    return (0 <= row < len(graph) and 0 <= col < len(graph[0]))

def cycle_len(start: Node, graph: list[list[Tile]], seen: set[Node], lefts: set[Node], rights: set[Node], the_path = [], loop = set()) -> int:
    path_len = 0
    seen.add(start)
    the_path.append(start)

    def compute_ground(n):
        l, r = ground_neighbours(start, n, graph, loop)
        for node in l:
            lefts.add(node)
        for node in r:
            rights.add(node)

    while True:
        neighbours = find_neighbours(start, graph)
        n = [ n for n in neighbours if n not in seen ]

        if not n:
            return path_len
        if len(n) == 1:
            compute_ground(n[0])
            start = n[0]
            path_len += 1
            seen.add(start)
            the_path.append(start)
        else:
            best = []
            for n in neighbours:
                compute_ground(n)
                seen.add(n)
                a_path = []
                path = cycle_len(n, graph, seen, lefts, rights, a_path) + 1
                path_len = max(path, path_len)
                if path_len == path:
                    best = a_path
            the_path.extend(best)
            return path_len

def floodfill(all_nodes, graph, loop):
    wavefront = all_nodes
    new_wavefront = set()
    while True:
        for node in wavefront:
            col, row = node
            for x in range(-1, 2):
                for y in range(-1, 2):
                    new_node = (col+x, row+y)
                    if new_node not in all_nodes and in_boundary(new_node, graph) and new_node not in loop:
                        new_wavefront.add(new_node)

        if not new_wavefront:
            return all_nodes
        for node in new_wavefront:
            all_nodes.add(node)
        wavefront = new_wavefront
        new_wavefront = set()

def extrapolate_right(c):
    if c in (Tile.HORIZONTAL, Tile.NE, Tile.SE):
        return Tile.HORIZONTAL
    return Tile.GROUND

def extrapolate_down(c):
    if c in (Tile.VERTICAL, Tile.SE, Tile.SW):
        return Tile.VERTICAL
    return Tile.GROUND

def explode(graph, loop):
    l2 = set([ (x*2, y*2) for (x, y) in loop ])
    g2 = []
    last = None
    for line in graph:
        if not last:
            last = line
        new_line = []
        for c in line:
            new_line.append(c)
            new_line.append(extrapolate_right(c))
        g2.append(new_line)
        g2.append([ extrapolate_down(c) for c in new_line ])
    return g2

def print_graph(graph, barrier = set(), path = set()):
    row = 0
    for line in graph:
        proc = ''
        col = 0
        for c in line:
            c = c.value
            index = (col, row)
            if index in barrier:
                proc += f'\033[31m{c}\033[0m'
            elif index in path:
                proc += f'\033[34m{c}\033[0m'
            else:
                proc += c
            col += 1
        row += 1
        print(proc)

start, graph = read_data()
the_path = []
print(math.ceil(cycle_len(start, graph, set(), set(), set(), the_path, set()) / 2))
lefts = set()
rights = set()
loop = set(the_path)
cycle_len(start, graph, set(), lefts, rights, [], loop)

exploded = explode(graph, loop)
exploded_path = []
s2 = (2 * start[0], 2 * start[1])
cycle_len(s2, exploded, set(), set(), set(), exploded_path, set())
exploded_lefts = set()
exploded_rights = set()
exploded_loop = set(exploded_path)
cycle_len(s2, exploded, set(), exploded_lefts, exploded_rights, [], exploded_loop)

exploded_barrier = set([(0, 0)]) # HACK should search perimeter
floodfill(exploded_barrier, exploded, exploded_loop)

barrier = set([ (x//2, y//2) for (x, y) in exploded_barrier ])
# print_graph(graph, barrier, loop)
# print_graph(exploded, exploded_barrier, exploded_loop)

barrier_and_loop = set()
for n in loop:
    barrier_and_loop.add(n)
for n in barrier:
    barrier_and_loop.add(n)

enclosed = len(graph) * len(graph[0]) - len(barrier_and_loop)
print(enclosed)

