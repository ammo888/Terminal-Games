import sys
import tty
import termios
import time

from random import sample
from itertools import product, combinations
from functools import reduce
from termcolor import colored
from numpy import array, copy

# TO DO:
# Comment all statements
# Add docstrings to functions
# Add AI ability to try 50/50s or fix them
# Add AI tree for low # of flags left and lots of nums
# Change hasnum to a list of nums that aren't satisfied yet


class Minesweeper(object):
    '''Minesweeper Class'''
    def __init__(self, level):
        sizedict = {1: [8, 8], 2: [10, 10], 3: [12, 12], 4: [16, 16], 5: [16, 32]}
        bombsdict = {1: 6, 2: 10, 3: 18, 4: 40, 5: 99}
        self.size = sizedict[level]
        self.numbombs = bombsdict[level]
        self.mines = array([[False]*self.size[1]]*self.size[0])
        self.nums = array([[0]*self.size[1]]*self.size[0])
        self.player = array([[0]*self.size[1]]*self.size[0])
        self.cursor = [self.size[0] // 2, self.size[1] // 2]
        self.endgame = False
        self.win = False
        self.tuples = list(product([x for x in range(self.size[0])],
                                   [x for x in range(self.size[1])]))

    def clear(self):
        self.mines = array([[False]*self.size[1]]*self.size[0])
        self.nums = array([[0]*self.size[1]]*self.size[0])
        self.player = array([[0]*self.size[1]]*self.size[0])

    def seed(self):
        '''Places bombs in grid'''
        row = self.cursor[0]
        col = self.cursor[1]
        choices = self.tuples[:]
        for a in range(-1, 2):
            for b in range(-1, 2):
                if (row + a, col + b) in choices:
                    choices.remove((row + a, col + b))
        chosen = sample(choices, self.numbombs)
        for i, j in chosen:
            self.mines[i][j] = True
            for hor in range(-1, 2):
                for ver in range(-1, 2):
                    if (i+hor, j+ver) in self.tuples:
                        if self.mines[i+hor][j+ver]:
                            self.nums[i+hor][j+ver] = 9
                        else:
                            self.nums[i+hor][j+ver] += 1

    def solveable(self):
        '''Checks if solveable without guessing'''
        # Tuples of mines
        mines = [x for x in self.tuples if self.mines[x[0]][x[1]]]
        notmines = [x for x in self.tuples if not self.mines[x[0]][x[1]]]
        udrl = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        dirs = list(product([-1, 0, 1], [-1, 0, 1]))
        dirs.remove((0, 0))


        # Checks if allbombs have numbers next to them
        for m in mines:
            num_next = False
            for d in dirs:
                n = tuple(map(sum, zip(m, d)))
                if n in self.tuples:
                    if self.nums[n[0]][n[1]] in range(1, 9):
                        num_next = True
            if not num_next:
                print('hi')
                return False
        # Checks for 50/50 pairs

        # Creates list of pairs
        pairs = []
        for m in mines:
            for v in udrl:
                n = tuple(map(sum, zip(m, v)))
                if n in notmines and set([m, n]) not in pairs:
                    pairs.append(set([m,n]))
        for p in pairs:
            # Checks if pair has same non-mine neighbors
            p1, p2 = p
            p1_nums = []
            p2_nums = []
            for d in dirs:
                n1 = tuple(map(sum, zip(p1, d)))
                n2 = tuple(map(sum, zip(p2, d)))
                if n1 in self.tuples:
                    if n1 != p2 and self.nums[n1[0]][n1[1]] in range(0, 9):
                        p1_nums.append(n1)
                if n2 in self.tuples:
                    if n2 != p1 and self.nums[n2[0]][n2[1]] in range(0, 9):
                        p2_nums.append(n2)
            if set(p1_nums) == set(p2_nums):
                return False
        return True

    def move(self, move):
        '''Performs move'''
        if move == 'esc':
            self.endgame = True
        elif move == 'press':
            self.open()
        elif move == 'flag':
            self.flag()
        else:
            self.movecursor(move)

    def press(self, row, col):
        '''Click'''
        if self.player[row][col] == 0:
            self.player[row][col] = 1
            return True
        return False

    def flag(self):
        '''Flags cell'''
        row = self.cursor[0]
        col = self.cursor[1]
        if self.player[row][col] == 0 and (self.player == 2).sum() < self.numbombs:
            self.player[row][col] = 2
        elif self.player[row][col] == 2:
            self.player[row][col] = 0

    def movecursor(self, move):
        '''Moves cursor'''
        row = self.cursor[0]
        col = self.cursor[1]
        if move == 'u' and row > 0:
            self.cursor[0] -= 1
        elif move == 'd' and row < self.size[0] - 1:
            self.cursor[0] += 1
        elif move == 'r' and col < self.size[1] - 1:
            self.cursor[1] += 1
        elif move == 'l' and col > 0:
            self.cursor[1] -= 1

    def open(self):
        '''Opens up field'''
        row = self.cursor[0]
        col = self.cursor[1]
        if self.mines[row][col]:
            self.press(row, col)
        else:
            self.openrcs(row, col)

    def openrcs(self, row, col):
        '''Recursive helper for open()'''
        if (row, col) in self.tuples:
            if self.nums[row][col] == 0:
                if self.press(row, col):
                    dirs = list(product([-1, 0, 1], [-1, 0, 1]))
                    dirs.remove((0, 0))
                    for d in dirs:
                        self.openrcs(row + d[0], col + d[1])
            else:
                self.press(row, col)

    def show(self):
        '''Prints out grid to console'''
        # Clear screen
        print("\033c")
        # Print top border
        print(colored('  ' * (self.size[1] + 2), 'white', 'on_blue'))
        for row in range(self.size[0]):
            # Print left border cell
            sys.stdout.write(colored(' ' * 2, 'white', 'on_blue'))
            for col in range(self.size[1]):
                num = self.nums[row][col]
                state = self.player[row][col]
                mine = self.mines[row][col]
                # Color cursor
                if self.cursor[0] == row and self.cursor[1] == col:
                    if num not in [0, 9] and state == 1:
                        text = ' ' + str(num)
                    else:
                        text = '  '
                    textcolor = 'white'
                    color = 'on_green'
                else:
                    # Cell is hidden
                    if state == 0:
                        text = '  '
                        textcolor = 'white'
                        color = 'on_grey'
                    # Cell is flagged
                    elif state == 2:
                        text = '  '
                        textcolor = 'white'
                        color = 'on_magenta'
                    # Cell is shown
                    elif state == 1:
                        # Cell is a mine
                        if mine:
                            text = '  '
                            textcolor = 'white'
                            color = 'on_red'
                        # Cell is not a mine
                        else:
                            text = '  ' if num == 0 else ' ' + str(num)
                            textcolor = 'blue'
                            color = 'on_white'
                # Print out cell
                txt = colored(text, textcolor, color)
                sys.stdout.write(txt)
            # Print right border cell
            sys.stdout.write(colored(' ' * 2, 'white', 'on_blue'))
            # Move to next line
            sys.stdout.write('\n')
        # Print bottom border
        print(colored('  ' * (self.size[1] + 2), 'white', 'on_blue'))
        numflags = (self.player == 2).sum()
        print('Flags left:', self.numbombs - numflags)

    def showall(self):
        '''Prints out uncovered grid to console'''
        # Clear screen
        print("\033c")
        # Print top border
        print(colored('  ' * (self.size[1] + 2), 'white', 'on_blue'))
        for row in range(self.size[0]):
            # Print left border cell
            sys.stdout.write(colored(' ' * 2, 'white', 'on_blue'))
            for col in range(self.size[1]):
                num = self.nums[row][col]
                mine = self.mines[row][col]
                # Cell is a mine
                if mine:
                    text = '  '
                    textcolor = 'white'
                    color = 'on_red'
                # Cell is not a mine
                else:
                    text = '  ' if num == 0 else ' ' + str(num)
                    textcolor = 'blue'
                    color = 'on_white'
                # Print out cell
                txt = colored(text, textcolor, color)
                sys.stdout.write(txt)
            # Print right border cell
            sys.stdout.write(colored(' ' * 2, 'white', 'on_blue'))
            # Move to next line
            sys.stdout.write('\n')
        # Print bottom border
        print(colored('  ' * (self.size[1] + 2), 'white', 'on_blue'))
        numflags = (self.player == 2).sum()
        print('Flags left:', self.numbombs - numflags)

    def check(self):
        '''Checks if game is finished'''
        for i in range(self.size[0]):
            for j in range(self.size[1]):
                if self.mines[i][j]:
                    if self.player[i][j] == 1:
                        self.endgame = True
        if ((self.player == 2) == self.mines).all():
            self.endgame = True
            self.win = True


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


def play():
    '''Play'''
    print('TERMINAL MINESWEEPER')
    print('\'WASD\' to move cursor')
    print('\'Enter\' to press on cell')
    print('\'f\' to flag cell')
    print()
    level = input('Enter level (1-5): ')
    while not level.isdigit() or int(level) not in range(1, 6):
        print('Error: Invalid level number')
        level = input('Re-enter level (1-5): ')
    level = int(level)
    game = Minesweeper(level)
    game.show()
    initloc = False
    moves = {27: 'esc', 119: 'u', 100: 'r', 115: 'd', 97: 'l', 13: 'press', 102: 'flag'}
    while not game.endgame:
        move = ord(getkey())
        if move in moves:
            if not initloc and (moves[move] == 'press' or moves[move] == 'esc'):
                # Only seed once player has chosen start location
                game.seed()
                while not game.solveable():
                    game.clear()
                    game.seed()
                initloc = True
            game.move(moves[move])
            game.show()
            if initloc:
                game.check()
    game.showall()
    if game.win:
        print('You\'ve identified all the bombs!')
    else:
        print('You died.')


def ai_move(g, m, fast):
    '''Performs move, shows grid, checks status, pauses'''
    g.move(m)
    g.check()
    if not fast:
        g.show()
        time.sleep(0.05)


def ai_cursor(g, rf, cf, fast):
    '''Moves cursor to specified location'''
    ri, ci = g.cursor
    up = True if rf - ri <= 0 else False
    right = True if cf - ci >= 0 else False
    for i in range(abs(rf-ri)):
        ai_move(g, 'u', fast) if up else ai_move(g, 'd', fast)
    for i in range(abs(cf-ci)):
        ai_move(g, 'r', fast) if right else ai_move(g, 'l', fast)


def ai_analysis(g, i, j):
    '''Returns no. of flags and choices for cell'''
    flagged = 0
    choices = []
    dirs = list(product([-1, 0, 1], [-1, 0, 1]))
    dirs.remove((0, 0))
    for d in dirs:
        if (i + d[0], j + d[1]) in g.tuples:
            if g.player[i + d[0]][j + d[1]] == 0:
                choices.append((i + d[0], j + d[1]))
            elif g.player[i + d[0]][j + d[1]] == 2:
                flagged += 1
    return (flagged, choices)


def ai_logic(g, fast):
    '''AI logic'''
    hasnum = filter(lambda x: g.player[x[0]][x[1]] == 1 and g.nums[x[0]][x[1]] in range(1, 9), g.tuples)
    # Prioritizes top left corner to make the solving look more 'natural'
    hasnum = sorted(hasnum, key=lambda x: sum(x))

    for loc in hasnum:
        i, j = loc
        num = g.nums[i][j]
        flagged, choices = ai_analysis(g, i, j)
        # No. of hidden cells equal to remaining flags for the cell
        if len(choices) == num - flagged:
            for choice in choices:
                ai_cursor(g, choice[0], choice[1], fast)
                ai_move(g, 'flag', fast)
            if choices:
                break
        # Cell already satisfied - press remaining hidden cells
        elif flagged == num:
            for choice in choices:
                ai_cursor(g, choice[0], choice[1], fast)
                ai_move(g, 'press', fast)
            # This break will update the hasnum statement more often
            break
        # Case to check if one flag is guaranteed
        elif num - flagged >= 2:
            dirs = [(1, 0), (-1, 0), (0, 1), (0, -1)]
            for d in dirs:
                if (i + d[0], j + d[1]) in g.tuples:
                    # state, num, flags, and choices of neighboring cell
                    state2 = g.player[i + d[0]][j + d[1]]
                    num2 = g.nums[i + d[0]][j + d[1]]
                    flagged2, choices2 = ai_analysis(g, i + d[0], j + d[1])
                    # only care if cell is shown and has less flags needed
                    if state2 == 1 and num - flagged > num2 - flagged2 > 0:
                        # combinations of flags
                        combos = list(combinations(choices, num - flagged))
                        # delete combos that can't happen with neighboring cell
                        for combo in combos:
                            if combo in list(combinations(choices2, num - flagged)):
                                combos.remove(combo)
                        # find required flag and flag, if exists
                        combos = [set(x) for x in combos]
                        toflag = list(reduce(lambda a, x: a & x, combos))
                        if toflag:
                            ai_cursor(g, toflag[0][0], toflag[0][1], fast)
                            ai_move(g, 'flag', fast)


def ai(level):
    '''AI'''
    game = Minesweeper(level)
    # Initial seeding and press
    game.seed()
    while not game.solveable():
        game.clear()
        game.seed()
    game.move('press')
    game.show()
    time.sleep(1)
    aiplaying = True
    while not game.endgame:
        if aiplaying:
            init = copy(game.player)
            # Change second parameter to:
            # True - skips to when AI is done
            # False - shows all of AI's steps
            ai_logic(game, False)   
            if (game.player == init).all():
                # Show grid in case using FAST AI
                game.show()
                print('AI couldn\'t identify all the mines')
                print('Continue playing? Press y/n: ')
                inplay = getkey()
                while inplay not in ['y', 'n']:
                    print('Error: Invalid option. Press y/n: ')
                    inplay = getkey()
                if inplay == 'y':
                    aiplaying = False
                    # Show grid and instructions to play
                    game.show()
                    print('\'WASD\' to move cursor')
                    print('\'Enter\' to press on cell')
                    print('\'f\' to flag cell')
                else:
                    return
        else:
            moves = {27: 'esc', 119: 'u', 100: 'r', 115: 'd', 97: 'l', 13: 'press', 102: 'flag'}
            move = ord(getkey())
            if move in moves:
                game.move(moves[move])
                game.check()
                game.show()
    game.showall()
    if aiplaying:
        print('AI identified all the mines')
    else:
        if game.win:
            print('You\'ve identified all the mines!')
        else:
            print('You died.')


def ai_test(level):
    '''Finds average flags left'''
    endscore = 0
    for i in range(100):
        game = Minesweeper(level)
        game.seed()
        game.move('press')
        while not game.endgame:
            init = copy(game.player)
            ai_logic(game, True)
            if (game.player == init).all():
                break
        endscore += game.numbombs - (game.player == 2).sum()
    print(endscore / 100)


def main():
    '''Main'''
    if sys.argv[1] == 'play':
        play()
    if sys.argv[1] == 'ai':
        ai(int(sys.argv[2]))

main()
# g = Minesweeper(5)
# g.seed()
# g.showall()
# g.solveable()
