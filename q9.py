def read_data():
	seqs = []
	with open('input9.txt') as f:
		for line in f.read().split('\n'):
			s = [ x.strip() for x in line.split(' ') ]
			s = [ int(x) for x in s if x ]
			seqs.append(s)
	return seqs

def extrapolate(seq, where, order):
	expanded = expand([seq], order)
	first = last = 0
	for row in range(len(expanded)-2, -1, -1):
		last += expanded[row][where]
		first = expanded[row][where] - first
	return last if order > 0 else first
	
def expand(seqs, order):
	if not seqs[-1] or set(seqs[-1]) == set([0]):
		return seqs
	
	add = []
	last = None
	s = seqs[-1]
	if order < 0:
		s = reversed(s)
	for num in s:
		if last is not None:
			add.append((num - last) * order)
		last = num
	
	if not add:
		return seqs
	if order < 0:
		seqs.append(list(reversed(add)))
	else:
		seqs.append(add)
	return expand(seqs, order)

data = read_data()
print(sum([ extrapolate(s, -1, 1) for s in data ]))
print(sum([ extrapolate(s, 0, -1) for s in data ]))
