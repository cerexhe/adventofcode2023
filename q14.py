from dataclasses import dataclass

@dataclass
class World:
    width: int
    height: int
    fixed: set()
    rolling: set[tuple[int, int]]

    def freeze(self) -> tuple[tuple[int, int]]:
        return tuple(self.rolling)

    def tilt(self, dx: int , dy: int) -> "World":
        changed = True
        while changed:
            changed = False
            for x,y in self.rolling:
            # for x,y in sorted(self.rolling, key=cmp): # TODO(tim) do some ordering heuristics to speed this up?
                x2 = x + dx
                y2 = y + dy
                coord = (x2, y2)
                if 0 <= x2 < self.width and 0 <= y2 < self.height and coord not in self.fixed and coord not in self.rolling:
                    self.rolling.remove((x, y))
                    self.rolling.add(coord)
                    changed = True

def read_data() -> World:
    width = 0
    fixed = set()
    rolling = set()
    with open('input14.txt') as f:
        y = 0
        for line in f.read().split('\n'):
            line = line.strip()
            if not line:
                continue
            width = max(width, len(line))
            for x, char in enumerate(line):
                if char == '#':
                    fixed.add((x, y))
                elif char == 'O':
                    rolling.add((x, y))
            y += 1
    return World(
        width=width,
        height=y,
        fixed=fixed,
        rolling=rolling,
    )

def compute_load(world: World) -> int:
    load = 0
    for (_, y) in data.rolling:
        multiplier = world.height - y
        load += multiplier
    return load

def compute_spin(data: World, count: int) -> int:
    path = []
    lookup = {}
    for i in range(count):
        path.append(compute_load(data))
        t = data.freeze()
        lookup[t] = i
        data.tilt(0, -1)
        data.tilt(-1, 0)
        data.tilt(0, 1)
        data.tilt(1, 0)
        t = data.freeze()
        if t in lookup:
            num_iterations = i + 1
            index = lookup[t]
            loop_length = num_iterations - index
            # first loop after 179 num_iterations - index 109 = 70 loop length
            # target num_iterations = 230, since (1e9 - 230) % 70 == 0
            # print('found loop', num_iterations, '-', index, '=', loop_length)
            # print(f"({count} - {num_iterations}) % {loop_length} == {(count - num_iterations) % loop_length}")
            pending = (count - num_iterations) % loop_length
            # print(f"({count} - {num_iterations + pending}) % {loop_length} == {(count - (num_iterations + pending)) % loop_length} for pending = {pending}")

            # for i,p in enumerate(path):
            #     print(i, ':', p)

            target = index + pending
            return path[target]

    return compute_load(data)

data = read_data()
data.tilt(0, -1)
print(compute_load(data))
print(compute_spin(data, int(1e9)))
