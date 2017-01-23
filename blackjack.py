import functools
import itertools
import time
import random


class Card:

    def __init__(self, r, s):
        self.rank = r
        self.suit = s
        self.ranks = dict([('A', 1), ('2', 2), ('3', 3), ('4', 4),
                           ('5', 5), ('6', 6), ('7', 7), ('8', 8), ('9', 9),
                           ('10', 10), ('J', 10), ('Q', 10), ('K', 10)])

    def value(self):
        return self.ranks[self.rank]


class Shoe:

    def __init__(self, d):
        ranks = ['A', '2', '3', '4',
                 '5', '6', '7', '8',
                 '9', '10', 'J', 'Q', 'K']
        suits = ['S', 'C', 'H', 'D']
        decks = list(itertools.product(ranks, suits)) * d
        random.shuffle(decks)
        self.shoe = functools.reduce(
            lambda a, x: a + [Card(x[0], x[1])], decks, [])

    def getCard(self):
        return self.shoe.pop()


class Player:

    def __init__(self):
        self.hand = []
        self.wallet = 100
        self.betting = 0
        self.showing = False
        self.blackjack = False

    def addCard(self, card):
        self.hand.append(card)

    def bet(self, amount):
        if amount <= self.wallet:
            self.wallet -= amount
            self.betting += amount
        else:
            print('Not enough money to bet')

    def bestvalue(self):
        value = functools.reduce(lambda a, x: a + x.value(), self.hand, 0)
        if [x for x in self.hand if x.rank == 'A']:
            value = value + 10 if value <= 11 else value
        return value

    def isbust(self):
        value = self.bestvalue()
        return True if value > 21 else False


class Board:

    def __init__(self, num):
        self.shoe = Shoe(6)
        self.players = [Player() for x in range(1 + num)]
        self.turn = 0
        self.rounddone = False
        self.gamedone = False

    def deal(self):
        for player in self.players:
            player.addCard(self.shoe.getCard())
            if self.players.index(player) != 0:
                player.addCard(self.shoe.getCard())
            if player.bestvalue() == 21:
                player.blackjack = True

    def rotateturn(self):
        self.players[self.turn].showing = False
        self.turn = (self.turn + 1) % len(self.players)

    def bet(self, amount):
        if self.turn != 0:
            self.players[self.turn].bet(amount)

    def hit(self):
        player = self.players[self.turn]
        if not player.isbust():
            player.addCard(self.shoe.getCard())

    def stand(self):
        self.rotateturn()

    def double(self):
        self.bet(self.players[self.turn].betting)
        self.hit()
        self.stand()

    def checkvalue(self):
        return self.players[self.turn].bestvalue()

    def show(self):
        self.players[self.turn].showing = True

    def hide(self):
        self.players[self.turn].showing = False

    def winners(self):
        # 0 - loss
        # 1 - win
        # 2 - blackjack
        # 3 - tie
        dealervalue = self.players[0].bestvalue()

        def didwin(player):
            if player.bestvalue() < dealervalue:
                return 0
            elif player.bestvalue() > dealervalue:
                if player.isbust():
                    return 0
                else:
                    return 1
            else:
                if player.blackjack == 1:
                    return 2
                else:
                    return 3
        if dealervalue > 21:
            arr = functools.reduce(
                lambda a, x: a + [0 if x.isbust() else 1], self.players, [])
        else:
            arr = functools.reduce(
                lambda a, x: a + [didwin(x)], self.players, [])
        return arr

    def pay(self):
        winners = self.winners()
        for i in range(len(winners)):
            if i != 0:
                if winners[i] == 1:
                    self.players[i].wallet += 2 * self.players[i].betting
                elif winners[i] == 2:
                    self.players[i].wallet += 2.5 * self.players[i].betting
                elif winners[i] == 3:
                    self.players[i].wallet += 1 * self.players[i].betting
            self.players[i].betting = 0

    def nextround(self):
        for player in self.players:
            player.hand = []
            player.showing = False
            player.blackjack = False
        self.rounddone = False

    def state(self):
        print("\033c")
        # Round not done
        if not self.rounddone:
            for player in self.players:
                if self.players.index(player) == 0:
                    name = 'Dealer:'
                elif self.players.index(player) == self.turn:
                    name = 'You:'
                else:
                    name = 'Player ' + str(self.players.index(player)) + ':'
                if player.showing or self.players.index(player) == 0:
                    print(name, ''.join(
                        [x.rank + x.suit + ' ' for x in player.hand]))
                else:
                    print(name, ''.join(['__ ' for x in player.hand]))
            print('Currently betting:', '$' +
                  str(self.players[self.turn].betting))
            print('In wallet:', '$' + str(self.players[self.turn].wallet))

        # Round is done
        else:
            # Show everyone's cards
            for player in self.players:
                if self.players.index(player) == 0:
                    name = 'Dealer:'
                else:
                    name = 'Player ' + str(self.players.index(player)) + ':'
                print(name, ''.join(
                    [x.rank + x.suit + ' ' for x in player.hand]), '-', player.bestvalue())
            # Show winners and losers
            winners = self.winners()
            print()
            for i in range(len(winners)):
                if i == 0:
                    if winners[i] == 0:
                        print('Dealer busts')
                else:
                    if winners[i] == 0:
                        print('Player', i, 'loses', '$' +
                              str(self.players[i].betting))
                    elif winners[i] == 1:
                        print('Player', i, 'wins', '$' +
                              str(self.players[i].betting))
                    elif winners[i] == 2:
                        print('Player', i, 'wins', '$' +
                              str(1.5 * self.players[i].betting))
                    else:
                        print('Player', i, 'is returned', '$' +
                              str(self.players[i].betting))
            self.pay()
            print()
            for player in self.players:
                if self.players.index(player) != 0:
                    name = 'Player ' + str(self.players.index(player))
                    print(name, 'has', '$' + str(player.wallet), 'in wallet')


def main():
    print('Starting Terminal Blackjack')
    time.sleep(1)
    g = Board(2)
    moves = ['hit', 'stand', 'double', 'show', 'hide', 'quit']
    # While game is running
    while not g.gamedone:
        # Deal cards
        g.deal()
        # Place initial bets
        for player in g.players:
            # Excluding dealer
            if g.players.index(player) != 0:
                name = 'Player ' + str(g.players.index(player)) + ','
                bet = int(input(name + ' place bet: '))
                g.bet(bet)
            g.rotateturn()
        # Switch turn to first player
        g.rotateturn()
        # While not dealer
        while g.turn != 0:
            g.state()
            move = input('Enter move: ')
            if move in moves:
                if move == 'quit':
                    print()
                    print('Closing Terminal Blackjack')
                    return
                else:
                    command = 'g.' + move + '()'
                    exec(command)
        # When all players done
        while not g.rounddone:
            # While dealer is less than 17
            while g.checkvalue() < 17:
                # Hit dealer
                g.state()
                g.hit()
                time.sleep(0.75)
            # Round is done
            g.rounddone = True
        # Display results
        g.state()
        print()
        roundcheck = input('Another round? [y/n]: ')
        if roundcheck == 'y':
            g.nextround()
            print("\033c")
        else:
            g.gamedone = True
    print()
    print('Closing Terminal Blackjack')
    return

main()
