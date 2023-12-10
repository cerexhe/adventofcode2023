import math
import re

MAPPING = re.compile(r'(?P<from>[^\s=]+)\s*=\s*[(](?P<left>[^,]+),\s*(?P<right>[^)]+)[)]\s*')

def read_data():
	with open("./input8.txt") as f:
		path = None
		graph = {}
		for line in f.read().split('\n'):
			line = line.strip()
			if not line:
				continue
			if not path:
				path = line
			else:
				m = MAPPING.match(line)
				assert m
				assert m.group('from') not in graph
				graph[m.group('from')] = (m.group('left'), m.group('right'))
		return path, graph
		
def count(path, graph):
	node = 'AAA'
	steps = 0
	for loop in range(100):
		for c in path:
			l, r = graph[node]
			node = l if c== 'L' else r
			steps += 1
			if node == 'ZZZ':
				return steps
	raise AssertionError('overflow')

def count_ghost(path, graph):
	nodes = [ k for k in graph.keys() if k.endswith('A') ]
	node_steps = [ count_step(path, graph, node) for node in nodes ]
	return math.lcm(*node_steps)
	
def count_step(path, graph, node):
		steps = 0
		seen = set([node])
		node_path = [node]
		phase = None
		loops = set()
		for loop in range(100):
			for c in path:
			  	l, r = graph[node]
			  	node = l if c== 'L' else r
			  	#print(node)
			  	steps += 1
			  	if node.endswith('Z'):
			  		#print('found end', phase)
			  		if not phase:
			  			phase = steps
			  		else:
			  			loops.add(steps)
			  		steps = 0

		loops.add(phase)
		assert len(loops) == 1
		print(phase, loops)
		return phase
	
path, graph = read_data()
print(count(path, graph))
print(count_ghost(path, graph))
