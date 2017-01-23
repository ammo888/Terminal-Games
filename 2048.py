from termcolor import colored
import numpy as np
import itertools
import random


class Grid(object):
    # Initializer

    def __init__(self):
        self.grid = np.zeros((4, 4), dtype=np.int)
        self.tuples = list(itertools.product(list(range(4)), list(range(4))))
        self.txtcolors = {0: ('white', None), 2: ('red', None), 4: ('yellow', None),
                          8: ('green', None), 16: ('cyan', None), 32: ('magenta', None),
                          64: ('white', 'on_grey'), 128: ('red', 'on_grey'), 256: ('yellow', 'on_grey'),
                          512: ('green', 'on_grey'), 1024: ('cyan', 'on_grey'), 2048: ('magenta', 'on_grey')}
        self.score = 0
        self.canPlay = True

    # Adds n numbers to grid
    def seed(self, n):
        # Checks for any places in grid with 0s
        candidates = list(
            filter(lambda x: self.grid[x[0]][x[1]] == 0, self.tuples))
        # If such places exist
        if candidates:
            # Select n of them
            points = random.sample(candidates, n)
            # Add 2 or 4 to grid
            for x in points:
                self.grid[x[0]][x[1]] = np.random.choice([2, 4], 1, p=[0.9, 0.1])
        else:
            # If can't add number, end game (some exceptions)
            self.canPlay = False

    # Move
    def move(self, dir):
        # dir:
        # -1 is quit
        # 0 is up
        # 1 is right
        # 2 is down
        # 3 is left

        # Quit
        if dir == -1:
            self.canPlay = False
            return
        # Make grid copy
        newgrid = np.copy(self.grid)
        # Transpose matrix if dir is even
        if dir & 1 == 0:
            newgrid = np.transpose(newgrid)
        # Flip matrix l-r if swipe is right (including transpose)
        if dir % 3 != 0:
            newgrid = np.fliplr(newgrid)

        # For each row in grid
        for i in range(4):
            row = newgrid[i]
            # Left justify nonzero values
            row = list(filter(lambda x: x != 0, row)) + \
                [0] * (np.array(row) == 0).sum(0)
            # Go through every consecutive pair in row
            for j in range(3):
                # If pair matching
                if row[j] == row[j + 1] and row[j] != 0:
                    # Combine values
                    # Double left value
                    row[j] *= 2
                    # Make right value 0
                    row[j + 1] = 0
                    # Left justify non zero values
                    row = list(filter(lambda x: x != 0, row)) + \
                        [0] * (np.array(row) == 0).sum(0)
                    # Increment score
                    self.score += row[j]
            # Put modified row back in
            newgrid[i] = row

        # Unflip
        if dir % 3 != 0:
            newgrid = np.fliplr(newgrid)
        # Untranspose
        if dir & 1 == 0:
            newgrid = np.transpose(newgrid)

        # End game if 2048 in grid
        if 2048 in newgrid:
            self.grid = newgrid
            self.canPlay = False
        # Replace grid and seed only if grid changed
        elif not (self.grid == newgrid).all():
            self.grid = newgrid
            self.seed(1)
        # If grid is full, no change after move
        elif self.grid.all():
            # If no legal moves left, end game
            if not((self.grid[:, :3] == self.grid[:, 1:]).any() or (self.grid[:3, :] == self.grid[1:, :]).any()):
                self.canPlay = False

    def state(self):
        print('\033c')
        print('Score:', self.score)
        print()
        for row in self.grid:
            print(''.join(colored(str(x).rjust(4), self.txtcolors[
                  x][0], self.txtcolors[x][1]) + ' ' for x in row))
            print()

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
    # Legal moves dictionary
    ctoint = {'q': int(-1), 'w': 0, 'd': 1, 's': 2, 'a': 3}
    # Initialize game
    game = Grid()
    # Seed with 2 values
    game.seed(2)
    # Play until no moves left
    while game.canPlay:
        # Print grid state
        game.state()
        # Get keyboard input
        d = getKey()
        # Make move if legal
        if d in ctoint:
            game.move(ctoint[d])

    game.state()
    # Print final score once game finished
    print('Final Score:', game.score)
    return

main()
