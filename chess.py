import sys
import locale
from termcolor import colored, cprint
import numpy as np

print('Terminal Chess')

init = 'rnbqkbnr/pppppppp/        /        /        /        /PPPPPPPP/RNBQKBNR-w'

class chess:
	def __init__(self, initial):
		self.stateinit = initial
		self.state = initial
		self.boardinit = np.array([list(self.stateinit.split('-')[0].split('/')[i]) for i in range(8)])
		self.board = np.copy(self.boardinit)
		self.boardnames = np.array([[chr(97+col) + str(row) for col in range(8)] for row in range(8,0,-1)])
		self.turn = self.state.split('-')[1]

		self.movep = [(1,0)]
		self.movepi = [(2,0)]
		self.movepx = [(1,-1),(1,1)]
		self.moveP = [(-1,0)]
		self.movePi = [(-2,0)]
		self.movePx = [(-1,-1),(-1,1)]
		self.movenN = [(-2,-1),(-2,1),(2,-1),(2,1),(1,2),(-1,2),(1,-2),(-1,-2)]
		self.movebB = [(i,j) for i in list(range(-7,8)) for j in list(range(-7,8)) if abs(i) == abs(j)]
		self.moverR = [(i,j) for i in list(range(-7,8)) for j in list(range(-7,8)) if i == 0 or j == 0]
		self.moveqQ = [(i,j) for i in list(range(-7,8)) for j in list(range(-7,8)) if abs(i) == abs(j) or i == 0 or j == 0]
		self.movekK = [(i,j) for i in list(range(-1,2)) for j in list(range(-1,2)) if abs(i) == abs(j) or i == 0 or j == 0]
		null = (0,0)
		self.movebB.remove(null)
		self.moverR.remove(null)
		self.moveqQ.remove(null)
		self.movekK.remove(null)
		self.moves = []

	def print(self):
		print(colored('  A B C D E F G H   ', 'white', 'on_blue'))
		for row in range(8):
			sys.stdout.write(colored(str(8-row) + ' ', 'white', 'on_blue'))
			for col in range(8):
				txt = colored(self.board[row][col] + ' ', 'white', 'on_grey' if(row + col) % 2 == 0 else None) 
				sys.stdout.write(txt)
			sys.stdout.write(colored(str(8-row) + ' ', 'white', 'on_blue'))
			sys.stdout.write('\n')
		print(colored('  A B C D E F G H   ', 'white', 'on_blue'))
		if self.turn == 'w':
			print('White turn')
		else:
			print('Black turn')

	def move(self, move):
		piece, which, play = self.identify(move)
		print(piece,which,play)
		loc, dest, check = self.islegal(piece, which, play)
		if check:
			self.moves.append([move, loc, dest])
		if len(self.moves) % 2 == 0:
			self.turn = 'w'
		else:
			self.turn = 'b'

	def identify(self, move):
		# Identify piece and the play
		if move[0].isupper():
			piece = move[0]
			play = move[1:]
		else:
			piece = 'P'
			play = move

		# White/Black's turn piece
		if self.turn == 'b':
			piece = piece.lower()

		# If specific rank/file is specified, save info
		which = ''
		if len(play) == 3:
			which = play[0]
			play = play[1:]

		return piece, which, play

	def islegal(self, piece, which, play):
		f = (-1,-1)
		# Find piece(s)
		loc = list(zip(*np.where(self.board == piece)))
		# Find specific piece if specified
		if which != '':
			if not which.isdigit():
				loc = [x for x in loc if x[1] == ord(which) - 97]
			else:
				loc = [x for x in loc if x[0] == 8 - int(which)]
		# Piece not on board
		if not loc:
			print('No such piece found')
			return f, f, False
		# Find destination
		dest = list(zip(*np.where(self.boardnames == play)))
		# Destination doesn't exist
		if not dest:
			print('No such destination')
			return f, f, False
		# Destination exists
		dest = dest[0]
		# Destination character
		destchar = self.board[dest[0]][dest[1]]
		# If destination not empty
		if destchar != ' ':
			# If collision with own team
			if destchar.isupper() == (self.turn == 'w'):
				print('Can\'t move onto own team')
		for l in loc:
			vec = tuple(map(lambda x, y: x - y, dest, l))
			if piece == 'N' or piece == 'n':
				if vec in self.movenN:
					return l, dest, True
			if piece == 'P':
				if vec in self.movePi:
					if l[0] == 6:
						if self.board[dest[0]-1][dest[0]] == ' ':
							return l, dest, True
						else:
							print('Another piece in the way')
							return f, f, False
					else:
						print('Pawn has already moved once')
						return f, f, False
				if vec in self.movePx:
					if destchar != ' ':
						return l, dest, True

				if vec in self.moveP:
					if destchar == ' ':
						return l, dest, True
					else:
						print('Another piece in the way')
			if piece == 'p':
				if vec in self.movepi:
					if l[0] == 1:
						if self.board[dest[0]+1][dest[0]] == ' ':
							return l, dest, True
						else:
							print('Another piece in the way')
							return f, f, False
					else:
						print('Pawn has already moved once')
						return f, f, False
				if vec in self.movepx:
					if destchar != ' ':
						return l, dest, True

				if vec in self.movep:
					if destchar == ' ':
						return l, dest, True
					else:
						print('Another piece in the way')			

		print('Move is not legal')
		return f, f, False

	def update(self):
		self.board = np.copy(self.boardinit)
		for move in self.moves:
			loc = move[1]
			dest = move[2]
			self.board[dest[0]][dest[1]] = self.board[loc[0]][loc[1]]
			self.board[loc[0]][loc[1]] = ' '

game = chess(init)
game.print()
game.move('Ngf3')
game.move('e5')
game.update()
game.print()