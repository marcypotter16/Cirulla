from Card import Card
from random import shuffle

class Board:
    def __init__(self):
        self.carte: list[Card] = []

class Deck:
    def __init__(self, size = 40):
        self.cards = []
        for i in range(1, 11):
            for s in ["P", "C", "Q", "F"]:
                self.cards.append(Card(i, s))

    def shuffle(self):
        shuffle(self.cards)

    def draw(self, howmany = 1) -> list:
        return [self.cards.pop() for _ in range(howmany)]

    def __str__(self):
        s = "["
        for card in self.cards:
            s += str(card) + ", "
        return s[0:-2] + "]"



class Game:
    def __init__(self):
        self.board = Board()
        self.turn_count = 0
        self.players = []
        self.deck: Deck = Deck()
        print(self.deck)

    def play_turn(self):
        for p in self.players:
            p.draw_card(self.deck, 3)

if __name__ == "__main__":
    g = Game()