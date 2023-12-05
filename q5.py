from dataclasses import dataclass
from bisect import bisect_right
from typing import Optional

FOREVER = -1

@dataclass
class Range:
    start: int
    length: int

@dataclass
class Region:
    source: int
    destination: int
    length: int

    def intersect_destinations(self, r: Range) -> Optional[Range]:
        start = max(r.start, self.source)
        end = min(r.start + r.length, self.source + self.length) - 1
        if start > end:
            return None
        assert start >= self.source
        offset = start - self.source
        length = end - start + 1
        assert length > 0
        return Range(start=self.destination + offset, length=length)

class Map:
    def __init__(self):
        self._projection: list[Region] = []

    def project_destination_ranges(self, r: Range) -> list[Range]:
        intersect = [ p.intersect_destinations(r) for p in self._projection ]
        return [ i for i in intersect if i is not None ]

    def insert(self, region: Region):
        self._projection.append(region)

    def freeze(self):
        self._projection.sort(key=lambda x: x.source)
        if not self._projection:
            self._projection.append(Region(0, 0, FOREVER))
            return

        if self._projection[0].source != 0:
            length = self._projection[0].source
            self._projection.insert(0, Region(source=0, destination=0, length=length))

        missing = []
        for i in range(1, len(self._projection)):
            pre = self._projection[i-1]
            o = self._projection[i]

            if pre.source + pre.length + 1 < o.source:
                start = pre.source + pre.length
                length = o.source - start
                missing.append(Region(source=start, destination=start, length=length))

        if self._projection[-1].length != FOREVER:
            last = self._projection[-1]
            start = last.source + last.length
            missing.append(Region(source=start, destination=start, length=FOREVER))

        self._projection.extend(missing)
        self._projection.sort(key=lambda x: x.source)

        # sanity check
        pre = None
        for r in self._projection:
            if pre is not None:
                assert pre.source + pre.length == r.source
            pre = r

    def destination(self, source: int) -> int:
        index = bisect_right(self._projection, source, key=lambda x: x.source) - 1
        if 0 <= index < len(self._projection):
            projection = self._projection[index]
            assert projection.source <= source
            if source < projection.source + projection.length:
                offset = source - projection.source
                return projection.destination + offset
        return source

class Data:
    seeds: list[int] = list()
    seed_to_soil: Map = Map()
    soil_to_fertiliser: Map = Map()
    fertiliser_to_water: Map = Map()
    water_to_light: Map = Map()
    light_to_temperature: Map = Map()
    temperature_to_humidity: Map = Map()
    humidity_to_location: Map = Map()

    def freeze(self):
        self.seed_to_soil.freeze()
        self.soil_to_fertiliser.freeze()
        self.fertiliser_to_water.freeze()
        self.water_to_light.freeze()
        self.light_to_temperature.freeze()
        self.temperature_to_humidity.freeze()
        self.humidity_to_location.freeze()

    def seed_to_location(self, seed: int) -> int:
        soil = self.seed_to_soil.destination(seed)
        fertiliser = self.soil_to_fertiliser.destination(soil)
        water = self.fertiliser_to_water.destination(fertiliser)
        light = self.water_to_light.destination(water)
        temperature = self.light_to_temperature.destination(light)
        humidity = self.temperature_to_humidity.destination(temperature)
        return self.humidity_to_location.destination(humidity)

    def min_projection(self, seed_ranges: list[Range]) -> int:
        levels = [
            self.seed_to_soil,
            self.soil_to_fertiliser,
            self.fertiliser_to_water,
            self.water_to_light,
            self.light_to_temperature,
            self.temperature_to_humidity,
            self.humidity_to_location,
        ]

        ranges = seed_ranges
        for level in levels:
            new_ranges = []
            for r in ranges:
                new_ranges.extend(level.project_destination_ranges(r))
            ranges = new_ranges
        ranges.sort(key=lambda x: x.start)
        return ranges[0].start

def get_data() -> Data:
    data = Data()
    with open('input5.txt') as f:
        category: Map = None
        for line in f.read().split('\n'):
            line = line.strip()
            if not line:
                continue

            if '0' <= line[0] <= '9':
                destination, source, length = map(int, line.split(" "))
                category.insert(Region(source=source, destination=destination, length=length))

            elif line.startswith("seeds:"):
                for seed in line[len("seeds:"):].strip().split(" "):
                    data.seeds.append(int(seed))
            elif line.startswith("seed-to-soil"):
                category = data.seed_to_soil
            elif line.startswith("soil-to-fertilizer"):
                category = data.soil_to_fertiliser
            elif line.startswith("fertilizer-to-water"):
                category = data.fertiliser_to_water
            elif line.startswith("water-to-light"):
                category = data.water_to_light
            elif line.startswith("light-to-temperature"):
                category = data.light_to_temperature
            elif line.startswith("temperature-to-humidity"):
                category = data.temperature_to_humidity
            elif line.startswith("humidity-to-location"):
                category = data.humidity_to_location
            else:
                raise AssertionError(f"unexpected format: {line}")
    data.freeze()
    return data

class Min:
    def __init__(self):
        self.min = None

    def add(self, candidate: int):
        self.min = candidate if self.min is None else min(self.min, candidate)

data = get_data()
min_location = Min()
for seed in data.seeds:
    min_location.add(data.seed_to_location(seed))
print(min_location.min)

seed_ranges = []
for i in range(0, len(data.seeds), 2):
    start, length = data.seeds[i:i+2]
    seed_ranges.append(Range(start=start, length=length))

print(data.min_projection(seed_ranges=seed_ranges))
