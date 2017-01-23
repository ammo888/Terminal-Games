# USE PYTHON 3
def state():
	print('0:', hanoi[0])
	print('1:', hanoi[1])
	print('2:', hanoi[2])
	print('')

def movelegal(a,b):
	hanoi[b].append(hanoi[a].pop())

	state()

def move(a,b):
	if len(hanoi[a]) != 0:
		if len(hanoi[b]) != 0:
			if hanoi[a][-1] < hanoi[b][-1]:
				movelegal(a,b)
			else:
				print('Can\'t move bigger disk onto smaller one')
		else:
			movelegal(a,b)
		print('Stack is empty')

def solve(s,i,f,b):
	if s == 0:
		return
	solve(s-1,i,b,f)
	movelegal(i,f)
	solve(s-1,b,f,i)

def game():
	global n, play, hanoi

	print('Towers of Hanoi')
	n = int(input('Enter number of disks: '))
	play = int(input('Enter 0 to solve, 1 to play, and anything else to quit: '))
	hanoi = [list(range(n))[::-1],[],[]]

	# Solve
	if play == 0:
		state()
		#solve(n)
		solve(n,0,2,1)
		print('Game completed in',2**n-1,'moves')
	# Play
	elif play == 1:
		count = 0
		print("\033c")
		state()
		while len(hanoi[2]) != n:
			a, b = input("Enter stacks to move disks from and to: ").split()
			print("\033c")
			move(int(a),int(b))
			count += 1
		print('You\'ve completed the game in',count,'moves!')
		print('Optimal number of moves:',2**n-1)
	# Quit
	else:
		print('You\'ve quit the game')

game()	
