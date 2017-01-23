from termcolor import colored
import sys


class Square:

    def __init__(self):
        self.state = [False] * 4
        self.team = 0


class Dots:

    def __init__(self, n):
        self.size = n
        self.grid = [[Square() for col in range(n)] for row in range(n)]
        self.edges = [[False] * (n + 1) if row &
                      1 else [False] * n for row in range(2 * n + 1)]
        self.cursor = [0, 0]
        self.turn = 1
        self.score = [0, 0]
        self.endgame = False

    def nexturn(self):
        self.turn = 1 + self.turn % 2

    def makeline(self):
        row = self.cursor[0]
        col = self.cursor[1]
        n = self.size
        if not self.edges[row][col]:
            self.edges[row][col] = True

            # If row is odd
            if row & 1:
                squares = filter(lambda x: 0 <= x[0] and x[0] < n and 0 <= x[1] and x[1] < n,
                                 [(row // 2, col - 1, 1), (row // 2, col, 3)])
            # If row is even
            else:
                squares = filter(lambda x: 0 <= x[0] and x[0] < n and 0 <= x[1] and x[1] < n,
                                 [(row // 2 - 1, col, 2), (row // 2, col, 0)])

            madeBox = False
            # For every square the edge touches
            for square in squares:
                # Set the corresponding edge of square to True
                gridrow = square[0]
                gridcol = square[1]
                statedir = square[2]
                s = self.grid[gridrow][gridcol]
                s.state[statedir] = True
                # If square's edges all True
                if all(s.state):
                    # Assign square's team
                    s.team = self.turn
                    # Increment score
                    self.score[self.turn - 1] += 1
                    # Make sure player continues turn
                    madeBox = True

            # End game if all edges are True
            if all([all(r) for r in self.edges]):
                self.endgame = True

            # If no box is made, next turn
            if not madeBox:
                self.nexturn()

    def movecursor(self, m):
        row = self.cursor[0]
        col = self.cursor[1]
        n = self.size

        if m == 'u' and row > 0:
            self.cursor[0] = row - 1
            self.cursor[1] = min(col, n - 1)
        elif m == 'd' and row < 2 * n:
            self.cursor[0] = row + 1
            self.cursor[1] = min(col, n - 1)
        elif m == 'r' and col < n - 1 + int(row & 1):
            self.cursor[1] = col + 1
        elif m == 'l' and col > 0:
            self.cursor[1] = col - 1

    def move(self, m):
        if m == 'esc':
            self.endgame = True
        elif m == 'line':
            self.makeline()
        else:
            self.movecursor(m)

    def state(self):
        # Clear screen
        print('\033c')
        # For every row of GAME SCSREEN
        for i in range(2 * self.size + 1):
            # For every col of GAME SCREEN
            for j in range(2 * self.size + 1):
                # If cursor, color appropriately
                if i == self.cursor[0] and j // 2 == self.cursor[1] and i + j & 1:
                    sys.stdout.write(
                        colored('  ', 'white', 'on_blue' if self.turn == 1 else 'on_red'))
                # If not cursor
                else:
                    # If odd row
                    if i & 1:
                        # If odd column
                        if j & 1:
                            t = self.grid[i // 2][j // 2].team
                            if t == 0:
                                sys.stdout.write('  ')
                            else:
                                sys.stdout.write(
                                    colored('  ', 'white', 'on_blue' if t == 1 else 'on_red'))
                        # If even column
                        else:
                            e = self.edges[i][j // 2]
                            sys.stdout.write(
                                colored('  ', 'white' if e else None, 'on_white' if e else None))
                    # If even row
                    else:
                        # If odd column
                        if j & 1:
                            e = self.edges[i][j // 2]
                            sys.stdout.write(
                                colored('  ', 'white' if e else None, 'on_white' if e else None))
                        # If even column
                        else:
                            sys.stdout.write(
                                colored('  ', 'white', 'on_white'))

            sys.stdout.write('\n')

        if self.turn == 1:
            print('Blue turn')
        else:
            print('Red turn')

# Class for detecting single character


class _GetchUnix:

    def __init__(self):
        import tty
        import sys
        import termios

    def __call__(self):
        import sys
        import tty
        import termios
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch

# Returns key that is pressed


def getKey():
    inkey = _GetchUnix()
    return inkey()


def main():
        # Initialize game
    g = Dots(5)
    g.state()
    # Legal moves
    moves = {27: 'esc', 119: 'u', 100: 'r', 115: 'd', 97: 'l', 13: 'line'}
    # Play while game no finished
    while not g.endgame:
        m = ord(getKey())
        if m in moves:
            g.move(moves[m])
            g.state()

    # Print scores and game result
    print()
    print('Blue:', g.score[0], 'Red:', g.score[1])
    if g.score[0] == g.score[1]:
        print('Players Tied')
    else:
        print('Blue Won' if g.score[0] > g.score[1] else 'Red Won')

main()
