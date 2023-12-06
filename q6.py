from dataclasses import dataclass

@dataclass
class Record:
    time: int
    distance: int

def read_data() -> (list[Record], Record):
    with open('input6.txt') as f:
        times = distances = None
        ctime = cdistance = None
        for line in f.read().split('\n'):
            line = line.strip()
            if not line:
                continue
            action, values = line.split(':')
            action = action.strip().lower()
            combined = int(values.replace(' ', ''))
            values = [ int(x.strip()) for x in values.split(' ') if x.strip() ]
            if action == 'time':
                assert not times
                times = values
                ctime = combined
            elif action == 'distance':
                assert not distances
                distances = values
                cdistance = combined
            else:
                raise AssertionError(f'unknown action {action}')
        assert len(times) == len(distances)
        combined = Record(time=ctime, distance=cdistance)
        return [ Record(time=time, distance=distance) for time, distance in zip(times, distances) ], combined

def check(target_speed: int, r: Record) -> bool:
    race_time = r.time - target_speed
    distance = race_time * target_speed
    return distance > r.distance

def search(lo: int, hi: int, r: Record, target: bool) -> int:
    v = (lo + hi) // 2
    # print(f'search {lo} - ({v}) - {hi} for {target}')
    if check(v, r) == target:
        if check(v-1, r) != target:  # we found the start of the target-valued run!
            return v
        else: #  we're somewhere in the middle of right section, so search left
            return search(lo, v, r, target)

    else:  # we're in the wrong section, search right
        return search(v, hi, r, target)
        

def get_winning_combos(r: Record) -> int:
    # TODO(tim) this seems like a hack, but it works:
    # winning combos for Record(time=42, distance=284): [(False, 7, 8), (True, 9, 33), (False, 34)]
    # winning combos for Record(time=68, distance=1005): [(False, 15, 21), (True, 22, 46), (False, 47)]
    # winning combos for Record(time=69, distance=1122): [(False, 17, 26), (True, 27, 42), (False, 43)]
    # winning combos for Record(time=85, distance=1341): [(False, 16, 20), (True, 21, 64), (False, 65)]
    split = r.time // 2 

    start = search(0, split, r, True)
    end = search(split, r.time, r, False)
    return end - start

# def og_get_winning_combos(r: Record) -> int:
#     seq = []
#     current = None
#     combos = 0
#     speed = int(r.distance / r.time)
#     while speed < r.time:
#         speed += 1
#         race_time = r.time - speed
#         distance = race_time * speed
#         success = False
#         if distance > r.distance:
#             success = True
#             combos += 1

#         if not current or current[0] != success:
#             if current:
#                 current_success, start = current
#                 seq.append((current_success, start, speed - 1))
#             current = (success, speed)
#     if current:
#         seq.append(current)

#     print(f'winning combos for {r}: {seq}')
#     return combos

data, combined = read_data()

combos = [ get_winning_combos(r) for r in data ]
combo_product = 1
for c in combos:
    combo_product *= c
print(combo_product)
assert combo_product == 440000

single = get_winning_combos(combined)
print(single)

assert single == 26187338
