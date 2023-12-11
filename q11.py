def read_data() -> list[str]:
    galaxy = []
    with open('input11.txt') as f:
        for line in f.read().split('\n'):
            line = line.strip()
            if not line:
                continue
            galaxy.append(line)
    return galaxy

def expand(galaxy: list[str], factor) -> list[(int, int)]:
    height = len(galaxy)
    width = len(galaxy[0])
    rows = set(range(height))
    cols = set(range(width))
    row = 0
    for line in galaxy:
        col = 0
        for c in line:
            if c == '#':
                rows.discard(row)
                cols.discard(col)
            col += 1
        row += 1

    row_lookup = {}
    col_lookup = {}

    count = 0
    for row in range(height):
        if row in rows:
            count += 1
        row_lookup[row] = count
    
    count = 0
    for col in range(width):
        if col in cols:
            count += 1
        col_lookup[col] = count

    galaxies = find_galaxies(galaxy)

    expanded = []
    factor -= 1
    for row, col in galaxies:
        row2 = row + factor * row_lookup[row]
        col2 = col + factor * col_lookup[col]
        expanded.append((row2, col2))

    return expanded

def find_galaxies(galaxy):
    galaxies = []
    for row, line in enumerate(galaxy):
        for col, c in enumerate(line):
            if c == '#':
                galaxies.append((row, col))
    return galaxies

def sum_shortest(galaxies) -> int:
    if not galaxies:
        return 0

    start = galaxies[0]
    sum = 0
    for i in range(1, len(galaxies)):
        end = galaxies[i]
        sum += find_shortest_path(start, end)
    sum += sum_shortest(galaxies[1:])
    return sum

# just Manhattan
def find_shortest_path(start, end) -> int:
    sr, sc = start
    er, ec = end
    return abs(sr - er) + abs(sc - ec)

galaxy = read_data()
print(sum_shortest(expand(galaxy, 2)))
print(sum_shortest(expand(galaxy, 1_000_000)))
