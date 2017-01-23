file = open('demogame.txt', 'r')
out = open('filtered.txt', 'w')
for line in file:
	arr = list(filter(lambda x: '.' not in x, line.replace('\n', '').split(' ')))
	for move in arr:
		move = move.replace('x', '-')
		out.write(move + '\n')