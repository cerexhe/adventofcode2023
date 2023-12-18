def read_data() -> list[str]:
    cases = []
    with open('input15.txt') as f:
        for line in f.read().split('\n'):
    #for line in ['rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7']:
            line = line.strip()
            if not line:
                continue
            for case in line.split(','):
                cases.append(case)
    return cases

def compute_hash(s) -> int:
    num = 0
    for c in s:
        num += ord(c)
        num = (num * 17) % 256
    return num

class Lens:
    label: str
    power: int

    def __init__(self, label: str, power: int):
        self.label = label
        self.power = power

    def __str__(self) -> str:
        return f"{self.label}={self.power}"

class Box:
    lenses: list[Lens]
    labels: set[str]

    def __init__(self):
        self.lenses = []
        self.labels = set()

    def __str__(self) -> str:
        return ", ".join(map(str, self.lenses))

    def rm_by_label(self, label: str):
        if label in self.labels:
            self.labels.remove(label)
            i = next(i for i,l in enumerate(self.lenses) if l.label == label)
            l = self.lenses[i]
            del self.lenses[i]

    def add(self, label: str, power: int):
        if label in self.labels:
            # replace existing label
            i = next(i for i,l in enumerate(self.lenses) if l.label == label)
            l = self.lenses[i]
            l.power = power
        else:
            self.labels.add(label)
            self.lenses.append(Lens(label, power))

def show(boxes: list[Box]):
    for num, box in enumerate(boxes):
        if box.lenses:
            print(f'{num}: {box}')

def focus(data: list[str]) -> int:
    boxes = [ Box() for _ in range(256) ]

    for s in data:
        if '=' in s:
            label, power = s.split('=')
            power = int(power)
            h = compute_hash(label)
            box = boxes[h]
            box.add(label, power)
        else:
            assert s[-1] == '-'
            label = s[:-1]
            h = compute_hash(label)
            box = boxes[h]
            box.rm_by_label(label)
        #show(boxes)

    power = 0
    for box_num, box in enumerate(boxes):
        mul = box_num + 1
        box_focus = 0
        for slot_num, lens in enumerate(box.lenses):
            box_focus += (slot_num + 1) * lens.power
        power += mul * box_focus
    return power

data = read_data()
print(sum([ compute_hash(s) for s in data ]))
print(focus(data))
