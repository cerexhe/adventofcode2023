import functools
 
def read_data() -> list[str]:
    lines = []
    with open('input12.txt') as f:
        for line in f.read().split('\n'):
            line = line.strip()
            if not line:
                continue
            lines.append(line)
    return lines

def combos(line: str, unfold=1) -> int:
    damaged, counts = line.split(' ', maxsplit=1)
    damaged = '?'.join([damaged] * unfold)
    counts = tuple([ int(c) for c in counts.split(',') ]) * unfold
    num = check(damaged, counts)
    assert num > 0
    return num

@functools.cache
def check(damaged: str, counts: tuple) -> int:
    if not counts:
        return 0 if '#' in damaged else 1

    if not damaged:
        return 1 if not counts else 0

    if damaged[0] == '.':
        return check(damaged[1:], counts)

    if damaged[0] == '#':
        if not counts:
            return 0
        assert counts[0] > 0
        if counts[0] > len(damaged):
            return 0
        for i in range(counts[0]):
            if damaged[i] == '.':
                return 0
        i += 1
        if i < len(damaged) and damaged[i] == '#':
            return 0
        return check(damaged[i+1:], counts[1:])

    assert damaged[0] == '?'

    yes = check('#' + damaged[1:], counts)
    no = check('.' + damaged[1:], counts)
    return yes + no

assert combos('???.### 1,1,3') == 1
assert combos('.??..??...?##. 1,1,3') == 4
assert combos('?#?#?#?#?#?#?#? 1,3,1,6') == 1
assert combos('????.#...#... 4,1,1') == 1
assert combos('????.######.#####. 1,6,5') == 4
assert combos('?###???????? 3,2,1') == 10
assert combos('.?#?#.?..#? 3,1') == 1
assert combos('#???#?.????????? 1,3,1,1,1') == 70
assert combos('.#????#?## 1,6') == 1
 
lines = read_data()
print(sum([ combos(line) for line in lines ]))
print(sum([ combos(line, unfold=5) for line in lines ]))
