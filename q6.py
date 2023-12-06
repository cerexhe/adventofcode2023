import math
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

def get_winning_combos(r: Record) -> int:
    speed = int(r.distance / r.time)
    combos = 0
    while speed < r.time:
        speed += 1
        race_time = r.time - speed
        distance = race_time * speed
        if distance > r.distance:
            combos += 1
    #print(r, '=', combos)
    return combos

data, combined = read_data()

combos = [ get_winning_combos(r) for r in data ]
combo_product = 1
for c in combos:
    combo_product *= c
print(combo_product) #, '(expect 288)')
print(get_winning_combos(combined))
