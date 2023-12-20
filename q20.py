import math
from typing import Any

class Sequencer:
    def __init__(self, node_lookup: dict[str, Any]):
        self.node_lookup = node_lookup
    
    def reset(self):
        for n in self.node_lookup.values():
            n.reset()

    def press_button(self, num_times: int) -> (int, int):
        num_hi = num_lo = 0
        broadcaster = self.node_lookup['broadcaster']
        rx_node = self.node_lookup['rx']
        assert len(rx_node.inputs) == 1
        rx_parent = self.node_lookup[rx_node.inputs[0]]
        rx_ins = {name: 0 for name in rx_parent.input_values.keys()}
        for iteration in range(10000000):
            if iteration == num_times:
                first = num_hi * num_lo
            if all(rx_ins.values()):
                second = math.prod(rx_ins.values())
                assert first
                return first, second

            queue = [('', broadcaster, False)]
            while queue:
                from_name, node, pulse = queue.pop(0)
                if pulse:
                    num_hi += 1
                else:
                    num_lo += 1
                extensions = node(from_name, pulse)
                if node == rx_parent:
                    for n, val in rx_parent.input_values.items():
                        if val:
                            rx_ins[n] = iteration + 1
                queue.extend(extensions)

        assert False

class Rx:
    def __init__(self):
        self.inputs = []

    def reset(self): pass
    def add_input(self, name: str):
        self.inputs.append(name)

    def add_output(self, conn): pass

    def __str__(self) -> str:
        return "empty"

    def __call__(self, from_name: str, hi: bool):
        return []

class FlipFlop:
    def __init__(self, name: str):
        self.name = name
        self.value = False
        self.outputs = []

    def reset(self): pass
    def add_input(self, name: str): pass

    def add_output(self, conn):
        self.outputs.append(conn)

    def __str__(self) -> str:
        return f"%{self.name}"

    def __call__(self, from_name: str, hi: bool):
        if hi:
            return []
        self.value = not self.value
        return [(self.name, c, self.value) for c in self.outputs]

class Conjunction:
    def __init__(self, name):
        self.name = name
        self.outputs = []
        self.input_values = {}
    
    def reset(self):
        for k in self.input_values.keys():
            self.input_values[k] = False

    def add_input(self, name: str):
        self.input_values[name] = False

    def add_output(self, conn):
        self.outputs.append(conn)

    def __str__(self) -> str:
        return f"&{self.name}"

    def __call__(self, from_name: str, hi: bool):
        self.input_values[from_name] = hi
        send_value = not all(self.input_values.values())
        return [(self.name, c, send_value) for c in self.outputs]

class Broadcaster:
    outputs = []

    def __init__(self, name):
        self.name = name

    def reset(self): pass
    def add_input(self, name: str): pass

    def add_output(self, conn):
        self.outputs.append(conn)

    def __str__(self) -> str:
        return self.name

    def __call__(self, from_name: str, value: bool):
        return [(self.name, c, value) for c in self.outputs]

def read_data() -> Sequencer:
    conns = {}
    node_lookup = {}
    # with open('baby20.txt') as f:
    with open('input20.txt') as f:
        for line in f.read().split('\n'):
            line = line.strip()
            if not line:
                continue
            key, destinations = line.split(' -> ')
            destinations = destinations.split(', ')
            tpe = key[0]
            name = key[1:]
            if tpe == '%':
                c = FlipFlop(name)
            elif tpe == '&':
                c = Conjunction(name)
            else:
                assert key == 'broadcaster'
                name = key
                c = Broadcaster(name)

            assert name not in node_lookup
            assert name not in conns
            node_lookup[name] = c
            conns[name] = destinations

    for name, destinations in conns.items():
        f = node_lookup[name]
        for d in destinations:
            t = node_lookup.get(d)
            if not t:
                assert d == "rx"
                assert d not in node_lookup
                t = Rx()
                node_lookup[d] = t

            f.add_output(t)
            t.add_input(name)

    return Sequencer(node_lookup)

seq = read_data()
a, b = seq.press_button(1000)
print(a)
print(b)
