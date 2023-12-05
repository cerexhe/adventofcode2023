from typing import Union, Tuple

_SYMBOLS = set(r'~!@#$%^&*()_+`-=<>,/?;:"\\|\'{[]}')

def check_surrounds(data: list[str], x1: int, y1: int, x2: int) -> Union[bool, Tuple[int, int]]:
    x1 = max(0, x1)
    y1 = max(0, y1)
    y2 = min(y1+3, len(data))
    # print(f'clamped x{x1}, y{y1}-{y2}')

    for y in range(y1, y2):
        line = data[y]
        x2 = min(x2, len(line))
        # print(f'x3 clamp {x2}')
        for x in range(x1, x2):
            c = line[x]
            if c == '.':
                continue
            if c == '*':
                return (x, y)
            if c in _SYMBOLS:
                return True

    return False

with open('input3.txt') as f:
    data = f.read().split('\n')

# data = data[0:2]

parts_sum = 0
possible_gears = {}
for y in range(len(data)):
    line = data[y]
    # print('line', y)
    x = 0
    while x < len(line):
        num = 0
        start = x - 1
        end = x + 1
        while x < len(line) and '0' <= line[x] <= '9':
            num *= 10
            num += ord(line[x]) - ord('0')
            x += 1
            end += 1
        assert (num != 0) == (end != start + 2)
        # if num:
            # print(num)

        if num:
            res = check_surrounds(data, start, y-1, end)
            if not res:
                continue

            parts_sum += num
            if res != True:
                if res not in possible_gears:
                    possible_gears[res] = []
                possible_gears[res].append(num)

        x += 1

gear_ratio = 0
for connected in possible_gears.values():
    assert len(connected) <= 2
    if len(connected) == 2:
        a, b = connected
        gear_ratio += a * b

print(parts_sum)
print(gear_ratio)