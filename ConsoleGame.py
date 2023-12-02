from more_itertools import powerset
from Card import Card, Presa
from random import shuffle

class Board:
    def __init__(self):
        self.cards: list[Card] = []

    def calculate_sums(self) -> list[Presa]:
        l = []
        for sublist in powerset(self.cards):
            l.append(Presa(sublist))
        return l
    
    def find_prese_possibili(self) -> list[Presa]:
        l = self.calculate_sums()
        for p in l:
            if p.valore <= 15:
                cards = p.cards
                new_p = Presa(cards)
                new_p.valore = 15 - p.valore
                l.append(new_p)
        return l
    
    def __str__(self) -> str:
        s = "["
        for card in self.cards:
            s += str(card) + ", "
        return s[0:-2] + "]"

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




if __name__ == "__main__":
    pass
    # g = Game()