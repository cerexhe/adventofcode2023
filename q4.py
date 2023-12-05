import functools

def read():
    data = []
    with open('input4.txt') as f:
        for line in f.read().split('\n'):
            if not line.strip():
                continue
            _, rest = line.split(':', maxsplit=1)
            winning, have = rest.split('|')
            winning = set([int(x.strip()) for x in winning.split(' ') if x.strip() ])
            have = set([int(x.strip()) for x in have.split(' ') if x.strip() ])
            data.append((winning, have))
    return data

data = read()

card_points = []
card_multipliers = []
row = 0
for winning, have in data:
    intersection = len(winning.intersection(have))
    row_points = int(2**(intersection-1))

    end = row + intersection
    while len(card_points) <= end:
        card_points.append(0)
        card_multipliers.append(0)

    card_points[row] = row_points
    card_multipliers[row] = intersection

    row += 1

@functools.cache
def count(row: int) -> int:
    points = 1
    for i in range(row+1, row+card_multipliers[row]+1):
        points += count(i)
    return points

# points2 = sum([ x*y for x, y in zip(card_points, card_multipliers)])

total_count = [ count(i) for i in range(len(card_points)) ]

print(sum(card_points))
print(sum(total_count))