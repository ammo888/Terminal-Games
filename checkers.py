import sys
import locale
from termcolor import colored, cprint
import numpy as np
import math
import functools
import itertools
import time


class draughts:

    def __init__(self):
        initial = ' o o o o o/o o o o o / o o o o o/o o o o o /          /          / O O O O O/O O O O O / O O O O O/O O O O O -O'
        self.stateinit = initial
        self.state = initial
        self.boardinit = np.array(
            [list(self.stateinit.split('-')[0].split('/')[i]) for i in range(10)])
        self.board = np.copy(self.boardinit)
        self.boardnames = np.array([[0 if (row + col) & 1 == 0 else math.ceil(
            (10 * row + col + 1) / 2) for col in range(10)] for row in range(10)])
        self.turn = self.state.split('-')[1]
        self.enemy = self.turn.lower()
        self.moves = []
        self.isref = False

    def print(self):
        print("\033c")
        print(colored(' ' * 24, 'white', 'on_blue'))
        for row in range(10):
            sys.stdout.write(colored(' ' * 2, 'white', 'on_blue'))
            for col in range(10):
                c = self.board[row][col]
                textcolor = 'red' if c == 'o' else 'white'
                txt = colored(c + ' ', textcolor,
                              'on_white' if (row + col) & 1 == 0 else None)
                sys.stdout.write(txt)
            sys.stdout.write(colored(' ' * 2, 'white', 'on_blue'))
            sys.stdout.write('\n')
        print(colored(' ' * 24, 'white', 'on_blue'))
        if self.turn == 'O':
            print('White turn')
        else:
            print('Red turn')

    def reference(self):
        print("\033c")
        print(colored(' ' * 24, 'white', 'on_blue'))
        for row in range(10):
            sys.stdout.write(colored(' ' * 2, 'white', 'on_blue'))
            for col in range(10):
                c = self.boardnames[row][col]
                label = ' ' + str(c) if len(str(c)) == 1 else str(c)
                txt = colored(label, 'white', 'on_white' if (
                    row + col) & 1 == 0 else None)
                sys.stdout.write(txt)
            sys.stdout.write(colored(' ' * 2, 'white', 'on_blue'))
            sys.stdout.write('\n')
        print(colored(' ' * 24, 'white', 'on_blue'))

    def move(self, move):
        if move == 'undo':
            self.moves.pop()
        elif move == 'ref':
            self.isref = not self.isref
        else:
            if move == '':
                return
            print(move)
            arr = [int(x) for x in move.split('-')]
            check = self.islegal(arr)
            if check:
                self.moves.append([move] + arr)
        if len(self.moves) & 1 == 0:
            self.turn = 'O'
            self.enemy = 'o'
        else:
            self.turn = 'o'
            self.enemy = 'O'

    def islegal(self, arr):
        for i in range(len(arr)):
            loc = list(zip(*np.where(self.boardnames == arr[i])))[0]
            piece = self.board[loc[0], loc[1]]
            # If starting location
            if i == 0:
                # Check if piece exists there
                if piece != self.turn:
                    print('No men at starting location')
                    return False
            # If not starting locaiton
            else:
                # Previous location
                prevloc = list(
                    zip(*np.where(self.boardnames == arr[i - 1])))[0]
                # Move vector
                vec = (loc[0] - prevloc[0], loc[1] - prevloc[1])
                # Single square movement vectors
                vecs = list(itertools.product([-1, 1], [-1, 1]))
                # If moving one square
                if vec in vecs:
                    # Check previous location for forced moves
                    if self.forced(prevloc):
                        print('Player must jump')
                        return False
                # If jumping two squares
                else:
                    if not self.canjump(prevloc, loc, piece):
                        print('Can\'t jump')
                        return False
        return True

    def forced(self, loc):
        # CHECK FOR FORCED MOVES

        # Add tuple to list
        def addtuple(a, x):
            a.append(x)
            return a
        # Four directions
        vecs = list(itertools.product([-1, 1], [-1, 1]))
        # Location neighbors
        neighbors = functools.reduce(lambda a, i:
                                     addtuple(
                                         a, tuple(map(lambda x: x[0] + x[1], zip(loc, vecs[i])))),
                                     range(4), [])
        # All possible locations in grid
        gridlist = list(itertools.product(range(10), range(10)))
        # Filter neighbors by possible locations
        neighbors = list(filter(lambda x: x in gridlist, neighbors))
        # Filter if any enemy neighbors
        enemies = list(filter(lambda x: self.board[
                       x[0], x[1]] == self.enemy, neighbors))
        # Return true if there are enemy neighbors
        return True if enemies else False

    def canjump(self, prevloc, loc, piece):
        # CHECK IF JUMP IS POSSIBLE

        # If end location is clear
        if piece == ' ':
            # Jump vector
            vec = (loc[0] - prevloc[0], loc[1] - prevloc[1])
            # Allowed jump vectors
            vecs = list(itertools.product([-2, 2], [-2, 2]))
            # If jump vector allowed
            if vec in vecs:
                # Intermediate location to check
                checkloc = ((prevloc[0] + loc[0]) // 2,
                            (prevloc[1] + loc[1]) // 2)
                if self.board[checkloc[0], checkloc[1]] == self.enemy:
                    return True
                else:
                    return False
            else:
                return False
        else:
            return False

    def update(self):
        self.board = np.copy(self.boardinit)
        for move in self.moves:
            i = move[1]
            loc = list(zip(*np.where(self.boardnames == i)))[0]
            for f in move[2:]:
                dest = list(zip(*np.where(self.boardnames == f)))[0]
                vec = (dest[0] - loc[0], dest[1] - loc[1])
                vecs = list(itertools.product([-1, 1], [-1, 1]))
                if vec not in vecs:
                    med = ((loc[0] + dest[0]) // 2, (loc[1] + dest[1]) // 2)
                    self.board[med[0], med[1]] = ' '
                self.board[dest[0], dest[1]] = self.board[loc[0], loc[1]]
                self.board[loc[0], loc[1]] = ' '
                loc = dest


def main():
    print('Terminal International Draughts')
    game = draughts()
    demo = open('filtered.txt', 'r')
    # for line in demo:
    #     time.sleep(0.25)
    #     game.print()
    #     move = line
    #     game.move(move)
    #     game.update()
    while True:
        if game.isref:
            game.reference()
        else:
            game.print()
            move = input('Enter move: ')
            game.move(move)
            game.update()

main()
