import sys
import tty
import termios
import time

from itertools import product
from functools import reduce
from termcolor import colored
from numpy import array


class conway(object):
    '''Conway's Game of Life Class'''
    def __init__(self, rows, cols):
        self.size = [rows, cols]
        self.grid = array([[False]*cols]*rows)
        self.cursor = [rows // 2, cols // 2]
        self.showcursor = True
        self.animating = False
        self.done = False

    def state(self, x, y):
        return self.grid[x % self.size[0]][y % self.size[1]]

    def neighbors(self, x, y):
        dirs = list(product([-1, 0, 1], [-1, 0, 1]))
        dirs.remove((0, 0))
        return reduce(lambda a, v: a + self.state(x + v[0], y + v[1]), dirs, 0)

    def next(self, x, y):
        return self.neighbors(x, y) == 3 or self.neighbors(x, y) == 2 and self.state(x, y)

    def nextgrid(self):
        self.grid = array([[self.next(i, j) for j in range(self.size[1])] for i in range(self.size[0])])

    def move(self, move):
        if move == 'esc':
            self.done = True
        elif move == 'clear':
            self.grid = array([[False]*self.size[1]]*self.size[0])
        elif move == 'press':
            if not self.showcursor:
                self.showcursor = True
            else:
                self.press()
        elif move == 'play':
            self.showcursor = False
            self.nextgrid()
        elif move == 'animate':
            self.showcursor = False
            self.animating = True
            # Somehow implement animation until keypress
            for i in range(20):
                self.nextgrid()
                self.show()
                time.sleep(0.05)
        else:
            self.showcursor = True
            self.movecursor(move)

    def press(self):
        '''Click'''
        row, col = self.cursor
        self.grid[row][col] ^= True

    def movecursor(self, move):
        '''Moves cursor'''
        self.cursor[move in ['l', 'r']] += [-1, 1][move in ['d', 'r']]
        self.cursor[0] %= self.size[0]
        self.cursor[1] %= self.size[1]

    def show(self):
        '''Prints out grid to console'''
        # Clear screen
        print("\033c")
        # Title
        print("Conway's Game of Life")
        # Print grid
        for r in range(self.size[0]):
            for c in range(self.size[1]):
                if self.showcursor and [r, c] == self.cursor:
                    text = colored('  ', 'white', 'on_green')
                else:
                    text = colored('  ', 'white', 'on_white' if self.state(r, c) else 'on_grey')
                sys.stdout.write(text)
            sys.stdout.write('\n')

class _GetchUnix(object):

    def __init__(self):
        pass

    def __call__(self):
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch

def getkey():
    '''Gets user keyboard input'''
    inkey = _GetchUnix()
    return inkey()

def main():
    '''Main'''
    moves = {27: 'esc', 119: 'u', 100: 'r', 115: 'd', 97: 'l', 99: 'clear', 13: 'press', 112: 'play', 32: 'animate'}
    g = conway(40, 40)
    g.show()
    while not g.done:
        move = ord(getkey())
        if move in moves:
            g.move(moves[move])
            g.show()

main()
