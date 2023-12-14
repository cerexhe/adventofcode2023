def load_data():
    worlds = []
    with open('input13.txt') as f:
        world = []
        for line in f.read().split('\n'):
            line = line.strip()
            if not line:
                if world:
                    worlds.append(world)
                    world = []
                continue

            world.append(line)
        if world:
            worlds.append(world)
    return worlds
 
def transpose(world: list[str]) -> list[str]:
    w2 = ['' for x in range(len(world[0])) ]
    for row in world:
        for x, c in enumerate(row):
            w2[x] += c
    return w2
 
def score(world: list[str], smudges: int) -> int:
    h = score_horizontal(world, smudges)

    world = transpose(world)
    v = score_horizontal(world, smudges)
    assert h or v
    if h and v:
        if h > v:
            return h * 100
        return v
    elif h:
        return h * 100
    return v
 
def score_horizontal(world, smudges: int) -> int:
    assert len(world) > 1
    best = None
    for y in range(len(world)):
        for i in range(1, len(world)):
            start = max(0, y-i+1)

            end = y+1+i
            if len(world[start:y+1]) != len(world[y+1:end]):
                continue
                 
            first = (world[start:y+1])
            second = list(reversed(world[y+1:end]))
            diff = sum([ 1 if a != b else 0 for (a,b) in zip(''.join(first), ''.join(second)) ])

            if diff != smudges:
                continue
            if y-i+1 <= 0 or end >= len(world):
                if best is None or y+1 > best:
                    best = y+1
    return best
 
 
worlds = load_data()
print(sum([ score(world, smudges=0) for world in worlds ]))
print(sum([ score(world, smudges=1) for world in worlds ]))
