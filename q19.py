import functools
import re
from dataclasses import dataclass
from typing import Optional

RULE_PATTERN = re.compile(r'^(?P<name>[^{]+)[{](?P<rules>[^}]+)[}]$')
STEP_PATTERN = re.compile(r'^(?P<name>[^<>]+)(?P<op>[<>])(?P<value>\d+)[:](?P<target>.*)$')

@dataclass
class Lt:
    label: str
    key: str
    value: int

    def __call__(self, p) -> Optional[str]:
        return self.label if p[self.key] < self.value else None

@dataclass
class Gt:
    label: str
    key: str
    value: int

    def __call__(self, p) -> Optional[str]:
        return self.label if p[self.key] > self.value else None

@dataclass
class Raw:
    label: str

    def __call__(self, p) -> Optional[str]:
        return self.label

def read_data():
    rules = {}
    parts = []
    with open("./input19.txt") as f:
    #with open("./baby19.txt") as f:
        getting_rules = True
        for line in f.read().split('\n'):
            line = line.strip()
            if not line:
                getting_rules = False
                continue

            if getting_rules:
                m = RULE_PATTERN.match(line)
                assert m
                name = m.group('name')
                stages = []
                rules[name] = stages
                for raw in m.group('rules').split(','):
                    m = STEP_PATTERN.match(raw)
                    if m:
                        arg = m.group('name')
                        op = m.group('op')
                        value = int(m.group('value'))
                        target = m.group('target')

                        if op == '<':
                            stage = Lt(target, arg, value)
                        else:
                            assert op == '>'
                            stage = Gt(target, arg, value)
                    else:
                        assert not any(c in raw for c in [':', '>', '<'])
                        stage = Raw(raw)
                    stages.append(stage)

            else:
                assert line[0] == '{' and line[-1] == '}'
                line = line[1:-1]
                part = {}
                for bit in line.split(','):
                    name, val = bit.split('=')
                    part[name] = int(val)

                parts.append(part)

    return rules, parts

def accepted(rules, part) -> bool:
    rule = rules['in']
    #print('in', end='')
    while True:
        for stage in rule:
            label = stage(part)
            if label is None:
                continue
            if label == 'A':
                #print(' --> A')
                return True
            if label == 'R':
                #print(' --> R')
                return False
            #print(f' --> {label}', end='')
            rule = rules[label]
            break

INDEX = {
    'x': 0,
    'm': 1,
    'a': 2,
    's': 3,
}

def total_accepted(rules) -> int:
    initial = (1, 4000) * 4
    return rule_accepted('in', initial)

def score(rng) -> int:
    l0,h0, l1,h1, l2,h2, l3,h3 = rng
    return (h0 - l0 + 1) * (h1 - l1 + 1) * (h2 - l2 + 1) * (h3 - l3 + 1)

# hack: use rules in scope because it's not cacheable :|
@functools.cache
def rule_accepted(label, rng) -> int:
    count = 0
    for stage in rules[label]:
        l0,h0, l1,h1, l2,h2, l3,h3 = rng
        if l0 > h0 or l1 > h1 or l2 > h2 or l3 > h3:
            break

        if isinstance(stage, Lt):
            i = 2 * INDEX[stage.key]
            lo = rng[i]
            hi = stage.value - 1
            r2 = list(rng)
            r2[i+1] = hi
            r2 = tuple(r2)
            if lo <= hi:
                if stage.label == 'A':
                    count += score(r2)
                elif stage.label != 'R':
                    count += rule_accepted(stage.label, r2)
            rng = list(rng)
            rng[i] = stage.value
            rng = tuple(rng)
        elif isinstance(stage, Gt):
            i = 2 * INDEX[stage.key]
            lo = stage.value + 1
            hi = rng[i+1]
            r2 = list(rng)
            r2[i] = lo
            r2 = tuple(r2)
            if lo <= hi:
                if stage.label == 'A':
                    count += score(r2)
                elif stage.label != 'R':
                    count += rule_accepted(stage.label, r2)
            rng = list(rng)
            rng[i+1] = stage.value
            rng = tuple(rng)
        else:
            assert isinstance(stage, Raw)
            if stage.label == 'A':
                count += score(rng)
            elif stage.label != 'R':
                count += rule_accepted(stage.label, rng)
            break
    return count

rules, parts = read_data()
print(sum([ sum(p.values()) for p in parts if accepted(rules, p) ]))
print(total_accepted(rules))
