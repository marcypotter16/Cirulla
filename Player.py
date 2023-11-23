from Board import Deck
from Card import Card

class Player:
    def __init__(self):
        self.hand = []
        self.won_cards = []

    def draw_cards(deck: Deck, amount: int):
        cards_to_draw = deck.draw(amount)
        if len(cards_to_draw) + len(hand) > 3:
            raise ValueError("Sono state pescate un troppe carte")
        self.hand.extend(cards_to_draw)

    def is_buona_tre(self) -> bool:
        if len(self.hand) == 3:
            if "7C" not in [str(c) for c in self.hand]:
                return sum([c.valore for c in self.hand]) < 10
            else:
                return sum([c.valore for c in self.hand if str(c) != "7C"]) < 9
        return False
    
    def is_buona_dieci(self) -> bool:
        if len(self.hand) == 3:
            cards = [c for c in self.hand if str(c) != "7C"]
            val = cards[0].valore
            return all([c.valore == val for c in cards])
        return False

if __name__ == "__main__":
    p1 = Player()
    p1.hand = [
        Card(1, "Q"),
        Card(1, "F"),
        Card(1, "D")
    ]

    p2 = Player()
    p2.hand = [
        Card(1, "Q"),
        Card(4, "D"),
        Card(3, "D")
    ]

    p3 = Player()
    p3.hand = [
        Card(3, "Q"),
        Card(3, "F"),
        Card(7, "C")
    ]

    p4 = Player()
    p4.hand = [
        Card(2, "F"),
        Card(3, "F"),
        Card(7, "C")
    ]

    players = [p1, p2, p3, p4]
    for p in players:
        print(p.is_buona_tre(), p.is_buona_dieci())